from __future__ import annotations


def validate_n(n: int) -> None:
    if not isinstance(n, int) or n < 1:
        raise ValueError("N must be an integer >= 1")


def validate_solution(placement: list[int] | None, n: int) -> bool:
    if placement is None or len(placement) != n:
        return False
    if any(not isinstance(c, int) or c < 0 or c >= n for c in placement):
        return False
    return (len(set(placement)) == n
            and len({r - placement[r] for r in range(n)}) == n
            and len({r + placement[r] for r in range(n)}) == n)


def render_board(placement: list[int]) -> str:
    n = len(placement)
    return "\n".join(" ".join("Q" if placement[r] == c else "." for c in range(n)) for r in range(n))
