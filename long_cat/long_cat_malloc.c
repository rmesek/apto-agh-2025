#include <stdbool.h>  // For bool type
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DIM 24     // Max dimension + 1 for null terminators/boundary checks
#define MAX_MOVES 550  // Max length for the moves sequence (adjust if needed)

// --- Data Structures ---

typedef struct {
  int x;
  int y;
} Position;

// Structure to hold information needed to undo a move sequence
typedef struct {
  Position
      changed_cells[MAX_DIM * MAX_DIM];     // Store positions of changed cells
  char original_values[MAX_DIM * MAX_DIM];  // Store original chars (' ' or '*')
  int change_count;                         // How many cells were changed
  int snacks_eaten_in_move;  // How many snacks were eaten in this move
  Position cat_start_pos;    // Where the cat was before this move sequence
} UndoInfo;

// Global variables to represent the board state (avoids passing large structs
// recursively)
char board[MAX_DIM][MAX_DIM];
int width, height;
int required_snacks_global;
Position cat_pos_global;
char moves[MAX_MOVES];
int moves_count = 0;
bool solution_found = false;

// --- Pre-allocated Undo Stack ---
UndoInfo* undo_stack = NULL;  // Pointer to the pre-allocated array
// --- End Pre-allocated Undo Stack ---

// Directions: G (Up), D (Down), L (Left), P (Right)
int dx[] = {0, 0, -1, 1};
int dy[] = {-1, 1, 0, 0};  // Corresponds to G, D, L, P
char dir_chars[] = {'G', 'D', 'L', 'P'};

// --- Function Declarations ---

bool load_input();
void print_output();
bool apply_move(char direction, UndoInfo* undo_info);
void undo_move(const UndoInfo* undo_info);
void solve();

// --- Function Implementations ---

// Reads the board configuration from standard input
bool load_input() {
  if (scanf("%d %d %d", &width, &height, &required_snacks_global) != 3) {
    fprintf(stderr, "Error reading dimensions and required snacks.\n");
    return false;
  }
  // Add boundary checks
  if (width <= 0 || width >= MAX_DIM || height <= 0 || height >= MAX_DIM ||
      required_snacks_global < 0) {
    fprintf(stderr, "Invalid dimensions or required snacks.\n");
    return false;
  }

  // Consume the rest of the first line
  while (getchar() != '\n');

  int initial_snacks_count = 0;
  bool cat_found = false;

  for (int y = 0; y < height; ++y) {
    if (fgets(board[y], MAX_DIM, stdin) == NULL) {
      fprintf(stderr, "Error reading board row %d.\n", y);
      return false;
    }
    // Remove trailing newline if present
    board[y][strcspn(board[y], "\r\n")] = 0;

    if ((int)strlen(board[y]) != width) {
      fprintf(stderr, "Error: Row %d length (%zu) does not match width (%d).\n",
              y, strlen(board[y]), width);
      return false;
    }

    for (int x = 0; x < width; ++x) {
      if (board[y][x] == '*') {
        initial_snacks_count++;
      } else if (board[y][x] == 'O') {
        if (cat_found) {
          fprintf(stderr,
                  "Error: Multiple cat starting positions ('O') found.\n");
          return false;
        }
        cat_pos_global.x = x;
        cat_pos_global.y = y;
        cat_found = true;
      } else if (board[y][x] != '.' && board[y][x] != '#') {
        fprintf(stderr, "Error: Invalid character '%c' found at (%d, %d).\n",
                board[y][x], x, y);
        return false;
      }
    }
  }

  if (!cat_found) {
    fprintf(stderr, "Error: Cat starting position ('O') not found.\n");
    return false;
  }
  if (initial_snacks_count < required_snacks_global) {
    fprintf(
        stderr,
        "Error: Not enough snacks (*) on the board (%d) for required (%d).\n",
        initial_snacks_count, required_snacks_global);
    return false;
  }

  return true;
}

// Prints the found sequence of moves
void print_output() {
  moves[moves_count] = '\0';  // Null-terminate the string
  printf("%s\n", moves);
}

