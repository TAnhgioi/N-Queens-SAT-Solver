from __future__ import annotations
import argparse
from dataclasses import asdict
import json
from nqueens.problem import render_board
from nqueens.solvers.registry import solve
from nqueens.experiments.benchmark import run_benchmark


def main() -> None:
    parser = argparse.ArgumentParser(description="N-Queens solver comparison")
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("solve", help="solve one instance")
    one.add_argument("--n", type=int, required=True)
    one.add_argument("--solver", choices=["pysat", "ortools", "gurobi", "cplex-mip", "cplex-cp"], default="pysat")
    one.add_argument("--encoding", choices=["pairwise", "sequential"], default="pairwise")
    one.add_argument("--timeout", type=float, default=60)
    bench = sub.add_parser("benchmark", help="run benchmark instances")
    bench.add_argument("--sizes", type=int, nargs="+", required=True)
    bench.add_argument("--solvers", nargs="+", choices=["pysat", "ortools", "gurobi", "cplex-mip", "cplex-cp"], default=["pysat", "ortools"])
    bench.add_argument("--timeout", type=float, default=60)
    bench.add_argument("--csv", default="results/benchmark.csv")
    args = parser.parse_args()
    if args.command == "solve":
        result = solve(args.n, args.solver, args.encoding, args.timeout)
        print(json.dumps(asdict(result), indent=2))
        if result.solution is not None:
            print(render_board(result.solution))
    else:
        run_benchmark(args.sizes, args.solvers, args.timeout, args.csv)

if __name__ == "__main__":
    main()
