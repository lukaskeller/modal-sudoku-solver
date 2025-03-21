from pydantic import BaseModel


class Sudoku(BaseModel):
    puzzle: str  # todo add validation: len 81, only dots or 1-9, complex rules?!
    level: str


class SudokuSolution(BaseModel):
    sudoku: Sudoku
    solution: str