// Applies a move sequence in a given direction and records undo info
// Returns true if the cat moved, false otherwise
bool apply_move(char direction, UndoInfo* undo_info) {
  int dir_index = -1;
  for (int i = 0; i < 4; ++i) {
    if (dir_chars[i] == direction) {
      dir_index = i;
      break;
    }
  }
  if (dir_index == -1) return false;  // Should not happen

  int current_dx = dx[dir_index];
  int current_dy = dy[dir_index];

  Position start_pos = cat_pos_global;
  undo_info->cat_start_pos = start_pos;
  undo_info->change_count = 0;
  undo_info->snacks_eaten_in_move = 0;

  while (true) {
    int next_x = cat_pos_global.x + current_dx;
    int next_y = cat_pos_global.y + current_dy;

    char next_cell = board[next_y][next_x];

    // Check for obstacles or already visited path
    if (next_cell == '#' || next_cell == 'O' || next_cell == 'X') {
      break;  // Stop before hitting obstacle/origin/path
    }

    // Record the change for undo
    if (undo_info->change_count < MAX_DIM * MAX_DIM) {
      undo_info->changed_cells[undo_info->change_count] =
          (Position){next_x, next_y};
      undo_info->original_values[undo_info->change_count] =
          board[next_y][next_x];  // Store '.' or '*'
      undo_info->change_count++;
    } else {
      fprintf(stderr, "Error: Exceeded undo buffer size.\n");
      // Handle error appropriately, maybe exit or return false
      return false;  // Indicate failure
    }

    // Update state
    if (next_cell == '*') {
      required_snacks_global--;
      undo_info->snacks_eaten_in_move++;
    }

    board[next_y][next_x] = 'X';  // Mark path
    cat_pos_global.x = next_x;
    cat_pos_global.y = next_y;
  }

  // Check if the cat actually moved
  if (cat_pos_global.x == start_pos.x && cat_pos_global.y == start_pos.y) {
    return false;
  }

  return true;
}

// Reverts the changes made by apply_move using the UndoInfo
void undo_move(const UndoInfo* undo_info) {
  // Restore cat position
  cat_pos_global = undo_info->cat_start_pos;

  // Restore board cells
  for (int i = 0; i < undo_info->change_count; ++i) {
    Position p = undo_info->changed_cells[i];
    board[p.y][p.x] = undo_info->original_values[i];
  }

  // Restore snack count
  required_snacks_global += undo_info->snacks_eaten_in_move;
}

// Recursive depth-first search function
void solve() {
  // Base case: Found a solution
  if (required_snacks_global == 0) {
    print_output();
    solution_found = true;
    return;  // Stop searching once one solution is found
  }

  // Pruning: If max moves reached (prevents infinite loops/stack overflow)
  if (moves_count >= MAX_MOVES - 1) return;

  // Recursive step: Try all directions
  for (int i = 0; i < 4; ++i) {
    UndoInfo* undo_info = &undo_stack[moves_count];

    if (apply_move(dir_chars[i], undo_info)) {
      // Move was successful, add to path and recurse
      moves[moves_count++] = dir_chars[i];

      solve();

      // Backtrack
      moves_count--;  // Remove the move from the path
      undo_move(undo_info);

      // If a solution was found in the recursive call, stop exploring further
      if (solution_found) return;
    }
  }
}

// --- Main Function ---

int main() {
  if (!load_input()) {
    return 1;  // Exit if input loading failed
  }

  // Allocate space for MAX_MOVES UndoInfo structs
  undo_stack = (UndoInfo*)malloc(MAX_MOVES * sizeof(UndoInfo));
  if (undo_stack == NULL) {
    fprintf(stderr, "Error: Failed to allocate memory for undo stack.\n");
    return 1;  // Exit if memory allocation fails
  }

  solve();

  free(undo_stack);   // Free the entire pre-allocated stack before exiting
  undo_stack = NULL;  // Good practice

  if (!solution_found) {
    // Optional: Indicate if no solution was found
    // fprintf(stderr, "No solution found.\n");
  }

  return 0;
}