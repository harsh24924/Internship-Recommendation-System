# Internship Recommendation System

## Descriptions
Uses text embeddings and cosine similarity to find the best internships for a resume.

## Setup
1. Install dependencies: `pip install pytest fastapi python-dotenv sentence-transformers numpy pydantic httpx uvicorn`
2. Process the internships. This needs to be done only once: `python populate.py`
3. Navigate to the backend directory and start the server: `uvicorn api:app --reload`
