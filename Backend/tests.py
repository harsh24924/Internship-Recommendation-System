import pytest
from main import app
from schemas import Internship
from fastapi.testclient import TestClient

client = TestClient(app)

def test_success():
    mock_resume = mock_resume = {
            "summary": "Enthusiastic and creative recent Graphic Design graduate with a strong portfolio showcasing expertise in visual communication, branding, and digital media. Eager to apply design principles and software proficiency to deliver impactful visual solutions in a dynamic environment.",
            "skills": "Proficient in Adobe Creative Suite (Photoshop, Illustrator, InDesign, After Effects, Premiere Pro), Figma, Sketch, Canva. Strong understanding of typography, color theory, layout design, branding, and web design principles. Experienced in digital illustration, motion graphics, and UI/UX basics.",
            "education": "Bachelor of Fine Arts in Graphic Design from Rhode Island School of Design, Providence, RI (Graduated: May 2023).",
            "projects": "Designed comprehensive brand identity for a local startup, including logo, style guide, and marketing collateral. Developed UI/UX mockups and interactive prototypes for a mobile application concept. Created a series of animated social media campaigns for a non-profit organization.",
            "experience": "Graphic Design Intern at Creative Solutions Agency (Summer 2022), assisting with client projects, brand development, and digital content creation. Freelance Graphic Designer (2021-Present), collaborating with small businesses on website graphics, print materials, and social media assets.",
            "certifications": "Adobe Certified Professional in Graphic Design & Illustration Using Adobe Illustrator."
        }

    response = client.post("/recommend/", json = mock_resume)
    internships = response.json()

    for internship in internships:
        print(internship["title"])

    assert response.status_code == 200
    assert isinstance(internships, list)

    for internship in internships:
        try:
            Internship(**internship)
        except Exception as e:
            pytest.fail(f"An item in the response list failed Pydantic validation: {e}")
