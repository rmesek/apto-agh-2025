#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_DIM 24
#define MAX_MOVES 550

// --- Data Structures ---

typedef struct {
  int x;
  int y;
} Position;

// Node for A* search
typedef struct Node {
  Position pos;
  Position cat_pos;
  int snacks_remaining;
  int g_cost;  // Actual cost from start
  int h_cost;  // Heuristic cost to goal
  int f_cost;  // g_cost + h_cost
  char move_sequence[MAX_MOVES];
  int move_length;
  char board_state[MAX_DIM][MAX_DIM];
  struct Node* parent;
} Node;

// Priority queue for A* (min-heap)
typedef struct {
  Node** nodes;
  int size;
  int capacity;
} PriorityQueue;

// Global variables
char initial_board[MAX_DIM][MAX_DIM];
int width, height;
int required_snacks_global;
Position initial_cat_pos;
char solution_moves[MAX_MOVES];
bool solution_found = false;

// Directions: G (Up), D (Down), L (Left), P (Right)
int dx[] = {0, 0, -1, 1};
int dy[] = {-1, 1, 0, 0};
char dir_chars[] = {'G', 'D', 'L', 'P'};

// --- Function Declarations ---
bool load_input();
void print_output();
PriorityQueue* create_priority_queue(int capacity);
void destroy_priority_queue(PriorityQueue* pq);
void pq_insert(PriorityQueue* pq, Node* node);
Node* pq_extract_min(PriorityQueue* pq);
bool pq_is_empty(PriorityQueue* pq);
Node* create_node(Position cat_pos, int snacks_remaining, const char board[MAX_DIM][MAX_DIM], 
                  const char* moves, int move_length, int g_cost);
void destroy_node(Node* node);
int calculate_heuristic(Position cat_pos, const char board[MAX_DIM][MAX_DIM], int snacks_remaining);
bool apply_move_to_state(char direction, char board[MAX_DIM][MAX_DIM], Position* cat_pos, int* snacks_eaten);
void copy_board(const char src[MAX_DIM][MAX_DIM], char dest[MAX_DIM][MAX_DIM]);
bool states_equal(const Node* a, const Node* b);
void solve_astar();

// --- Function Implementations ---

bool load_input() {
  if (scanf("%d %d %d", &width, &height, &required_snacks_global) != 3) {
    fprintf(stderr, "Error reading dimensions and required snacks.\n");
    return false;
  }
  
  if (width <= 0 || width >= MAX_DIM || height <= 0 || height >= MAX_DIM ||
      required_snacks_global < 0) {
    fprintf(stderr, "Invalid dimensions or required snacks.\n");
    return false;
  }

  while (getchar() != '\n');

  int initial_snacks_count = 0;
  bool cat_found = false;

  for (int y = 0; y < height; ++y) {
    if (fgets(initial_board[y], MAX_DIM, stdin) == NULL) {
      fprintf(stderr, "Error reading board row %d.\n", y);
      return false;
    }
    initial_board[y][strcspn(initial_board[y], "\r\n")] = 0;

    if ((int)strlen(initial_board[y]) != width) {
      fprintf(stderr, "Error: Row %d length (%zu) does not match width (%d).\n",
              y, strlen(initial_board[y]), width);
      return false;
    }

    for (int x = 0; x < width; ++x) {
      if (initial_board[y][x] == '*') {
        initial_snacks_count++;
      } else if (initial_board[y][x] == 'O') {
        if (cat_found) {
          fprintf(stderr, "Error: Multiple cat starting positions ('O') found.\n");
          return false;
        }
        initial_cat_pos.x = x;
        initial_cat_pos.y = y;
        cat_found = true;
      } else if (initial_board[y][x] != '.' && initial_board[y][x] != '#') {
        fprintf(stderr, "Error: Invalid character '%c' found at (%d, %d).\n",
                initial_board[y][x], x, y);
        return false;
      }
    }
  }

  if (!cat_found) {
    fprintf(stderr, "Error: Cat starting position ('O') not found.\n");
    return false;
  }
  if (initial_snacks_count < required_snacks_global) {
    fprintf(stderr, "Error: Not enough snacks (*) on the board (%d) for required (%d).\n",
            initial_snacks_count, required_snacks_global);
    return false;
  }

  return true;
}

