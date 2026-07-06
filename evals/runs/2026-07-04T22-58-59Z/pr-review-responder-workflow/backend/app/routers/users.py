"""Eval fixture — users list endpoint."""
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def list_users():
    return []
