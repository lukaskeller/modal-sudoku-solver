import pyomo.environ as pe

from .fastapi_models import Sudoku, SudokuSolution

def solve_sudoku(s: Sudoku):

    model = pe.ConcreteModel()
    model.rows = pe.Set(initialize=range(9))
    model.cols = pe.Set(initialize=range(9))
    model.vals = pe.Set(initialize=range(1,10)) # actual numbers 1 to incl 9

    model.box = pe.Set(initialize=range(3)) # identifes the 3x3 boxes position in row or col order respectively

    # boolean variable for each row and column whether it contains a certain value or not
    model.has_value = pe.Var(model.rows * model.cols * model.vals, domain=pe.Binary )


    def _row_rule(model, row, value):
        return sum(model.has_value[row, col, value] for col in model.cols) == 1
    model.row_rule = pe.Constraint(model.rows * model.vals, rule=_row_rule)

    def _col_rule(model, col, value):
        return sum(model.has_value[row, col, value] for row in model.rows) == 1
    model.col_rule = pe.Constraint(model.cols * model.vals, rule=_col_rule)

    def _box_rule(model, box_row: int, box_col:int, value:int): # evaluated 3x3x9 times
        row = 3* box_row # offset
        col = 3* box_col # offset: 0, 3 or 6, then added 1,2,3
        return (
            model.has_value[row+0, col, value] + model.has_value[row+0, col+1, value] + model.has_value[row+0, col+2, value] +
            model.has_value[row+1, col, value] + model.has_value[row+1, col+1, value] + model.has_value[row+1, col+2, value] +
            model.has_value[row+2, col, value] + model.has_value[row+2, col+1, value] + model.has_value[row+2, col+2, value] == 1
        )
    model.box_rule = pe.Constraint(model.box * model.box * model.vals, rule=_box_rule)

    # fix the known values from the grid
    for row in model.rows:
        for col in model.cols:
            if s.grid[row][col] is not None and s.grid[row][col] != 0:
                model.has_value[row, col, s.grid[row][col]].fix(1)

    model.obj = pe.Objective(expr=0, sense=pe.minimize)

    pe.SolverFactory('appsi_highs').solve(model, load_solutions=False).write()

    return model


