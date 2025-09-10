# Internship Recommendation System

## Descriptions
Uses Sentence Transformers and Cross Encoders to find the best internships for a resume.

## Setup
1. Install Python dependencies: `pip install pytest fastapi python-dotenv sentence-transformers numpy pydantic httpx uvicorn`
2. Process the internships. This needs to be done only once: `python process.py`
3. Start the backend server: `uvicorn main:app --reload`
