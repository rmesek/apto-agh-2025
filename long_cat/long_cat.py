type Board = list[list[str]]
type Position = tuple[int, int]


def load_input() -> tuple[Board, set[Position], int, Position]:
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

    return board, snacks, required_snacks, cat


def print_output(moves: list[str]) -> None:
    print("".join(moves))


def print_board(board: Board, h_spacing: int = 2) -> None:
    RED = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

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
        line = h_space.join(colored_row)
        print(line)


def main(debug: bool = False) -> None:
    board, snacks, required_snacks, cat = load_input()

    if debug:
        print(f"Loaded board of size {len(board)}x{len(board[0])}")
        print_board(board)
        print(f"Snacks: {snacks}")
        print(f"Cat: {cat}")
        print(f"Required Snacks: {required_snacks}")


if __name__ == "__main__":
    main(debug=True)
