
from pydantic import BaseModel
from typing import Union

class Sudoku(BaseModel):
    grid: list[list[Union[int, None]]]
    level: str
