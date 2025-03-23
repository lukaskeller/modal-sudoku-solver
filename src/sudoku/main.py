import modal


from .fastapi_models import Sudoku, SudokuSolution
from .solve import SudokuSolver

# image = modal.Image.debian_slim().pip_install("fastapi[standard]")
image = (
    modal.Image.debian_slim()
    .dockerfile_commands("COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/")
    .apt_install("glpk-utils")
    .add_local_file("pyproject.toml", "/pyproject.toml", copy=True)
    .add_local_file("uv.lock", "/uv.lock", copy=True)
    .run_commands(
        "uv export --frozen -o reqs.txt && uv pip install --system --compile-bytecode -r reqs.txt"
    )
)

app = modal.App(name="sudoku-solver", image=image)

solver = SudokuSolver()


@app.function()
@modal.fastapi_endpoint(requires_proxy_auth=True, method="POST")
def solve(s: Sudoku) -> SudokuSolution:
    raw_solution = solver.solve_sudoku(s.puzzle)
    solution = SudokuSolution(sudoku=s, solution=raw_solution)
    return solution
