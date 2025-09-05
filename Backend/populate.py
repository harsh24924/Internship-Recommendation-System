import os
import json
import numpy
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model_id = os.getenv("MODEL_ID", "sentence-transformers/all-mpnet-base-v2")
json_file_path = os.getenv("INTERNSIPS_JSON_FILE_PATH", "Data/internships.json")
numpy_file_path = os.getenv("INTERNSHIPS_NUMPY_FILE_PATH", "Data/internships.npy")

model = SentenceTransformer(model_id)
internships = json.load(open(json_file_path))

required_categories = ["title", "description", "requirements"]
filtered_internships = [[internship[category] for category in required_categories] for internship in internships]

all_internship_vectors = []
for filtered_internship in filtered_internships:
    filtered_internship_vectors = model.encode(filtered_internship)
    all_internship_vectors.append(filtered_internship_vectors)

all_internship_vectors_numpy = numpy.stack(all_internship_vectors, axis = 0)
numpy.save(numpy_file_path, all_internship_vectors_numpy)
