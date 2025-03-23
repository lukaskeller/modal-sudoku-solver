import pytest
from src.sudoku.main import solve  # Assuming this function exists
from src.sudoku.fastapi_models import Sudoku


def test_unsolvable_puzzle():
    # Load different difficulty level puzzle
    sudoku = Sudoku(puzzle="1" * 80 + "9", level="beginner")
    with pytest.raises(ValueError) as e:
        solution = solve.local(sudoku)  # noqa: F841
    assert "infeasible" in str(e.value)


def test_several_solutions():
    sudoku = Sudoku(puzzle="1" + "." * 80, level="beginner")
    # should not raise, will just return any 1 valid solution
    solve.local(sudoku)  # does not throw
