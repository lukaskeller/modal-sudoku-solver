import pytest
from src.sudoku.main import solve  # Assuming this function exists
from test.fixtures.examples import beginner_puzzle, advanced_puzzle


@pytest.mark.parametrize("puzzle", beginner_puzzle()[:5])  # first 5
def test_sudoku_solver_simple_subset(puzzle):
    # simply call the function in local() mode to bypass modal
    solution = solve.local(puzzle.sudoku)
    assert solution.solution == puzzle.solution


@pytest.mark.parametrize("puzzle", advanced_puzzle()[:5])  # first 5
def test_sudoku_solver_advanced_subset(puzzle):
    # simply call the function in local() mode to bypass modal
    solution = solve.local(puzzle.sudoku)
    assert solution.solution == puzzle.solution


@pytest.mark.slow
@pytest.mark.parametrize("puzzle", beginner_puzzle())
def test_sudoku_solver_simple(puzzle):
    # simply call the function in local() mode to bypass modal
    solution = solve.local(puzzle.sudoku)
    assert solution.solution == puzzle.solution


@pytest.mark.slow
@pytest.mark.parametrize("puzzle", advanced_puzzle())
def test_sudoku_solver_advanced(puzzle):
    # simply call the function in local() mode to bypass modal
    solution = solve.local(puzzle.sudoku)
    assert solution.solution == puzzle.solution
