from pydantic import BaseModel

class Resume(BaseModel):
    summary: str
    skills: str
    education: str
    projects: str
    experience: str
    certifications: str

class Internship(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: str
