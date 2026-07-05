"""Eval fixture — redundant Depends for PR review eval."""
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    return {}


@router.get("/")
def list_users(db=Depends(get_db)):
    return []
