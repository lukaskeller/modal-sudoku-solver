import itertools
import pyomo.environ as pe


class SudokuSolver:
    def __init__(self):
        # prep pyomo model only once
        self.model = self._prepare_model()
        self.solver = pe.SolverFactory("glpk")
        # self.solver = pe.SolverFactory("appsi_highs") # slower, although easier to install coz pypi package

    def solve_sudoku(self, puzzle: str):
        self.set_known_cell_values(puzzle)

        result = self.solver.solve(self.model, load_solutions=False, tee=True)

        if (result.solver.status == pe.SolverStatus.ok) and (
            result.solver.termination_condition == pe.TerminationCondition.optimal
        ):
            # Manually load the solution into the model
            self.model.solutions.load_from(result)
        else:
            raise ValueError(
                f"Model not solved to optimality: {result.solver.termination_condition}"
            )

        solution_canonical_form = self._extract_result()

        return solution_canonical_form

    def set_known_cell_values(self, puzzle: str):
        # we use variable fixing in pyomo to enforce starting values in the grid

        ## the model could have run before. reset all fixed vars. idempotent operation
        self.model.unfix_all_vars()

        # fix the known values from the grid
        all_rows_and_columns = itertools.product(
            self.model.rows, self.model.cols
        )  # (row, col) tuples
        for i, (row, col) in enumerate(all_rows_and_columns):
            # going through all columns and rows, if the puzzle has a value at this position, fix the corresponding variable
            # Note: the puzzle is a string with this structure:
            # puzzle='1.4.28...3.815...7265.7.4.17438..15...2.4.73...97.162..3.......8.1..6....263.7.4.'
            val = puzzle[i]
            if val != ".":
                self.model.has_value[row, col, int(val)].fix(1)  # force to true

    def _extract_result(self) -> str:
        correct_cell_values = sorted(
            [v.index() for v in self.model.has_value.values() if v.value > 0.5]
        )
        # tuple form: [(0, 0, 1), (0, 1, 7), (0, 2, 4), (0, 3, 6), ....
        assert len(correct_cell_values) == 81
        only_correct_values = [val for (_, _, val) in correct_cell_values]
        # value form: [1, 7, 4, 6, 2, 8,...
        canonical_form = "".join(str(val) for val in only_correct_values)
        # '17462859...
        return canonical_form

    @staticmethod
    def _prepare_model() -> pe.ConcreteModel:
        model = pe.ConcreteModel()
        model.rows = pe.Set(initialize=range(9))
        model.cols = pe.Set(initialize=range(9))
        model.vals = pe.Set(initialize=range(1, 10))  # actual numbers 1 to incl 9
        model.box = pe.Set(
            initialize=range(3)
        )  # identifes the 3x3 boxes position in row or col order respectively
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

        def _box_rule(
            model, box_row: int, box_col: int, value: int
        ):  # evaluated 3x3x9 times
            row = 3 * box_row  # offset
            col = 3 * box_col  # offset: 0, 3 or 6, then added 1,2,3
            return (
                model.has_value[row + 0, col, value]
                + model.has_value[row + 0, col + 1, value]
                + model.has_value[row + 0, col + 2, value]
                + model.has_value[row + 1, col, value]
                + model.has_value[row + 1, col + 1, value]
                + model.has_value[row + 1, col + 2, value]
                + model.has_value[row + 2, col, value]
                + model.has_value[row + 2, col + 1, value]
                + model.has_value[row + 2, col + 2, value]
                == 1
            )

        model.box_rule = pe.Constraint(
            model.box * model.box * model.vals, rule=_box_rule
        )

        model.obj = pe.Objective(expr=0, sense=pe.minimize)  # dummy obj func

        return model
