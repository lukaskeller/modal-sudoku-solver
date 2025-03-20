import json
import os
import pytest
from src.sudoku.fastapi_models import SudokuSolution, Sudoku

# Define the path to the fixture data
FIXTURE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(FIXTURE_DIR, "data")

def load_file_as_json(filename):
    """Load JSON fixture from the data directory."""
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)



# not setting this as a fixture bcz we to use it for parametrizing the test
def beginner_puzzle():
    """Returns the beginner puzzle fixture"""

    # Load different difficulty level puzzles
    BEGINNER_PUZZLE_DICT = load_file_as_json("beginner.json")
    BEGINNER_PUZZLE = list()

    for puzzle in BEGINNER_PUZZLE_DICT["puzzles"]:
        sudoku = Sudoku(puzzle=puzzle["puzzle"], level="beginner")
        solution = SudokuSolution(sudoku=sudoku, solution=puzzle["solution"])
        BEGINNER_PUZZLE.append(solution)

    return BEGINNER_PUZZLE

# not setting this as a fixture bcz we to use it for parametrizing the test
def advanced_puzzle():
    """Returns the advanced puzzle fixture"""

    # Load different difficulty level puzzles
    ADVANCED_PUZZLE_DICT = load_file_as_json("advanced.json")
    ADVANCED_PUZZLE = list()

    for puzzle in ADVANCED_PUZZLE_DICT["puzzles"]:
        sudoku = Sudoku(puzzle=puzzle["puzzle"], level="advanced")
        solution = SudokuSolution(sudoku=sudoku, solution=puzzle["solution"])
        ADVANCED_PUZZLE.append(solution)

    return ADVANCED_PUZZLE

