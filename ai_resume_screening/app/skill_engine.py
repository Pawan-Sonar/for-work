import json
import re

from docx import Document
from pypdf import PdfReader


SKILL_VOCABULARY = {
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "html", "css",
    "fastapi", "django", "flask", "react", "node.js", "angular", "vue", "spring boot",
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "docker", "kubernetes", "aws",
    "azure", "gcp", "git", "github", "linux", "rest api", "graphql", "microservices",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning",
    "deep learning", "nlp", "data analysis", "power bi", "tableau", "excel", "agile",
    "scrum", "figma", "ui/ux", "testing", "pytest", "selenium", "ci/cd"
}

_embedding_model = None


def extract_text(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    if path.lower().endswith(".docx"):
        return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)
    raise ValueError("Only PDF and DOCX resumes are supported.")


def extract_skills(text: str) -> list[str]:
    searchable_text = text.lower()
    found = []
    for skill in SKILL_VOCABULARY:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, searchable_text):
            found.append(skill)
    return sorted(found)


def parse_json_list(value: str | None) -> list[str]:
    return json.loads(value) if value else []


def make_json_list(items: list[str]) -> str:
    return json.dumps(sorted(set(items)))


def generate_questions(matched_skills: list[str], missing_skills: list[str]) -> list[str]:
    questions = [
        f"Tell us about a project where you used {skill}. What was your contribution?"
        for skill in matched_skills[:5]
    ]
    questions.extend(
        f"How would you approach learning and applying {skill} for this role?"
        for skill in missing_skills[:3]
    )
    return questions or ["Walk us through a recent project that best represents your skills."]


def semantic_similarity(resume_text: str, job_text: str) -> float:
    """Return cosine similarity from a compact sentence-transformer embedding model."""
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = _embedding_model.encode([resume_text, job_text], normalize_embeddings=True)
    return float(embeddings[0] @ embeddings[1])
