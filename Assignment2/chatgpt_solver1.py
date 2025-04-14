import time
from collections import deque

def make_board(s):
    """Convert puzzle string to 9x9 grid."""
    if len(s) != 81 or not all(c in '.123456789' for c in s):
        raise ValueError("Invalid puzzle string")
    board = [[int(c) if c != '.' else 0 for c in s[i*9:(i+1)*9]] for i in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0 and not is_valid(board, i, j, board[i][j]):
                raise ValueError("Initial board has conflicts")
    return board

def precompute_neighbors():
    """Precompute neighbors for each cell (row, column, box)."""
    neighbors = {}
    for i in range(9):
        for j in range(9):
            n = set()
            for y in range(9):
                if y != j:
                    n.add((i, y))
            for x in range(9):
                if x != i:
                    n.add((x, j))
            start_i, start_j = (i // 3) * 3, (j // 3) * 3
            for x in range(start_i, start_i + 3):
                for y in range(start_j, start_j + 3):
                    if (x, y) != (i, j):
                        n.add((x, y))
            neighbors[(i, j)] = list(n)
    return neighbors

NEIGHBORS = precompute_neighbors()

def ac3(board):
    """Enforce arc consistency using AC-3."""
    domains = {(i, j): [board[i][j]] if board[i][j] != 0 else list(range(1, 10))
               for i in range(9) for j in range(9)}
    queue = deque([((i, j), (ni, nj)) for i in range(9) for j in range(9)
                   for (ni, nj) in NEIGHBORS[(i, j)]])
    
    while queue:
        (xi, xj), (yi, yj) = queue.popleft()
        revised = False
        original = domains[(xi, xj)].copy()
        for val in original:
            if not any(val != d for d in domains[(yi, yj)]):
                domains[(xi, xj)].remove(val)
                revised = True
        if revised:
            if not domains[(xi, xj)]:
                return False, domains
            for (ni, nj) in NEIGHBORS[(xi, xj)]:
                if (ni, nj) != (yi, yj):
                    queue.append(((ni, nj), (xi, xj)))
    return True, domains

def is_valid(board, i, j, num):
    """Check if placing num at (i, j) is valid."""
    for y in range(9):
        if board[i][y] == num and y != j:
            return False
    for x in range(9):
        if board[x][j] == num and x != i:
            return False
    start_i, start_j = (i // 3) * 3, (j // 3) * 3
    for x in range(start_i, start_i + 3):
        for y in range(start_j, start_j + 3):
            if board[x][y] == num and (x, y) != (i, j):
                return False
    return True

def find_empty_mrv(board, domains):
    """Find the empty cell with the minimum remaining values (MRV)."""
    min_vals, best_pos = float('inf'), None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                num_vals = len(domains[(i, j)])
                if num_vals < min_vals:
                    min_vals, best_pos = num_vals, (i, j)
    return best_pos

def backtrack(board, domains):
    """Solve using backtracking with MRV heuristic."""
    pos = find_empty_mrv(board, domains)
    if not pos:
        return True
    i, j = pos
    # Copy domains to avoid modifying during backtracking
    for num in domains[(i, j)].copy():
        if is_valid(board, i, j, num):
            board[i][j] = num
            # Update domains temporarily for neighbors
            old_domains = {k: v.copy() for k, v in domains.items()}
            for (ni, nj) in NEIGHBORS[(i, j)]:
                if num in domains[(ni, nj)]:
                    domains[(ni, nj)].remove(num)
            if backtrack(board, domains):
                return True
            # Restore board and domains
            board[i][j] = 0
            domains.update(old_domains)
    return False

def solve_sudoku(puzzle):
    """Solve the puzzle and return the solution grid and elapsed time."""
    start = time.time()
    try:
        board = make_board(puzzle)
        success, domains = ac3(board)
        if not success:
            return None, time.time() - start
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and len(domains[(i, j)]) == 1:
                    board[i][j] = domains[(i, j)][0]
                    # Update neighbors' domains
                    for (ni, nj) in NEIGHBORS[(i, j)]:
                        if board[i][j] in domains[(ni, nj)]:
                            domains[(ni, nj)].remove(board[i][j])
        success = backtrack(board, domains)
        return board if success else None, time.time() - start
    except ValueError as e:
        return None, time.time() - start
    except Exception as e:
        print(f"Error in solving: {e}")
        return None, time.time() - start

def board_to_string(board):
    """Convert a 9x9 grid to an 81-character string."""
    if board is None:
        return "No solution"
    return ''.join(str(cell) for row in board for cell in row)

try:
    with open('sudoku.txt', 'r') as f:
        puzzles = [line.strip() for line in f]
    for idx, puzzle in enumerate(puzzles, 1):
        print(f"\n--- Puzzle {idx} ---")
        print(f"Puzzle string: {puzzle}")
        print("Solving...")
        solution, elapsed = solve_sudoku(puzzle)
        print(f"Solution: {board_to_string(solution)}")
        print(f"Total Time: {elapsed:.5f}s")
except FileNotFoundError:
    print("Error: sudoku.txt not found")
except ValueError as e:
    print(f"Error: {e}")