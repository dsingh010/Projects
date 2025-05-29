# 🤖 Simple QA Agent API with LangChain, FastAPI, and Docker

This project is a lightweight AI-powered question-answering API built using [LangChain](https://github.com/langchain-ai/langchain), [OpenAI](https://platform.openai.com/), [FastAPI](https://fastapi.tiangolo.com/), and Docker. It lets users ask natural language questions and receive answers powered by a LangChain agent connected to the OpenAI API.

---

## 📦 Features

- 🧠 LangChain agent wrapping OpenAI’s LLM
- ⚡️ FastAPI backend with a `/ask` endpoint
- 🐳 Dockerized for cross-platform deployment
- 🔐 Environment variable support for secure API key management
- 🧪 Local testing with `curl`

---

## 🚀 Project Guide

### 1. Clone the Repository

git clone https://github.com/your-username/simple-agent-api.git
cd simple-agent-api

2. Set Up and Run the App

  # Step 1: Set your OpenAI API key
  # Replace with your actual key in the line below or in the Docker run command
  export OPENAI_API_KEY=sk-...
  
  # Step 2: Build the Docker image
  docker build -t simple-agent .
  
  # Step 3: Run the container with the key passed securely
  docker run -d -p 8000:8000 --env OPENAI_API_KEY=OPENAI_API_KEY simple-agent
  
  3. Test the API Endpoint
  curl -X POST "http://localhost:8000/ask" \
    -H "Content-Type: application/json" \
    -d '{"question": "What is AI?"}'
  
  Expected response:
  {
    "answer": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines..."
  }
