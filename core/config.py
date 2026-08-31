import os

try:
    import streamlit as st
    _in_streamlit = True
except ImportError:
    _in_streamlit = False


def _get(key, default=None):
    if _in_streamlit:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except Exception:
            return os.getenv(key, default)
    return os.getenv(key, default)


class Settings:
    DATABASE_URL = _get("DATABASE_URL", "sqlite:///./builder.db")
    ENCRYPTION_KEY = _get("ENCRYPTION_KEY", "")
    JWT_SECRET = _get("JWT_SECRET", "change-me-in-production-32-char-min")
    JWT_ALGO = "HS256"
    JWT_EXPIRE_DAYS = 7
    OPENAI_KEY = _get("OPENAI_API_KEY", "")
    APP_NAME = "Agentic Builder"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
