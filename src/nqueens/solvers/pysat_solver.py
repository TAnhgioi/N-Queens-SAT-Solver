from __future__ import annotations
import time
from pysat.solvers import Solver
from nqueens.problem import validate_n, validate_solution
from nqueens.encoding.sequential import build_cnf, decode_solution
from nqueens.solvers.base import SolveResult


def solve_pysat(n: int, encoding: str = "pairwise", timeout: float = 60) -> SolveResult:
    validate_n(n)
    started = time.perf_counter()
    cnf = build_cnf(n, encoding)
    with Solver(name="g3", bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
    elapsed = time.perf_counter() - started
    placement = decode_solution(model, n) if model else None
    valid = validate_solution(placement, n) if placement is not None else None
    return SolveResult(n, "pysat", "SAT" if sat else "UNSAT", elapsed, placement, valid, cnf.nv, len(cnf.clauses))
