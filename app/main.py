from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from groq import Groq

from app.models import ChatRequest
from app.query_classifier import classify_query
from app.rag import retrieve_context
from app.diet_rag import retrieve_diet_context
from app.prompts import create_prompt

import pandas as pd
import os
import json


# Load Environment Variables

load_dotenv()

# Load CSV Files

exercise_df = pd.read_csv(
    "data/cleaned_fitness_data.csv"
)

diet_df = pd.read_csv(
    "data/cleaned_diet_data.csv"
)

# Initialize Groq Client

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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

# Home Route

@app.get("/")
def home():

    return {

        "message":
            "AI Fitness Assistant API Running"
    }

# Dynamic Parameter Extraction

def extract_parameters(message):

    message = message.lower()

    # Spelling Normalization

    spelling_map = {

        "ancle": "ankle",
        "sholder": "shoulder",
        "wrsit": "wrist",
        "rehablitation": "rehabilitation"
    }

    for wrong, correct in spelling_map.items():

        message = message.replace(
            wrong,
            correct
        )

    # Initialize Parameters

    extracted = {

        # Exercise Parameters

        "condition": None,
        "exercise": None,
        "precaution": None,
        "goal": None,
        "difficulty": None,
        "steps": None,

        # Diet Parameters

        "diet_type": None,
        "foods": None,
        "avoid": None,
        "hydration": None,
        "meal_tip": None
    }

    # Searchable Exercise Columns

    exercise_columns = [

        "condition",
        "exercise",
        "precaution",
        "goal",
        "difficulty",
        "steps"
    ]

    # Searchable Diet Columns

    diet_columns = [

        "goal",
        "condition",
        "diet_type",
        "foods",
        "avoid",
        "hydration",
        "meal_tip"
    ]

    # Extract Exercise Parameters

    for column in exercise_columns:

        unique_values = exercise_df[column] \
            .dropna() \
            .astype(str) \
            .str.lower() \
            .unique()

        for value in unique_values:

            if value in message:

                extracted[column] = value

    # Extract Diet Parameters

    for column in diet_columns:

        unique_values = diet_df[column] \
            .dropna() \
            .astype(str) \
            .str.lower() \
            .unique()

        for value in unique_values:

            if value in message:

                extracted[column] = value

    return extracted

# Chat Endpoint

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # User Inputs

        user_message = request.message

        chat_history = request.chat_history

        # Extract Parameters

        extracted = extract_parameters(
            user_message
        )
        
        # Detect Intent

        intent = classify_query(
            user_message
        )

        print("\nDetected Intent:", intent)

        # Conversational Memory

        if chat_history:

            history_text = ""

            for item in chat_history:

                if hasattr(item, "content"):

                    history_text += item.content + " "

                elif isinstance(item, dict):

                    history_text += item.get(
                        "content",
                        ""
                    ) + " "

            previous_extracted = extract_parameters(
                history_text
            )

            for key in extracted:

                if not extracted[key]:

                    extracted[key] = previous_extracted[key]

        print("\nExtracted Parameters:")

        for key, value in extracted.items():

            print(f"{key}: {value}")

        # Initialize Retrieval Results

        retrieved_context = []

        diet_context = []

        # Exercise Retrieval

        if intent == "exercise":

            retrieved_context = retrieve_context(

                query=user_message,

                extracted=extracted,

            )

        # Diet Retrieval

        elif intent == "diet":

            diet_context = retrieve_diet_context(

                query=user_message,

                extracted=extracted,

            )

        # Both Retrieval

        elif intent == "both":

            retrieved_context = retrieve_context(

                query=user_message,

                extracted=extracted,

            )

            diet_context = retrieve_diet_context(

                query=user_message,

                extracted=extracted,

            )

        # General Routing

        else:
    
            retrieved_context = []

            diet_context = []

        # Create Prompt

        prompt = create_prompt(

            user_message=user_message,

            chat_history=chat_history,

            retrieved_context=retrieved_context,

            diet_context=diet_context,

            intent=intent
        )


        # LLM Call

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        llm_output = response.choices[0].message.content

        # Parse Response

        try:

            response_data = json.loads(
                llm_output
            )

        except Exception:

            response_data = {

                "assistant_response":

                    "I found some recommendations based on your request.",

                "safety_guidance":

                    "Please exercise carefully and listen to your body."
            }

        # Final Response

        return {

            "message": user_message,

            "intent": intent,

            "parameters": extracted,

            "retrieved_context": retrieved_context,

            "diet_context": diet_context,

            "response": response_data
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {

            "error": str(e)
        }