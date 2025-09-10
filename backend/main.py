import os
import json
import numpy
from typing import List
from fastapi import FastAPI
from engine import Recommend
from dotenv import load_dotenv
# from fastapi.staticfiles import StaticFiles
from schemas import Resume, RecommendedInternship
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import CrossEncoder, SentenceTransformer

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
internships = json.load(open(os.getenv("INTERNSHIPS_JSON_FILE_PATH", "Data/internships.json")))
all_internship_vectors = numpy.load(os.getenv("INTERSHIPS_NUMPY_FILE_PATH", "Data/internships.npy"))
cross_encoding_model = CrossEncoder(os.getenv("CROSS_ENCODER_ID", "cross-encoder/ms-marco-MiniLM-L6-v2"))
embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL_ID", "sentence-transformers/all-mpnet-base-v2"))

recommend = Recommend()

@app.post("/recommend/", response_model = List[RecommendedInternship])
def get_recommendations(resume: Resume) -> List[RecommendedInternship]:
    resume_vectors = recommend.encode_resume(resume, embedding_model)
    scores = recommend.compare(resume_vectors, all_internship_vectors)
    recommendations = recommend.get_top_matches(scores, recommendation_count, internships)
    reranked_recommendations = recommend.rerank(resume, cross_encoding_model, recommendations)
    return reranked_recommendations

# app.mount("/", StaticFiles(directory = "../ui", html = True), name = "ui")
