import base64
from cryptography.fernet import Fernet
from core.config import settings

_fernet = None

def get_enc():
    global _fernet
    if _fernet is None:
        key = settings.ENCRYPTION_KEY
        if not key:
            # Generate a temporary key (not for production)
            key = Fernet.generate_key().decode()
        if isinstance(key, str):
            key = key.encode()
        # Ensure 32-byte url-safe base64
        try:
            _fernet = Fernet(key)
        except Exception:
            key = base64.urlsafe_b64encode(key.ljust(32)[:32])
            _fernet = Fernet(key)
    return _fernet

def encrypt(text: str) -> str:
    if not text:
        return ""
    return get_enc().encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    if not token:
        return ""
    try:
        return get_enc().decrypt(token.encode()).decode()
    except Exception:
        return ""
