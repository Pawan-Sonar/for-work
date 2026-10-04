import os
import shutil
import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import JobDescription, MatchResult, Resume
from .schemas import JobCreate, JobResponse, MatchResponse, ResumeResponse
from .skill_engine import (
    extract_skills,
    generate_questions,
    make_json_list,
    parse_json_list,
    semantic_similarity,
)
from .tasks import process_resume


UPLOAD_DIRECTORY = Path(os.getenv("UPLOAD_DIRECTORY", "uploads"))
UPLOAD_DIRECTORY.mkdir(exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screening & Job Matching Platform")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    skills = extract_skills(job.description)
    record = JobDescription(
        title=job.title,
        description=job.description,
        extracted_skills=make_json_list(skills),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return JobResponse(id=record.id, title=record.title, extracted_skills=skills)


@app.get("/jobs", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobDescription).order_by(JobDescription.created_at.desc()).all()
    return [JobResponse(id=job.id, title=job.title, extracted_skills=parse_json_list(job.extracted_skills)) for job in jobs]


@app.post("/resumes", response_model=ResumeResponse)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        raise HTTPException(status_code=400, detail="Upload a PDF or DOCX resume.")

    stored_filename = f"{uuid.uuid4()}{suffix}"
    target = UPLOAD_DIRECTORY / stored_filename
    with target.open("wb") as output:
        shutil.copyfileobj(file.file, output)

    resume = Resume(original_filename=file.filename or stored_filename, stored_filename=stored_filename)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    process_resume.delay(resume.id, str(target))
    return ResumeResponse(id=resume.id, filename=resume.original_filename, status=resume.status, extracted_skills=[])


@app.get("/resumes", response_model=list[ResumeResponse])
def list_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).order_by(Resume.created_at.desc()).all()
    return [
        ResumeResponse(
            id=resume.id,
            filename=resume.original_filename,
            status=resume.status,
            extracted_skills=parse_json_list(resume.extracted_skills),
        )
        for resume in resumes
    ]


@app.post("/matches", response_model=MatchResponse)
def create_match(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    job = db.get(JobDescription, job_id)
    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or job description not found.")
    if resume.status != "ready":
        raise HTTPException(status_code=409, detail="Resume is still being processed.")

    resume_skills = set(parse_json_list(resume.extracted_skills))
    job_skills = set(parse_json_list(job.extracted_skills))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    skill_score = len(matched) / len(job_skills) if job_skills else 0
    embedding_score = semantic_similarity(resume.raw_text or "", job.description)
    similarity = round(((skill_score * 0.6) + (embedding_score * 0.4)) * 100, 2)
    questions = generate_questions(matched, missing)
    result = MatchResult(
        resume_id=resume.id,
        job_id=job.id,
        similarity_score=similarity,
        matched_skills=make_json_list(matched),
        missing_skills=make_json_list(missing),
        interview_questions=make_json_list(questions),
    )
    db.add(result)
    db.commit()
    return MatchResponse(
        resume_id=resume.id,
        job_id=job.id,
        similarity_score=similarity,
        matched_skills=matched,
        missing_skills=missing,
        interview_questions=questions,
    )
