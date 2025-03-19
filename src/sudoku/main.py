import modal


from .fastapi_models import Sudoku, SudokuSolution
from .solve import solve_sudoku

#image = modal.Image.debian_slim().pip_install("fastapi[standard]")
image = modal.Image.debian_slim().pip_install_from_pyproject("pyproject.toml")

app = modal.App(image=image)

@app.function()
@modal.fastapi_endpoint(requires_proxy_auth=True, method="POST")
def solve(s: Sudoku) -> SudokuSolution:

   raw_solution = solve_sudoku(s.puzzle)
   solution = SudokuSolution(sudoku=s, solution=raw_solution)
   return solution
# 
# gen curl request for the endpoint
# with out null
# curl -H "Modal-Key: $TOKEN_ID" -H "Modal-Secret: $TOKEN_SECRET" -H "Content-Type: application/json" -X POST https://lukaskeller--main-py-f-dev.modal.run/ -d '{"grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "level": "easy"}' 
# with null (nulls symbolize empty cells)
# curl -H "Modal-Key: $TOKEN_ID" -H "Modal-Secret: $TOKEN_SECRET" -H "Content-Type: application/json" -X POST https://lukaskeller--main-py-f-dev.modal.run/ -d '{"grid": [[1, 2, 3], [4, 5, 6], [7, 8, null]], "level": "easy"}' 
