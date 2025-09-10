import numpy
from typing import List
from schemas import Resume, Internship, RecommendedInternship
from sentence_transformers import CrossEncoder, SentenceTransformer


def calculate_cosine_similarity(vector1: numpy.ndarray, vector2: numpy.ndarray) -> float:
    dot_product = numpy.dot(vector1, vector2)

    norm_vector1 = numpy.linalg.norm(vector1)
    norm_vector2 = numpy.linalg.norm(vector2)

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

    weights = {
        "skills_requirements": 0.25,
        "experience_description": 0.20,
        "projects_description": 0.15,
        "experience_requirements": 0.10,
        "skills_description": 0.10,
        "summary_description": 0.05,
        "summary_title": 0.05,
        "education_requirements": 0.05,
        "certifications_requirements": 0.04,
        "certifications_description": 0.01
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
                (score1 * self.weights["skills_requirements"]) +
                (score2 * self.weights["experience_description"]) +
                (score3 * self.weights["projects_description"]) +
                (score4 * self.weights["experience_requirements"]) +
                (score5 * self.weights["skills_description"]) +
                (score6 * self.weights["summary_description"]) +
                (score7 * self.weights["summary_title"]) +
                (score8 * self.weights["education_requirements"]) +
                (score9 * self.weights["certifications_requirements"]) +
                (score10 * self.weights["certifications_description"])
            )

            scores.append(score)

        return numpy.array(scores)

    def get_top_matches(self, scores: numpy.ndarray, recommendation_count: int, internships: List[Internship]) -> List[Internship]:
        top_indices = numpy.argsort(scores)[-recommendation_count:][::-1]
        recommendations = [internships[i] for i in top_indices]
        return recommendations

    def rerank(self, resume: Resume, cross_encoder: CrossEncoder, recommendations: List[Internship]) -> List[RecommendedInternship]:

        for i, internship in enumerate(recommendations):
            scores = cross_encoder.predict([
                (resume.skills, internship["requirements"]),
                (resume.experience, internship["description"]),
                (resume.projects, internship["description"]),
                (resume.experience, internship["requirements"]),
                (resume.skills, internship["description"]),
                (resume.summary, internship["description"]),
                (resume.summary, internship["title"]),
                (resume.education, internship["requirements"]),
                (resume.certifications, internship["requirements"]),
                (resume.certifications, internship["description"])
            ])

            weighted_score = (
                (scores[0] * self.weights["skills_requirements"]) +
                (scores[1] * self.weights["experience_description"]) +
                (scores[2] * self.weights["projects_description"]) +
                (scores[3] * self.weights["experience_requirements"]) +
                (scores[4] * self.weights["skills_description"]) +
                (scores[5] * self.weights["summary_description"]) +
                (scores[6] * self.weights["summary_title"]) +
                (scores[7] * self.weights["education_requirements"]) +
                (scores[8] * self.weights["certifications_requirements"]) +
                (scores[9] * self.weights["certifications_description"])
            )

            recommendations[i]["score"] = weighted_score

        reranked_internships = sorted(recommendations, key = lambda x: x["score"], reverse = True)
        return reranked_internships[0:5]
