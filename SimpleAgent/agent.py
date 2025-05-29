from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import initialize_agent, Tool
from fastapi import FastAPI, HTTPException
import os

# Load API Key (optional, but better to get from environment variable)
os.environ['OPENAI_API_KEY'] = '<YOUR_OPENAI_KEY>'  # Replace or use dotenv
llm = OpenAI(temperature=0)

# Define QA Tool using LangChain
prompt = PromptTemplate.from_template("Answer the following question concisely and clearly: {input}")
qa_chain = LLMChain(llm=llm, prompt=prompt)

qa_tool = Tool(
    name="QA",
    func=lambda q: qa_chain.run(input=q), 
    description="Use this to answer general questions."
)

# Initialize the Agent
agent = initialize_agent(
    tools=[qa_tool],
    llm=llm,
    agent_type="zero-shot-react-description", 
    verbose=True
)

# Build FastAPI App
app = FastAPI()

@app.post("/ask")
def ask_question(payload: dict):
    question = payload.get('question')
    if not question:
        raise HTTPException(status_code=400, detail="Please include a 'question'")
    answer = agent.run(question)
    return {"answer": answer}
