# AI Resume Screening & Job Matching Platform

This FastAPI platform accepts resumes in PDF or DOCX format, extracts skills, compares candidates with job descriptions, calculates a skill-similarity score, identifies missing skills, and generates tailored interview questions.

## Technology

- FastAPI API and browser dashboard
- PostgreSQL persistence
- Redis and Celery background workers for resume processing
- PDF/DOCX text extraction
- NLP embeddings from `sentence-transformers` plus an explainable skill-coverage score

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Open `http://localhost:8000` for the dashboard or `http://localhost:8000/docs` for API documentation.

## Local development

For a lightweight demo without Docker, leave `DATABASE_URL` unset to use SQLite. Run a Redis server, install the dependencies, start the worker with `celery -A app.tasks.celery_app worker --loglevel=info`, then start FastAPI with `uvicorn app.main:app --reload`.

## How scoring works

The final match score combines 60% job-skill coverage and 40% semantic similarity from the `all-MiniLM-L6-v2` sentence-transformer model. The first match download fetches the model automatically. This keeps the score meaningful while clearly showing the candidate's matched and missing skills.
