import os
import json
import numpy
from typing import List
from fastapi import FastAPI
from engine import Recommend
from dotenv import load_dotenv
from schemas import Resume, Internship
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
    
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_origins = origins,
    allow_credentials = True
    
)

recommendation_count = int(os.getenv("RECOMMENDATION_COUNT", "5"))
model = SentenceTransformer(os.getenv("MODEL_ID", "sentence-transformers/all-mpnet-base-v2"))
internships = json.load(open(os.getenv("INTERNSHIPS_JSON_FILE_PATH", "Data/internships.json")))
all_internship_vectors = numpy.load(os.getenv("INTERSHIPS_NUMPY_FILE_PATH", "Data/internships.npy"))

recommend = Recommend()

@app.post("/recommend/", response_model = List[Internship])
def get_recommendations(resume: Resume) -> List[Internship]:
    resume_vectors = recommend.encode_resume(resume, model)
    scores = recommend.compare(resume_vectors, all_internship_vectors)
    recommendations = recommend.get_top_matches(scores, recommendation_count, internships)
    return recommendations
