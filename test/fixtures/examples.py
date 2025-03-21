import json
import os
from src.sudoku.fastapi_models import SudokuSolution, Sudoku

# Define the path to the fixture data
FIXTURE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(FIXTURE_DIR, "data")


def load_file_as_json(filename) -> dict:
    """Load JSON fixture from the data directory."""
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)


# not setting this as a fixture bcz we to use it for parametrizing the test
def beginner_puzzle() -> list[SudokuSolution]:
    """Returns the beginner puzzle fixture"""

    # Load different difficulty level puzzles
    beginner_puzzle_dict = load_file_as_json("beginner.json")
    puzzles = list()

    for puzzle in beginner_puzzle_dict["puzzles"]:
        sudoku = Sudoku(puzzle=puzzle["puzzle"], level="beginner")
        solution = SudokuSolution(sudoku=sudoku, solution=puzzle["solution"])
        puzzles.append(solution)

    return puzzles


# not setting this as a fixture bcz we to use it for parametrizing the test
def advanced_puzzle():
    """Returns the advanced puzzle fixture"""

    # Load different difficulty level puzzles
    advanced_puzzle_dict = load_file_as_json("advanced.json")
    puzzles = list()

    for puzzle in advanced_puzzle_dict["puzzles"]:
        sudoku = Sudoku(puzzle=puzzle["puzzle"], level="advanced")
        solution = SudokuSolution(sudoku=sudoku, solution=puzzle["solution"])
        puzzles.append(solution)

    return puzzles
