from __future__ import annotations
import time
from nqueens.problem import validate_n, validate_solution
from nqueens.solvers.base import SolveResult


def solve_cplex_cp(n: int, timeout: float = 60) -> SolveResult:
    validate_n(n)
    try:
        from docplex.cp.model import CpoModel
    except ImportError as exc:
        raise RuntimeError("DOcplex CP is missing; install docplex and configure a CPLEX CP Optimizer runtime/license") from exc
    started = time.perf_counter()
    mdl = CpoModel(name="nqueens_cp")
    q = [mdl.integer_var(min=0, max=n-1, name=f"q_{r}") for r in range(n)]
    mdl.add(mdl.all_diff(q))
    mdl.add(mdl.all_diff([q[r] + r for r in range(n)]))
    mdl.add(mdl.all_diff([q[r] - r for r in range(n)]))
    sol = mdl.solve(TimeLimit=float(timeout), LogVerbosity="Quiet")
    elapsed = time.perf_counter() - started
    if sol is not None:
        p = [sol.get_value(v) for v in q]
        result = SolveResult(n, "cplex-cp", "SAT", elapsed, p, validate_solution(p,n))
    else:
        result = SolveResult(n, "cplex-cp", "UNKNOWN/TIMEOUT", elapsed, None, None)
    return result
