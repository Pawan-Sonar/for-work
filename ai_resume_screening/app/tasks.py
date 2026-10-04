import os

from celery import Celery

from .database import SessionLocal
from .models import Resume
from .skill_engine import extract_skills, extract_text, make_json_list


celery_app = Celery(
    "resume_tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)


@celery_app.task(name="process_resume")
def process_resume(resume_id: int, file_path: str) -> None:
    db = SessionLocal()
    resume = None
    try:
        resume = db.get(Resume, resume_id)
        if not resume:
            return
        resume.status = "processing"
        db.commit()
        text = extract_text(file_path)
        resume.raw_text = text
        resume.extracted_skills = make_json_list(extract_skills(text))
        resume.status = "ready"
        db.commit()
    except Exception:
        if resume:
            resume.status = "failed"
            db.commit()
        raise
    finally:
        db.close()
