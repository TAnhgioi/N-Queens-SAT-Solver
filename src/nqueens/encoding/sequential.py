from __future__ import annotations
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from nqueens.problem import validate_n


def var_id(row: int, col: int, n: int) -> int:
    return row * n + col + 1


def add_amo(cnf: CNF, literals: list[int], encoding: str, top_id: int) -> int:
    if len(literals) <= 1:
        return top_id
    if encoding == "pairwise":
        cnf.extend([[-literals[i], -literals[j]] for i in range(len(literals)) for j in range(i + 1, len(literals))])
        return top_id
    if encoding == "sequential":
        result = CardEnc.atmost(lits=literals, bound=1, encoding=EncType.seqcounter, top_id=top_id)
        cnf.extend(result.clauses)
        return result.nv
    raise ValueError("encoding must be 'pairwise' or 'sequential'")


def build_cnf(n: int, encoding: str = "pairwise") -> CNF:
    validate_n(n)
    if encoding not in {"pairwise", "sequential"}:
        raise ValueError("encoding must be 'pairwise' or 'sequential'")
    cnf = CNF()
    top_id = n * n
    # Exactly one queen per row and column: ALO is one positive clause; AMO is selected encoding.
    for r in range(n):
        row = [var_id(r, c, n) for c in range(n)]
        cnf.append(row)
        top_id = add_amo(cnf, row, encoding, top_id)
    for c in range(n):
        col = [var_id(r, c, n) for r in range(n)]
        cnf.append(col)
        top_id = add_amo(cnf, col, encoding, top_id)
    diagonals: dict[tuple[int, int], list[int]] = {}
    for r in range(n):
        for c in range(n):
            v = var_id(r, c, n)
            diagonals.setdefault((r-c, 0), []).append(v)
            diagonals.setdefault((r+c, 1), []).append(v)
    for group in diagonals.values():
        top_id = add_amo(cnf, group, encoding, top_id)
    return cnf


def decode_solution(model: list[int], n: int) -> list[int]:
    positive = {lit for lit in model if lit > 0}
    result = []
    for r in range(n):
        cols = [c for c in range(n) if var_id(r, c, n) in positive]
        if len(cols) != 1:
            raise ValueError(f"Expected one queen in row {r}, found {len(cols)}")
        result.append(cols[0])
    return result
