from dataclasses import dataclass

@dataclass
class SolveResult:
    n: int
    solver: str
    status: str
    elapsed_seconds: float
    solution: list[int] | None
    valid: bool | None
    variables: int | None = None
    constraints: int | None = None
    message: str | None = None
