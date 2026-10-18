from __future__ import annotations
import time
from nqueens.problem import validate_n, validate_solution
from nqueens.solvers.base import SolveResult


def solve_ortools(n: int, timeout: float = 60) -> SolveResult:
    validate_n(n)
    try:
        from ortools.sat.python import cp_model
    except ImportError as exc:
        raise RuntimeError("OR-Tools is missing; install with: pip install ortools") from exc
    started = time.perf_counter()
    model = cp_model.CpModel()
    q = [model.new_int_var(0, n - 1, f"q_{r}") for r in range(n)]
    model.add_all_different(q)
    model.add_all_different([q[r] + r for r in range(n)])
    model.add_all_different([q[r] - r for r in range(n)])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(timeout)
    status = solver.solve(model)
    elapsed = time.perf_counter() - started
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        placement = [solver.value(v) for v in q]
        return SolveResult(n, "ortools", "SAT", elapsed, placement, validate_solution(placement, n), None, None)
    if status == cp_model.INFEASIBLE:
        return SolveResult(n, "ortools", "UNSAT", elapsed, None, None)
    return SolveResult(n, "ortools", "UNKNOWN/TIMEOUT", elapsed, None, None)
