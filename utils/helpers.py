from datetime import datetime
from typing import Optional
import uuid


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def gen_id() -> str:
    return str(uuid.uuid4())


def safe_get(d: dict, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
    return d if d is not None else default