void print_output() {
  printf("%s\n", solution_moves);
}

PriorityQueue* create_priority_queue(int capacity) {
  PriorityQueue* pq = malloc(sizeof(PriorityQueue));
  if (!pq) return NULL;
  
  pq->nodes = malloc(capacity * sizeof(Node*));
  if (!pq->nodes) {
    free(pq);
    return NULL;
  }
  
  pq->size = 0;
  pq->capacity = capacity;
  return pq;
}

void destroy_priority_queue(PriorityQueue* pq) {
  if (!pq) return;
  
  for (int i = 0; i < pq->size; i++) {
    destroy_node(pq->nodes[i]);
  }
  free(pq->nodes);
  free(pq);
}

void pq_insert(PriorityQueue* pq, Node* node) {
  if (pq->size >= pq->capacity) return;
  
  int i = pq->size++;
  pq->nodes[i] = node;
  
  // Bubble up
  while (i > 0) {
    int parent = (i - 1) / 2;
    if (pq->nodes[i]->f_cost >= pq->nodes[parent]->f_cost) break;
    
    Node* temp = pq->nodes[i];
    pq->nodes[i] = pq->nodes[parent];
    pq->nodes[parent] = temp;
    i = parent;
  }
}

Node* pq_extract_min(PriorityQueue* pq) {
  if (pq->size == 0) return NULL;
  
  Node* min = pq->nodes[0];
  pq->nodes[0] = pq->nodes[--pq->size];
  
  // Bubble down
  int i = 0;
  while (true) {
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    int smallest = i;
    
    if (left < pq->size && pq->nodes[left]->f_cost < pq->nodes[smallest]->f_cost)
      smallest = left;
    if (right < pq->size && pq->nodes[right]->f_cost < pq->nodes[smallest]->f_cost)
      smallest = right;
    
    if (smallest == i) break;
    
    Node* temp = pq->nodes[i];
    pq->nodes[i] = pq->nodes[smallest];
    pq->nodes[smallest] = temp;
    i = smallest;
  }
  
  return min;
}

bool pq_is_empty(PriorityQueue* pq) {
  return pq->size == 0;
}

Node* create_node(Position cat_pos, int snacks_remaining, const char board[MAX_DIM][MAX_DIM],
                  const char* moves, int move_length, int g_cost) {
  Node* node = malloc(sizeof(Node));
  if (!node) return NULL;
  
  node->cat_pos = cat_pos;
  node->snacks_remaining = snacks_remaining;
  node->g_cost = g_cost;
  node->h_cost = calculate_heuristic(cat_pos, board, snacks_remaining);
  node->f_cost = node->g_cost + node->h_cost;
  node->move_length = move_length;
  node->parent = NULL;
  
  if (moves && move_length > 0) {
    memcpy(node->move_sequence, moves, move_length);
  }
  node->move_sequence[move_length] = '\0';
  
  copy_board(board, node->board_state);
  
  return node;
}

void destroy_node(Node* node) {
  if (node) free(node);
}

int calculate_heuristic(Position cat_pos, const char board[MAX_DIM][MAX_DIM], int snacks_remaining) {
  if (snacks_remaining == 0) return 0;
  
  // Find distance to nearest snack (Manhattan distance)
  int min_dist = INT_MAX;
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      if (board[y][x] == '*') {
        int dist = abs(cat_pos.x - x) + abs(cat_pos.y - y);
        if (dist < min_dist) min_dist = dist;
      }
    }
  }
  
  // Heuristic: minimum distance to nearest snack + remaining snacks
  return (min_dist == INT_MAX) ? INT_MAX : min_dist + snacks_remaining - 1;
}

