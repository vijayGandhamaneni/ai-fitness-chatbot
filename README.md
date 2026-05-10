# AI Fitness Chatbot (RAG + LLM)

An AI-powered fitness chatbot built using FastAPI, embedding-based RAG, FAISS vector search, and LLaMA 3.1 via Groq API.

## Features

- AI Fitness Chatbot
- Embedding-based RAG
- Semantic Search using FAISS
- LLM Integration (Groq + LLaMA 3.1)
- JSON-based responses
- Frontend + Backend integration
- CSV-based fitness knowledge base

---

## Tech Stack

- Python
- FastAPI
- Groq API
- LLaMA 3.1
- Sentence Transformers
- FAISS
- HTML/CSS/JavaScript

---

## Project Structure

```bash
ai-fitness-chatbot/
│
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── prompts.py
│   ├── models.py
│
├── data/
│   └── fitness_data.csv
│
├── frontend/
│   └── index.html
│
├── requirements.txt
├── .env
├── README.md
```

---

## How It Works

1. User enters fitness query
2. Query converted into embeddings
3. FAISS retrieves semantically relevant fitness data
4. Retrieved context passed into prompt
5. LLM generates structured fitness response
6. Response displayed in frontend

---

## Sample Query

```json
{
  "query": "I have knee pain and obesity"
}
```

---

## Sample Output

```json
{
  "condition": "knee pain and obesity",
  "recommended_exercises": [
    "Walking",
    "Cycling"
  ],
  "precautions": [
    "Avoid running",
    "Start with low impact exercises"
  ]
}
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

---

## API Docs

```bash
http://127.0.0.1:8000/docs
```

---

## Future Improvements

- PDF knowledge base support
- Better UI
- Multi-turn conversation memory
- Real-time fitness tracking


## Author

Vijay Kiran Chowdary Gandhamaneni
AI Intern  | FastAPI | LLMs | RAG  

GitHub: https://github.com/vijayGandhamaneni