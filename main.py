from fastapi import FastAPI
from pydantic import BaseModel
from app.text_processing import recommend_jobs 

app = FastAPI()


class Candidate(BaseModel):
    name: str
    skills: list[str]
    experience: float | None = None
    education: str | None = None
    location: str | None = None
    preferred_role: str | None = None
    summary: str | None = None

class Job(BaseModel):
    title: str
    company: str
    description: str
    required_skills: list[str]
    mandatory_skills: list[str] = []
    min_experience: float | None = None
    education: str | None = None
    location: str | None = None
    remote_type: str | None = None


@app.get("/")
def home():
    return {"message": "Job Recommendation API is running"}


@app.post("/recommend")
def recommend(candidate: Candidate, jobs: list[Job]):

    candidate_data = candidate.model_dump()

    jobs_data = [
        job.model_dump()
        for job in jobs
    ]

    recommendations = recommend_jobs(
        candidate_data,
        jobs_data
    )

    return {
        "recommendations": recommendations
    }