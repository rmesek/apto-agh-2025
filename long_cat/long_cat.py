import copy
from dataclasses import dataclass
from typing import Dict, List, Literal, Set, Tuple

DEBUG = True

# Type definitions for better clarity
Bed = Literal["O"]
Empty = Literal["."]
Wall = Literal["#"]
Cat = Literal["X"]
Snack = Literal["*"]
Block = Literal[Bed, Empty, Wall, Cat, Snack]
Board = List[List[Block]]
Direction = Literal["G", "D", "L", "P"]  # Up, Down, Left, Right

# Direction mappings for readability
DIRECTION: Dict[Direction, Tuple[int, int]] = {
    "G": (0, -1),  # Up
    "D": (0, 1),  # Down
    "L": (-1, 0),  # Left
    "P": (1, 0),  # Right
}


@dataclass
class BoardState:
    board: Board  # Board as a 2D list of characters
    _width: int  # Width of the board
    _height: int  # Height of the board
    snacks: Set[Tuple[int, int]]  # Set of snack positions
    snacks_left: int  # Number of snacks left to eat
    cat: Tuple[int, int]  # Cat's current position
    moves: List[Direction]  # List of moves made

    def __repr__(self) -> str:
        board_str = "\n".join(str(row) for row in self.board)
        return (
            f"BoardState(board=\n{board_str}, \n"
            f"_width={self._width}, "
            f"_height={self._height}, "
            f"snacks={self.snacks}, "
            f"snacks_left={self.snacks_left}, "
            f"cat={self.cat}, "
            f"moves={self.moves})"
        )

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the position is valid for the cat to move."""
        block = self.board[y][x]
        in_bounds = 0 <= x < self._width and 0 <= y < self._height  # Optional
        can_walk = block in (".", "*")
        return in_bounds and can_walk

    def is_complete(self) -> bool:
        """Check if all snacks have been eaten."""
        return self.snacks_left == 0

    def clone(self) -> "BoardState":
        """Create a deep copy of the board state."""
        return copy.deepcopy(self)


def load_input() -> BoardState:
    """Load the input from stdin and return a BoardState object."""
    board: Board = []
    w, h, s = map(int, input().strip().split())
    cat = None
    snacks = set()

    for y in range(h):
        line = input().strip()
        for x in range(len(line)):
            if line[x] == "O":
                cat = (x, y)
            elif line[x] == "*":
                snacks.add((x, y))
        board.append(list(line))  # type: ignore

    assert cat is not None, "Cat's bed not found"

    return BoardState(
        board=board,
        _width=w,
        _height=h,
        snacks=snacks,
        snacks_left=s,
        cat=cat,
        moves=[],
    )


def print_output(moves: list[Direction]) -> None:
    """Print the moves in the required format."""
    print("".join(moves))


# Solver Code


def move(board_state: BoardState, direction: Direction) -> None:
    """Attempt to move in the given direction and return new state if valid."""
    dx, dy = DIRECTION[direction]

    while True:
        x, y = board_state.cat
        new_x, new_y = x + dx, y + dy

        if not board_state.is_valid_position(new_x, new_y):
            break

        # Elongate the cat
        board_state.cat = (new_x, new_y)
        board_state.board[new_y][new_x] = "X"

        # Check if there's a snack at the new position
        if (new_x, new_y) in board_state.snacks:
            board_state.snacks.remove((new_x, new_y))
            board_state.snacks_left -= 1

    board_state.moves.append(direction)

    if DEBUG:
        print(f"\033[94mMove {direction}:\033[0m")
        print(board_state)


def solve(board_state: BoardState) -> List[Direction]:
    """Main solver function."""
    for direction in "DPGL":
        move(board_state, direction)
    return board_state.moves


# End of Solver Code


if __name__ == "__main__":
    board_state = load_input()
    if DEBUG:
        print("\033[95mInitial Board State:\033[0m")
        print(board_state)
    moves = solve(board_state)
    print_output(moves)
    if DEBUG:
        print("\033[95mFinal Board State:\033[0m")
        print(board_state)
