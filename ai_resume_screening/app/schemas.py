from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=20)


class JobResponse(BaseModel):
    id: int
    title: str
    extracted_skills: list[str]


class ResumeResponse(BaseModel):
    id: int
    filename: str
    status: str
    extracted_skills: list[str]


class MatchResponse(BaseModel):
    resume_id: int
    job_id: int
    similarity_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    interview_questions: list[str]
