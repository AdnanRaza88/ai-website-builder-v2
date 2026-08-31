import base64
from cryptography.fernet import Fernet
from core.config import settings


def _get_fernet():
    key = settings.ENCRYPTION_KEY
    if not key:
        key = Fernet.generate_key().decode()
    if isinstance(key, str):
        key = key.encode()
    # Pad/truncate to 32 bytes for Fernet
    key = base64.urlsafe_b64encode(key.ljust(32)[:32])
    return Fernet(key)


def encrypt(text: str) -> str:
    if not text:
        return ""
    f = _get_fernet()
    return f.encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    if not token:
        return ""
    try:
        f = _get_fernet()
        return f.decrypt(token.encode()).decode()
    except Exception:
        return ""
