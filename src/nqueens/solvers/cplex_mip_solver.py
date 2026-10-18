from __future__ import annotations
import time
from nqueens.problem import validate_n, validate_solution
from nqueens.solvers.base import SolveResult


def solve_cplex_mip(n: int, timeout: float = 60) -> SolveResult:
    validate_n(n)
    try:
        from docplex.mp.model import Model
    except ImportError as exc:
        raise RuntimeError("DOcplex is missing; install docplex and configure a CPLEX runtime/license") from exc
    started = time.perf_counter()
    mdl = Model(name="nqueens_mip")
    mdl.parameters.timelimit = float(timeout)
    x = {(r,c): mdl.binary_var(name=f"x_{r}_{c}") for r in range(n) for c in range(n)}
    for r in range(n): mdl.add_constraint(mdl.sum(x[r,c] for c in range(n)) == 1)
    for c in range(n): mdl.add_constraint(mdl.sum(x[r,c] for r in range(n)) == 1)
    for d in range(-(n-1), n): mdl.add_constraint(mdl.sum(x[r,c] for r in range(n) for c in range(n) if r-c == d) <= 1)
    for d in range(2*n-1): mdl.add_constraint(mdl.sum(x[r,c] for r in range(n) for c in range(n) if r+c == d) <= 1)
    sol = mdl.solve(log_output=False)
    elapsed = time.perf_counter() - started
    if sol is not None:
        p = [next(c for c in range(n) if sol.get_value(x[r,c]) > .5) for r in range(n)]
        result = SolveResult(n, "cplex-mip", "SAT", elapsed, p, validate_solution(p,n), n*n, mdl.number_of_constraints)
    else:
        status_text = str(mdl.solve_details.status).lower()
        status = "UNSAT" if "infeasible" in status_text else "UNKNOWN/TIMEOUT"
        result = SolveResult(n, "cplex-mip", status, elapsed, None, None, n*n, mdl.number_of_constraints, status_text)
    mdl.end()
    return result
