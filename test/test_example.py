import pytest
from src.sudoku.main import solve  # Assuming this function exists
from test.fixtures.examples import beginner_puzzle, advanced_puzzle


def test_sudoku_solver(beginner_puzzle):
    p_1 = beginner_puzzle[0]

    # simply call the function in local() mode to bypass modal
    solution = solve.local(p_1.sudoku)
    assert solution.solution == p_1.solution


def test_sudoku_solver_advanced(advanced_puzzle):

    for i, p in enumerate(advanced_puzzle):
        if i>3:
            break
        p = advanced_puzzle[0]

        # simply call the function in local() mode to bypass modal
        solution = solve.local(p.sudoku)
        assert solution.solution == p.solution

