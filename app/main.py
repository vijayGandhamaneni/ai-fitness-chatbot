from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from groq import Groq
from dotenv import load_dotenv

import os

from app.models import ChatRequest
from app.rag import retrieve_context
from app.prompts import create_prompt

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


@app.get("/")
def home():
    return {
        "message": "AI Fitness Chatbot API Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Step 1: User Query
    user_query = request.query

    # Step 2: Retrieve Context from RAG
    retrieved_context = retrieve_context(user_query)

    # Step 3: Create Prompt
    prompt = create_prompt(user_query, retrieved_context)

    try:

        # Step 4: LLM Call
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI fitness coach."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Step 5: Extract Output
        llm_output = response.choices[0].message.content

        # Step 6: Return Response
        return {
            "query": user_query,
            "retrieved_context": retrieved_context,
            "response": llm_output
        }

    except Exception as e:

        return {
            "error": str(e)
        }