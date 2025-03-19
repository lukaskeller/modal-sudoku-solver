import itertools
import pyomo.environ as pe

from .fastapi_models import Sudoku, SudokuSolution

def solve_sudoku(puzzle: str):

    model = _prepare_model() # todo: can be extracted to startup for performance, independent of puzzle


    # fix the known values from the grid
    for i, (row, col) in enumerate(itertools.product(model.rows, model.cols)):
        val = puzzle[i]
        if val != ".":
            # the puzzle looks like this
            # puzzle='1.4.28...3.815...7265.7.4.17438..15...2.4.73...97.162..3.......8.1..6....263.7.4.'
            model.has_value[row, col, int(val)].fix(1) # force to true

    model.obj = pe.Objective(expr=0, sense=pe.minimize) # dummy obj func

    #sol = pe.SolverFactory('glpk').solve(model, load_solutions=True, tee=True)
    sol = pe.SolverFactory('appsi_highs').solve(model, load_solutions=True, tee=True)

    canonical_form = _extract_result(model, sol)
    return canonical_form


def _extract_result(model, sol):
    sol_json = sol.json_repn()
    solver_info = sol_json['Solver'][0]
    print(solver_info)
    correct_cell_values = sorted([v.index() for v in model.has_value.values() if v.value > 0.5])
    # tuple form: [(0, 0, 1), (0, 1, 7), (0, 2, 4), (0, 3, 6), ....
    assert len(correct_cell_values) == 81
    only_correct_values = [val for (_, _, val) in correct_cell_values]
    # value form: [1, 7, 4, 6, 2, 8,...
    canonical_form = "".join(str(val) for val in only_correct_values)
    # '17462859...
    return canonical_form


def _prepare_model():
    model = pe.ConcreteModel()
    model.rows = pe.Set(initialize=range(9))
    model.cols = pe.Set(initialize=range(9))
    model.vals = pe.Set(initialize=range(1, 10))  # actual numbers 1 to incl 9
    model.box = pe.Set(initialize=range(3))  # identifes the 3x3 boxes position in row or col order respectively
    # boolean variable for each row and column whether it contains a certain value or not
    model.has_value = pe.Var(model.rows * model.cols * model.vals, domain=pe.Binary)

    def _row_rule(model, row, value):
        return sum(model.has_value[row, col, value] for col in model.cols) == 1

    model.row_rule = pe.Constraint(model.rows * model.vals, rule=_row_rule)

    def _col_rule(model, col, value):
        return sum(model.has_value[row, col, value] for row in model.rows) == 1

    model.col_rule = pe.Constraint(model.cols * model.vals, rule=_col_rule)

    def _cell_rule(model, col, row):
        return sum(model.has_value[row, col, v] for v in model.vals) == 1

    model.cell_rule = pe.Constraint(model.cols * model.rows, rule=_cell_rule)

    def _box_rule(model, box_row: int, box_col: int, value: int):  # evaluated 3x3x9 times
        row = 3 * box_row  # offset
        col = 3 * box_col  # offset: 0, 3 or 6, then added 1,2,3
        return (
                model.has_value[row + 0, col, value] + model.has_value[row + 0, col + 1, value] + model.has_value[
            row + 0, col + 2, value] +
                model.has_value[row + 1, col, value] + model.has_value[row + 1, col + 1, value] + model.has_value[
                    row + 1, col + 2, value] +
                model.has_value[row + 2, col, value] + model.has_value[row + 2, col + 1, value] + model.has_value[
                    row + 2, col + 2, value] == 1
        )

    model.box_rule = pe.Constraint(model.box * model.box * model.vals, rule=_box_rule)
    return model


