import pytest
from main import app
from schemas import Internship
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def mock_resume():
    resume = {
        "summary": "Highly motivated and detail-oriented college graduate with a Bachelor's degree in Computer Science, passionate about building engaging and user-friendly web applications. Proficient in Angular, TypeScript, HTML, CSS, and modern frontend development practices. Seeking to leverage strong problem-solving skills and a collaborative spirit to contribute to innovative projects in a dynamic team environment.",
        "skills": "Angular, TypeScript, JavaScript, HTML5, CSS3 (SCSS/LESS), RxJS, NgRx/State Management, RESTful APIs, Git, Responsive Design, Angular Material, Jest/Karma/Jasmine, Agile/Scrum, Webpack, npm, VS Code, Problem Solving, Communication, Team Collaboration.",
        "education": "Bachelor of Science in Computer Science from State University, City, State (Graduated: May 2023). Relevant Coursework: Web Development, Data Structures, Algorithms, Object-Oriented Programming, Database Systems. Dean's List: 5 Semesters.",
        "projects": "E-commerce Platform (Personal Project): Developed a full-stack e-commerce application frontend using Angular, TypeScript, and RxJS for state management. Implemented responsive UI with Angular Material components. Integrated with a RESTful API for product catalog, user authentication, and shopping cart functionality. Achieved a 20% reduction in page load times through lazy loading and performance optimizations. Task Management Dashboard (Academic Project): Built a single-page application (SPA) for task management using Angular, focusing on a clean and intuitive user interface. Utilized component-based architecture and services for data handling. Implemented features like drag-and-drop task reordering and real-time updates using WebSockets (simulated). Enhanced user engagement by 15% through a streamlined task creation process.",
        "experience": "Junior Frontend Developer Intern at InnovateTech Solutions, City, State (May 2022 – August 2022): Contributed to the development of a customer-facing web application using Angular 14+, TypeScript, and SCSS. Collaborated with a team of 5 developers to implement new features and improve existing modules. Participated in daily stand-ups, sprint planning, and code reviews, adhering to Agile methodologies. Successfully refactored legacy components, reducing technical debt and improving maintainability by 10%.",
        "certifications": ""
    }


    yield resume

def test_success(mock_resume):
    response = client.post("/recommend/", json = mock_resume)
    internships = response.json()

    for internship in internships:
        print(internship["title"], internship["score"])
        print(internship["requirements"], "\n")

    assert response.status_code == 200
    assert isinstance(internships, list)

    for internship in internships:
        try:
            Internship(**internship)
        except Exception as e:
            pytest.fail(f"An item in the response list failed Pydantic validation: {e}")

def test_missing_field(mock_resume):
    del mock_resume["projects"]

    response = client.post("/recommend/", json = mock_resume)
    response_details = response.json()

    assert response.status_code == 422
    assert response_details["detail"][0]["type"] == "missing"
    assert response_details["detail"][0]["loc"] == ["body", "projects"]

def test_missing_json_payload():
    response = client.post("/recommend/")
    response_details = response.json()

    assert response.status_code == 422
    assert response_details["detail"][0]["type"] == "missing"
    assert response_details["detail"][0]["loc"] == ["body"]

def test_wrong_data_type(mock_resume):
    mock_resume["skills"] = ["C++", "Java"]
    response = client.post("/recommend/", json = mock_resume)
    response_details = response.json()

    assert response.status_code == 422
    assert response_details["detail"][0]["loc"] == ["body", "skills"]
    assert response_details["detail"][0]["msg"] == "Input should be a valid string"


def test_empty_field(mock_resume):
    mock_resume["skills"] = None
    response = client.post("/recommend/", json = mock_resume)
    response_details = response.json()

    assert response.status_code == 422
    assert response_details["detail"][0]["loc"] == ["body", "skills"]
    assert response_details["detail"][0]["msg"] == "Input should be a valid string"
