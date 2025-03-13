import copy
from dataclasses import dataclass

# Type definitions
type Board = list[list[str]]
type InitBoard = tuple[tuple[str, ...], ...]
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
    _init_board: InitBoard = tuple()

    def __post_init__(self) -> None:
        """Set the initial board state."""
        self._init_board = tuple(tuple(row) for row in self.board)

    def __hash__(self) -> int:
        """Hash function to allow BoardState to be used in sets."""
        # Use the moves and _init_board for hashing
        return hash((tuple(self.moves), self._init_board))

    def __eq__(self, other: object) -> bool:
        """Equality check for BoardState."""
        if not isinstance(other, BoardState):
            return NotImplemented
        return self.moves == other.moves and self._init_board == other._init_board

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


def make_move(board_state: BoardState, direction: str) -> bool:
    dx, dy = DIRECTIONS[direction]
    start_position = board_state.cat

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

    if start_position == board_state.cat:
        return False

    board_state.moves.append(direction)
    return True


def brute_force(
    board_state: BoardState, found_states: set[BoardState], early_stop: bool = True
) -> None:
    if early_stop and board_state.required_snacks == 0:
        return

    for direction in DIRECTIONS:
        new_board_state = board_state.clone()
        if make_move(new_board_state, direction):
            found_states.add(new_board_state)
            brute_force(new_board_state, found_states, early_stop)


def solve(board_state: BoardState, debug: bool = False) -> set[BoardState]:
    all_states = {board_state}

    brute_force(board_state, all_states, early_stop=not debug)

    if debug:
        print(f"Found {len(all_states)} states")

    return {state for state in all_states if state.required_snacks == 0}


def main(debug: bool = False) -> None:
    board_state = load_input()

    if debug:
        print("Initial board state:")
        print(board_state)

    solutions = solve(board_state, debug=debug)

    if debug:
        print(f"Found {len(solutions)} solutions:")
        for solution in solutions:
            print(solution)

    for solution in solutions:
        print_output(solution)
        if not debug:
            break


if __name__ == "__main__":
    main(debug=False)
