from typing import Literal
from dataclasses import dataclass

DEBUG = False

type Bed = Literal["O"]
type Empty = Literal["."]
type Wall = Literal["#"]
type Cat = Literal["X"]
type Food = Literal["*"]
type Block = Bed | Empty | Wall | Cat | Food
type Board = list[list[Block]]
type Direction = Literal["G", "D", "L", "P"]  # Up, Down, Left, Right


@dataclass
class BoardState:
    board: Board
    cat: tuple[int, int]
    food_eaten: int
    moves: list[Direction]
    _food: int
    _width: int
    _height: int

    def __repr__(self) -> str:
        board_str = "\n".join("".join(str(row)) for row in self.board)
        return (
            f"BoardState(board=\n{board_str}, \n"
            f"cat={self.cat},"
            f"food_eaten={self.food_eaten},"
            f"_food={self._food},"
            f"_width={self._width},"
            f"_height={self._height})"
        )

    def move_up(self) -> None:
        # TODO: Implement the logic to move the cat up
        self.moves.append("G")


def load_input() -> BoardState:
    board: Board = []
    w, h, s = map(int, input().strip().split())
    cat = None
    for i in range(h):
        line = input().strip()
        if "O" in line:
            cat = (line.index("O"), i)
        board.append(list(line))  # type: ignore
    assert cat is not None, "Cat's bed not found"
    board_state = BoardState(
        board=board, cat=cat, food_eaten=0, moves=[], _food=s, _width=w, _height=h
    )
    return board_state


def print_output(moves: list[Direction]) -> None:
    print("".join(moves))


def solve(board_state: BoardState) -> list[Direction]:
    return board_state.moves


if __name__ == "__main__":
    board_state = load_input()
    if DEBUG:
        print(board_state)
    moves = solve(board_state)
    print_output(moves)
