# 📖 Study Assistant API

A FastAPI backend that proxies requests to OpenAI's API to generate study materials from any text input. Built with Python and deployed on Railway.

**Live API:** https://study-assistant-api-production.up.railway.app
**Frontend:** https://github.com/Lunaris47/study-assistant

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.14 |
| Framework | FastAPI |
| Server | Uvicorn |
| AI | OpenAI API (gpt-4o-mini) |
| Deployment | Railway |

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/summarize` | Generate a summary of the provided text |
| POST | `/api/flashcards` | Generate flashcard question/answer pairs |
| POST | `/api/quiz` | Generate multiple choice quiz questions |

All three POST endpoints accept the same request body:

```json
{
  "text": "Your text here..."
}
```

### Example responses

**`/api/summarize`**
```json
{
  "summary": "Photosynthesis is the process by which plants..."
}
```

**`/api/flashcards`**
```json
{
  "flashcards": [
    { "question": "What is photosynthesis?", "answer": "The process by which plants..." },
    { "question": "Where does photosynthesis occur?", "answer": "In the chloroplasts..." }
  ]
}
```

**`/api/quiz`**
```json
{
  "quiz": [
    {
      "question": "What do plants produce during photosynthesis?",
      "options": ["Oxygen and sugar", "Carbon dioxide", "Nitrogen", "Water"],
      "answer": "Oxygen and sugar"
    }
  ]
}
```

---

## Running Locally

### Prerequisites
- Python 3.12+
- An OpenAI API key (get one at https://platform.openai.com)

### Setup

1. Clone the repo:
```bash
git clone https://github.com/Lunaris47/study-assistant-api.git
cd study-assistant-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root:
```
OPENAI_API_KEY=sk-your-key-here
```

5. Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## Project Structure

```
study-assistant-api/
├── main.py            # FastAPI app with all endpoints
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (gitignored)
└── .gitignore
```

---

## Related

- **Frontend:** [Study Assistant Web App](https://study-assistant-seven-sooty.vercel.app) — React frontend deployed on Vercel

---

## Author

Jesse Sciamanna — [GitHub](https://github.com/Lunaris47) | [LinkedIn](https://www.linkedin.com/in/JesseSciam)
