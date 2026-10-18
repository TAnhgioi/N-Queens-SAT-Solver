from __future__ import annotations


def solve(n: int, solver: str = "pysat", encoding: str = "pairwise", timeout: float = 60):
    # Lazy imports let CLI help and non-SAT solvers load without PySAT installed.
    if solver == "pysat":
        from nqueens.solvers.pysat_solver import solve_pysat
        return solve_pysat(n, encoding, timeout)
    if solver == "ortools":
        from nqueens.solvers.ortools_solver import solve_ortools
        return solve_ortools(n, timeout)
    if solver == "gurobi":
        from nqueens.solvers.gurobi_solver import solve_gurobi
        return solve_gurobi(n, timeout)
    if solver == "cplex-mip":
        from nqueens.solvers.cplex_mip_solver import solve_cplex_mip
        return solve_cplex_mip(n, timeout)
    if solver == "cplex-cp":
        from nqueens.solvers.cplex_cp_solver import solve_cplex_cp
        return solve_cplex_cp(n, timeout)
    raise ValueError(f"Unknown solver: {solver}")
