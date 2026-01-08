"""API router package for InsureMate.

Move endpoint routers here (e.g. predict, results) and include them in the
application in `insuremate/main.py`.
"""

from fastapi import APIRouter

router = APIRouter()

__all__ = ["router"]
