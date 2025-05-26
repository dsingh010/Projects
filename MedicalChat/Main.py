import base64
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check that the API key is defined
if not GROQ_API_KEY:
    raise ValueError("API Key is not defined. Please set GROQ_API_KEY in your environment variables.")

def process_image(img_path, query):
    """
    Processes an image and sends it to the Groq vision models for analysis.

    Parameters:
    - img_path: Path to the image file.
    - query: A textual prompt to be sent along with the image.

    Returns:
    - A dictionary with results from different Groq vision models.
    """
    try:
        # Read and base64-encode the image
        with open(img_path, 'rb') as img_file:
            img_content = img_file.read()
            encoded_image = base64.b64encode(img_content).decode("utf-8")

        # Validate image using PIL
        try:
            img = Image.open(io.BytesIO(img_content))
            img.verify()  # Will raise if image is corrupted
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}")
            return {"error": f"Invalid image format: {str(e)}"}

        # Create the message payload
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]

        def make_api_request(model):
            """
            Makes a POST request to the Groq API with a given model.

            Parameters:
            - model: The model ID string.

            Returns:
            - Response object from the API.
            """
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

        # Make API requests to both models
        llama_response = make_api_request("meta-llama/llama-4-scout-17b-16e-instruct")
        llava_response = make_api_request("meta-llama/llama-4-maverick-17b-128e-instruct")

        responses = {}

        # Handle both responses
        for model, response in [("llama11b", llama_11b_response), ("llama90b", llama_90b_response)]:
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                logger.info(f"Processed response from {model}: {answer}")
                responses[model] = answer
            else:
                logger.error(f"Error from {model} API: {response.status_code} - {response.text}")
                responses[model] = f"Error: {response.status_code}"

        return responses

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Ensure this block only runs when the script is executed directly
if __name__ == "__main__":
    img_path = "abc.jpg"  # Replace with your actual image path
    query = "Describe this image"
    result = process_image(img_path, query)
    print(result)
