import pyomo.environ as pe

from .fastapi_models import Sudoku

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

    return model



sudoku_example = {
    "puzzle": "1.4.28...3.815...7265.7.4.17438..15...2.4.73...97.162..3.......8.1..6....263.7.4.",
    "solution": "174628593398154267265973481743862159612549738589731624437285916851496372926317845"
}

# convert to list-list form
def convert(s : str) -> Sudoku:
    s_list = list(val if val != "." else None for val in s)
    # slice after evry 9th element
    grid = [s_list[i:i+9] for i in range(0, len(s_list), 9)]
    
    return Sudoku(grid=grid, level='easy')




m = solve_sudoku(convert(sudoku_example["solution"]))

pe.SolverFactory('appsi_highs').solve(m,  load_solutions = False).write()
#m.pprint()
