from __future__ import annotations
import time
from nqueens.problem import validate_n, validate_solution
from nqueens.solvers.base import SolveResult


def solve_gurobi(n: int, timeout: float = 60) -> SolveResult:
    validate_n(n)
    try:
        import gurobipy as gp
        from gurobipy import GRB
    except ImportError as exc:
        raise RuntimeError("Gurobi Python package is missing; install gurobipy and configure a valid license") from exc
    started = time.perf_counter()
    model = gp.Model("nqueens")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = float(timeout)
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
    for r in range(n): model.addConstr(gp.quicksum(x[r,c] for c in range(n)) == 1)
    for c in range(n): model.addConstr(gp.quicksum(x[r,c] for r in range(n)) == 1)
    for d in range(-(n-1), n): model.addConstr(gp.quicksum(x[r,c] for r in range(n) for c in range(n) if r-c == d) <= 1)
    for d in range(2*n-1): model.addConstr(gp.quicksum(x[r,c] for r in range(n) for c in range(n) if r+c == d) <= 1)
    model.setObjective(0)
    model.optimize()
    elapsed = time.perf_counter() - started
    if model.SolCount:
        p = [next(c for c in range(n) if x[r,c].X > .5) for r in range(n)]
        return SolveResult(n, "gurobi", "SAT", elapsed, p, validate_solution(p,n), n*n, model.NumConstrs)
    status = "UNSAT" if model.Status == GRB.INFEASIBLE else "UNKNOWN/TIMEOUT"
    return SolveResult(n, "gurobi", status, elapsed, None, None, n*n, model.NumConstrs)
