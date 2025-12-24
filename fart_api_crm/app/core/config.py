from __future__ import annotations
import os

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://student:stud_secret@localhost:5432/proxy"
)