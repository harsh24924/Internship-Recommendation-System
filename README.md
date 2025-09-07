# Internship Recommendation System

## Descriptions
Uses text embeddings and cosine similarity to find the best internships for a resume.

## Setup
1. Install Python dependencies: `pip install pytest fastapi python-dotenv sentence-transformers numpy pydantic httpx uvicorn`
2. Install NPM packages: `npm install`
2. Process the internships. This needs to be done only once: `python populate.py`
3. Start the backend server: `uvicorn main:app --reload`
4. Start the React server: `npm start`
