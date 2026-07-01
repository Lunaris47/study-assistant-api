# ===============================
# STUDY ASSISTANT API
# FastAPI backend that proxies requests to OpenAI
# and returns summaries, flashcards, and quizzes.
# ===============================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===============================
# CORS CONFIGURATION
# Allows the React frontend to call this API
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://study-assistant-seven-sooty.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===============================
# REQUEST MODELS
# ===============================

class TextInput(BaseModel):
    """Request body containing the text to analyze."""
    text: str


# ===============================
# HEALTH CHECK
# ===============================

@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "Study Assistant API is running"}


# ===============================
# SUMMARY ENDPOINT
# ===============================

@app.post("/api/summarize")
async def summarize(input: TextInput):
    """
    Generates a concise summary of the provided text.
    Returns a plain text summary of the key points.
    """
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful study assistant. Summarize the provided text concisely, highlighting the most important concepts and key points. Use clear, student-friendly language."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text:\n\n{input.text}"
                }
            ],
            max_tokens=500
        )
        return {"summary": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# FLASHCARDS ENDPOINT
# ===============================

@app.post("/api/flashcards")
async def flashcards(input: TextInput):
    """
    Generates a list of flashcards from the provided text.
    Returns a JSON array of {question, answer} objects.
    """
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful study assistant. Generate flashcards from the provided text.
Return ONLY a valid JSON array with no extra text, markdown, or explanation.
Each flashcard must have exactly two fields: "question" and "answer".
Example format:
[
  {"question": "What is X?", "answer": "X is..."},
  {"question": "What is Y?", "answer": "Y is..."}
]
Generate between 5 and 10 flashcards."""
                },
                {
                    "role": "user",
                    "content": f"Generate flashcards from the following text:\n\n{input.text}"
                }
            ],
            max_tokens=1000
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        flashcard_list = json.loads(raw)
        return {"flashcards": flashcard_list}

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse flashcards from AI response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# QUIZ ENDPOINT
# ===============================

@app.post("/api/quiz")
async def quiz(input: TextInput):
    """
    Generates multiple choice quiz questions from the provided text.
    Returns a JSON array of {question, options, answer} objects.
    """
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful study assistant. Generate multiple choice quiz questions from the provided text.
Return ONLY a valid JSON array with no extra text, markdown, or explanation.
Each question must have exactly three fields:
- "question": the question text
- "options": an array of exactly 4 answer choices (strings)
- "answer": the correct answer (must exactly match one of the options)
Example format:
[
  {
    "question": "What is X?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }
]
Generate between 5 and 8 questions."""
                },
                {
                    "role": "user",
                    "content": f"Generate quiz questions from the following text:\n\n{input.text}"
                }
            ],
            max_tokens=1500
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        quiz_list = json.loads(raw)
        return {"quiz": quiz_list}

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse quiz from AI response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))