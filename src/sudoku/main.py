import modal


from .fastapi_models import Sudoku, SudokuSolution
from .solve import SudokuSolver

#image = modal.Image.debian_slim().pip_install("fastapi[standard]")
image = modal.Image.debian_slim().pip_install_from_pyproject("pyproject.toml")

app = modal.App(name="sudoku-solver", image=image)

solver = SudokuSolver()

@app.function()
@modal.fastapi_endpoint(requires_proxy_auth=True, method="POST")
def solve(s: Sudoku) -> SudokuSolution:

   raw_solution = solver.solve_sudoku(s.puzzle)
   solution = SudokuSolution(sudoku=s, solution=raw_solution)
   return solution
