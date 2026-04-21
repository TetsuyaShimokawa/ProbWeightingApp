from pydantic import BaseModel, field_validator
from typing import Optional


class SessionStartRequest(BaseModel):
    student_id: str
    name: str


class TrialResult(BaseModel):
    session_id: str
    student_id: str
    name: str
    trial: int
    block: int
    N: int
    p: float
    q: float
    r: float
    x: float
    x_prime: float
    y: float
    s: float
    y_prime: float
    pN: float
    qN: float
    rN: float
    sN: float
    choice: str  # "X" / "Indifferent" / "Y"
    ci_satisfied: bool

    @field_validator("choice")
    @classmethod
    def validate_choice(cls, v: str) -> str:
        if v not in {"X", "Indifferent", "Y"}:
            raise ValueError("choice must be one of: X, Indifferent, Y")
        return v
