from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

import base64
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Set up Jinja2 templates directory for HTML rendering
templates = Jinja2Templates(directory="templates")

# Load GROQ API key and endpoint from environment variables
GROQ_API_URL = os.getenv("GROQ_API_URL")  # FIX: was hardcoded inside `os.getenv()`
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validate that the API key is set
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")

# Route to render the index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to accept image uploads and text queries
@app.post("/upload_and_query")
async def upload_and_query(image: UploadFile = File(...), query: str = Form(...)):
    try:
        # Read image content from the uploaded file
        image_content = await image.read()
        if not image_content:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Try to verify that it's a valid image using PIL
        try:
            img = Image.open(io.BytesIO(image_content))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

        # Convert the image to base64 encoding for API usage
        encoded_image = base64.b64encode(image_content).decode("utf-8")

        # Analyze the user's query to tailor the API prompt
        api_query = query
        lower_query = query.lower()

        if "alternate diagnoses" in lower_query or "other possibilities" in lower_query or "what else could it be" in lower_query:
            api_query = query + " Please also provide a list of plausible alternate diagnoses and their characteristics."
        elif "treatment" in lower_query or "how to treat" in lower_query or "what to do" in lower_query:
             api_query = query + " Please provide information on potential treatment options."
        elif "prevention" in lower_query or "how to prevent" in lower_query or "avoid" in lower_query:
             api_query = query + " Please provide tips on how to prevent this condition."
        else:
             # Default instruction for general queries
             api_query = query + " Please provide a detailed analysis of the image."

        # Prepare the message payload for the chat API with image and query
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": api_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]

        # Helper function to call the GROQ API with a specified model
        def make_api_request(model: str):
            response = requests.post(
                GROQ_API_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 1000
                },
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            return response

        # Call both vision models
        llama_response = make_api_request("meta-llama/llama-4-scout-17b-16e-instruct")
        llava_response = make_api_request("meta-llama/llama-4-maverick-17b-128e-instruct")

        # Parse and collect responses
        responses = {}
        for model_name, response in [("llama", llama_response), ("llava", llava_response)]:
            if response.status_code == 200:
                result = response.json()
                try:
                    answer = result["choices"][0]["message"]["content"]
                    logger.info(f"{model_name} response: {answer[:100]}...")
                    responses[model_name] = answer
                except (KeyError, IndexError) as e:
                    logger.error(f"Malformed response from {model_name}: {result}")
                    responses[model_name] = "Malformed response received"
            else:
                logger.error(f"Error from {model_name} API: {response.status_code} - {response.text}")
                responses[model_name] = f"Error from {model_name} API: {response.status_code}"

        return JSONResponse(status_code=200, content=responses)

    except HTTPException as he:
        logger.error(f"HTTP Exception: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Run the app with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8001)
