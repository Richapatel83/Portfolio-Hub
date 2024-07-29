from enum import StrEnum
from typing import Optional, Any

from pydantic import BaseModel


class Proficiency(StrEnum):
    Novice = "Novice"
    Beginner = "Beginner"
    Intermediate = "Intermediate"
    Advanced = "Advanced"
    Expert = "Expert"


class Project(BaseModel):
    id: str = "p000"
    name: str
    description: Optional[str]
    github_repo: Optional[str]
    live_url: Optional[str]
    image: Optional[str]
    technologies: list[dict[int, str]] = []


class Technology(BaseModel):
    id: str = "t000"
    name: str
    description: Optional[str]
    proficiency: str = Proficiency.Novice
    image: Optional[str]
    visibility: bool = True
    projects: list[dict[int, str]] = []


def response(success: bool, message: str, data: Any = None) -> dict:
    """Returns a formatted response."""
    return {
        "success": success,
        "message": message,
        "data": data
    }
