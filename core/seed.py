from sqlalchemy.orm import Session
from core.models import SPrompt, Template

PROMPTS = [
    {"name": "Intent Classifier", "category": "pipeline", "content": "You are an intent classifier..."},
    {"name": "Architecture Planner", "category": "pipeline", "content": "You are a website architecture planner..."},
]

TEMPLATES = [
    {"name": "SaaS Landing", "category": "landing", "description": "Modern SaaS landing page", "content": "<!DOCTYPE html>..."},
]

def seed_db(db: Session):
    if db.query(SPrompt).count() == 0:
        for p in PROMPTS:
            db.add(SPrompt(**p))
        db.commit()
    if db.query(Template).count() == 0:
        for t in TEMPLATES:
            db.add(Template(**t))
        db.commit()
