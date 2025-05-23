import random
import sys


def generate_board(width, height):
    # initialize the board with empty spaces '.'
    board = [["." for _ in range(width)] for _ in range(height)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    snack_count = 0

    # fill edges with solid walls '#'
    for i in range(width):
        board[0][i] = "#"
        board[height - 1][i] = "#"
    for i in range(height):
        board[i][0] = "#"
        board[i][width - 1] = "#"

    # find random start position 'O'
    cat_x = random.randint(1, width - 2)
    cat_y = random.randint(1, height - 2)
    board[cat_y][cat_x] = "O"

    last_direction = None
    while True:
        moved = False

        # try every possible move in random order
        random.shuffle(directions)

        for direction in directions:
            new_x = cat_x + direction[0]
            new_y = cat_y + direction[1]

            # check if new position is valid
            if board[new_y][new_x] != ".":
                continue

            # if changing direction place a wall
            if last_direction and direction != last_direction:
                wall_x = cat_x + last_direction[0]
                wall_y = cat_y + last_direction[1]
                if board[wall_y][wall_x] == ".":
                    board[wall_y][wall_x] = "#"

            # make the move
            last_direction = direction
            board[new_y][new_x] = "*"
            snack_count += 1
            cat_x = new_x
            cat_y = new_y
            moved = True
            break

        # no move was possible
        if not moved:
            break

    # replace '.' with walls '#' to ensure all spaces are filled
    for y in range(height):
        for x in range(width):
            if board[y][x] == ".":
                board[y][x] = "#"
    return board, snack_count


def print_board(board, required_snacks):
    height = len(board)
    width = len(board[0])
    print(f"{width} {height} {required_snacks}")
    for row in board:
        print("".join(row))


def main():
    if len(sys.argv) != 3:
        print("Usage: python gen.py <width> <height>")
        sys.exit(1)

    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        board, snack_count = generate_board(width, height)
        print_board(board, snack_count)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
