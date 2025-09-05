import numpy
from typing import List
from schemas import Resume, Internship
from sentence_transformers import SentenceTransformer


def calculate_cosine_similarity(vector1: numpy.ndarray, vector2: numpy.ndarray) -> float:
    dot_product = numpy.dot(vector1, vector2)

    norm_vector1 = numpy.linalg.norm(vector1)
    norm_vector2 = numpy.linalg.norm(vector1)

    cosine_similarity = dot_product / (norm_vector1 * norm_vector2)
    return cosine_similarity


class Recommend:
    resume_mapping = {
        "summary": 0,
        "skills": 1,
        "education": 2,
        "projects": 3,
        "experience": 4,
        "certifications": 5
    }

    internship_mapping = {
        "title": 0,
        "description": 1,
        "requirements": 2
    }

    def encode_resume(self, resume: Resume, model: SentenceTransformer) -> numpy.ndarray:
        resume_details = list(resume.model_dump().values())
        resume_vectors = model.encode(resume_details)
        return resume_vectors

    def compare(self, resume_vectors: numpy.ndarray, all_internship_vectors: numpy.ndarray) -> numpy.ndarray:
        scores = []

        for internship_vectors in all_internship_vectors:
            score1 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["skills"]], internship_vectors[self.internship_mapping["requirements"]])
            score2 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["experience"]], internship_vectors[self.internship_mapping["description"]])
            score3 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["projects"]], internship_vectors[self.internship_mapping["description"]])
            score4 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["experience"]], internship_vectors[self.internship_mapping["requirements"]])
            score5 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["skills"]], internship_vectors[self.internship_mapping["description"]])
            score6 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["summary"]], internship_vectors[self.internship_mapping["description"]])
            score7 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["summary"]], internship_vectors[self.internship_mapping["title"]])
            score8 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["education"]], internship_vectors[self.internship_mapping["requirements"]])
            score9 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["certifications"]], internship_vectors[self.internship_mapping["requirements"]])
            score10 = calculate_cosine_similarity(resume_vectors[self.resume_mapping["certifications"]], internship_vectors[self.internship_mapping["description"]])

            score = (
                (score1 * 0.25) +
                (score2 * 0.20) +
                (score3 * 0.15) +
                (score4 * 0.10) +
                (score5 * 0.10) +
                (score6 * 0.05) +
                (score7 * 0.05) +
                (score8 * 0.05) +
                (score9 * 0.04) +
                (score10 * 0.01)
            )

            scores.append(score)

        return numpy.array(scores)

    def get_top_matches(self, scores: numpy.ndarray, recommendation_count: int, internships: List[Internship]) -> List[Internship]:
        top_indices = numpy.argsort(scores)[-recommendation_count:][::-1]
        recommendations = [internships[i] for i in top_indices]
        return recommendations
