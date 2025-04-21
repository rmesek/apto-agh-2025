import random

def generate_board(width, height, wall_probability=0.4):
    """
    Generates a board with a border and random internal patterns,
    including chessboard-patterned walls.
    """

    board = [['.' for _ in range(width)] for _ in range(height)]

    # Create the border
    for y in range(height):
        board[y][0] = '#'
        board[y][width - 1] = '#'
    for x in range(width):
        board[0][x] = '#'
        board[height - 1][x] = '#'

    # Place potential walls in a chessboard pattern within the border
    # (x + y) % 2 == 0 defines one color of the chessboard
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x + y) % 2 == 0: # Target cells for potential walls
                if random.random() < wall_probability:
                    board[y][x] = '#'

    # --- Find available spots for 'O' and '*' ---
    available_dots = []
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if board[y][x] == '.':
                available_dots.append((x, y))

    if not available_dots:
        raise ValueError("No available spots left after placing walls.")

    # --- Place 'O' ---
    # Choose a random available spot for 'O'
    cat_pos_index = random.randint(0, len(available_dots) - 1)
    cat_x, cat_y = available_dots.pop(cat_pos_index) # Remove spot from list
    board[cat_y][cat_x] = 'O'

    # --- Place '*' ---
    # Calculate number of snacks based on remaining available spots
    # Use a proportion of the *remaining* dots after placing 'O'
    # Let's aim for snacks in about 30-40% of the remaining spots
    num_snacks_to_place = int(len(available_dots) * random.uniform(0.3, 0.4))
    num_snacks_to_place = min(num_snacks_to_place, len(available_dots)) # Can't place more snacks than spots

    # Place snacks randomly in the remaining available spots
    snacks_placed_count = 0
    random.shuffle(available_dots) # Shuffle to pick random spots easily
    for i in range(num_snacks_to_place):
        snack_x, snack_y = available_dots[i]
        board[snack_y][snack_x] = '*'
        snacks_placed_count += 1

    return board, snacks_placed_count

def print_board(board, width, height, num_snacks):
    """Prints the board dimensions and the board itself."""
    print(f"{width} {height} {num_snacks}")
    for row in board:
        print("".join(row))

# --- Main Execution ---
if __name__ == "__main__":
    board_width = 20
    board_height = 20
    # Adjust wall_probability (0.0 to 1.0) to control wall density
    # 0.0 = no internal walls, 1.0 = walls on all pattern cells
    prob_internal_wall = 0.2

    try:
        generated_board, snack_count = generate_board(
            board_width, board_height, wall_probability=prob_internal_wall
        )
        print_board(generated_board, board_width, board_height, snack_count)
    except ValueError as e:
        print(f"Error generating board: {e}")
        print("Consider reducing wall_probability or increasing board size.")