bool apply_move_to_state(char direction, char board[MAX_DIM][MAX_DIM], Position* cat_pos, int* snacks_eaten) {
  int dir_index = -1;
  for (int i = 0; i < 4; ++i) {
    if (dir_chars[i] == direction) {
      dir_index = i;
      break;
    }
  }
  if (dir_index == -1) return false;

  int current_dx = dx[dir_index];
  int current_dy = dy[dir_index];
  Position start_pos = *cat_pos;
  *snacks_eaten = 0;

  while (true) {
    int next_x = cat_pos->x + current_dx;
    int next_y = cat_pos->y + current_dy;

    if (next_x < 0 || next_x >= width || next_y < 0 || next_y >= height) break;
    
    char next_cell = board[next_y][next_x];

    if (next_cell == '#' || next_cell == 'O' || next_cell == 'X') break;

    if (next_cell == '*') {
      (*snacks_eaten)++;
    }

    board[next_y][next_x] = 'X';
    cat_pos->x = next_x;
    cat_pos->y = next_y;
  }

  return !(cat_pos->x == start_pos.x && cat_pos->y == start_pos.y);
}

void copy_board(const char src[MAX_DIM][MAX_DIM], char dest[MAX_DIM][MAX_DIM]) {
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      dest[y][x] = src[y][x];
    }
  }
}

bool states_equal(const Node* a, const Node* b) {
  if (a->cat_pos.x != b->cat_pos.x || a->cat_pos.y != b->cat_pos.y ||
      a->snacks_remaining != b->snacks_remaining) return false;
  
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      if (a->board_state[y][x] != b->board_state[y][x]) return false;
    }
  }
  return true;
}

void solve_astar() {
  PriorityQueue* open_set = create_priority_queue(10000);
  if (!open_set) {
    fprintf(stderr, "Error: Failed to create priority queue.\n");
    return;
  }
  
  // Create initial node
  Node* start = create_node(initial_cat_pos, required_snacks_global, 
                           initial_board, "", 0, 0);
  if (!start) {
    destroy_priority_queue(open_set);
    return;
  }
  
  pq_insert(open_set, start);
  
  Node* visited[1000];
  int visited_count = 0;
  
  while (!pq_is_empty(open_set)) {
    Node* current = pq_extract_min(open_set);
    
    // Check if goal reached
    if (current->snacks_remaining == 0) {
      strcpy(solution_moves, current->move_sequence);
      solution_found = true;
      destroy_node(current);
      break;
    }
    
    // Check if already visited
    bool already_visited = false;
    for (int i = 0; i < visited_count; i++) {
      if (states_equal(current, visited[i])) {
        already_visited = true;
        break;
      }
    }
    
    if (already_visited) {
      destroy_node(current);
      continue;
    }
    
    // Add to visited
    if (visited_count < 1000) {
      visited[visited_count++] = current;
    }
    
    // Pruning: stop if too many moves
    if (current->move_length >= MAX_MOVES - 1) {
      continue;
    }
    
    // Generate successors
    for (int i = 0; i < 4; i++) {
      char new_board[MAX_DIM][MAX_DIM];
      copy_board(current->board_state, new_board);
      
      Position new_cat_pos = current->cat_pos;
      int snacks_eaten = 0;
      
      if (apply_move_to_state(dir_chars[i], new_board, &new_cat_pos, &snacks_eaten)) {
        char new_moves[MAX_MOVES];
        strcpy(new_moves, current->move_sequence);
        new_moves[current->move_length] = dir_chars[i];
        new_moves[current->move_length + 1] = '\0';
        
        int new_snacks_remaining = current->snacks_remaining - snacks_eaten;
        int new_g_cost = current->g_cost + 1;
        
        Node* successor = create_node(new_cat_pos, new_snacks_remaining, new_board,
                                     new_moves, current->move_length + 1, new_g_cost);
        
        if (successor) {
          pq_insert(open_set, successor);
        }
      }
    }
  }
  
  // Cleanup
  for (int i = 0; i < visited_count; i++) {
    destroy_node(visited[i]);
  }
  destroy_priority_queue(open_set);
}

int main() {
  if (!load_input()) {
    return 1;
  }

  solve_astar();

  if (solution_found) {
    print_output();
  }

  return 0;
}