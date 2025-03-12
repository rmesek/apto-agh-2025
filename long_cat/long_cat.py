import copy
from dataclasses import dataclass

# Type definitions
type Board = list[list[str]]
type Position = tuple[int, int]

# Constants for colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Directions for movement (Up, Down, Left, Right)
DIRECTIONS = {"G": (0, -1), "D": (0, 1), "L": (-1, 0), "P": (1, 0)}


@dataclass
class BoardState:
    """Class representing the state of the board."""

    board: Board
    snacks: set[Position]
    required_snacks: int
    cat: Position
    moves: list[str]

    def __repr__(self) -> str:
        def board_as_str(board: Board, h_spacing: int = 2) -> str:
            board_str = ""
            h_space = " " * h_spacing
            for row in board:
                colored_row = []
                for char in row:
                    if char == "#":
                        colored_row.append(f"{RED}{char}{RESET}")
                    elif char == "*":
                        colored_row.append(f"{GREEN}{char}{RESET}")
                    else:
                        colored_row.append(char)
                board_str += h_space.join(colored_row) + "\n"
            return board_str

        return (
            f"Board of size {len(self.board)}x{len(self.board[0])}\n"
            f"{board_as_str(self.board)}"
            f"Snacks: {self.snacks}\n"
            f"Cat: {self.cat}\n"
            f"Required Snacks: {self.required_snacks}\n"
            f"Moves: {self.moves}\n"
        )

    def clone(self) -> "BoardState":
        """Create a deep copy of the board state."""
        return copy.deepcopy(self)


def load_input() -> BoardState:
    board = []
    snacks = set()
    cat = None

    width, height, required_snacks = map(int, input().strip().split())
    for y in range(height):
        line = input().strip()
        assert len(line) == width, "Line length does not match specified width"
        for x in range(width):
            if line[x] == "*":
                snacks.add((x, y))
            elif line[x] == "O":
                cat = (x, y)
        board.append(list(line))
    assert len(board) == height, "Number of lines does not match specified height"
    assert len(snacks) >= required_snacks, "Not enough snacks specified"
    assert cat is not None, "Cat's bed not found"

    return BoardState(board, snacks, required_snacks, cat, [])


def print_output(board_state: BoardState) -> None:
    print("".join(board_state.moves))


def make_move(board_state: BoardState, direction: str) -> None:
    dx, dy = DIRECTIONS[direction]
    while True:
        new_x = board_state.cat[0] + dx
        new_y = board_state.cat[1] + dy

        if board_state.board[new_y][new_x] in ("#", "O", "X"):
            break

        if board_state.board[new_y][new_x] == "*":
            board_state.snacks.remove((new_x, new_y))
            board_state.required_snacks -= 1

        board_state.board[new_y][new_x] = "X"
        board_state.cat = (new_x, new_y)

    board_state.moves.append(direction)


def solve(board_state: BoardState) -> None:
    # TODO: Implement the actual solving logic
    for direction in "GPDLDL":
        make_move(board_state, direction)
        # print(board_state)


def main(debug: bool = False) -> None:
    board_state = load_input()

    if debug:
        print("Initial board state:")
        print(board_state)

    solve(board_state)

    if debug:
        print("Final board state:")
        print(board_state)

    print_output(board_state)


if __name__ == "__main__":
    main(debug=False)
