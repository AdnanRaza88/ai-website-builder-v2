from datetime import datetime
from typing import Optional
import uuid

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def gen_id() -> str:
    return str(uuid.uuid4())

def mask_key(key: str) -> str:
    if not key or len(key) < 8:
        return "****"
    return key[:4] + "****" + key[-4:]

def fmt_dt(dt) -> str:
    if not dt:
        return "-"
    if isinstance(dt, str):
        return dt[:19]
    return dt.strftime("%Y-%m-%d %H:%M")

def status_color(status: str) -> str:
    colors = {
        "draft": "#94a3b8",
        "running": "#3b82f6",
        "done": "#22c55e",
        "error": "#ef4444",
        "pending": "#f59e0b",
    }
    return colors.get(status, "#94a3b8")

def safe_get(d: dict, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
    return d if d is not None else default
