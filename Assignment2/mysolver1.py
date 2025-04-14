import time

def make_board(puzzle):
    if len(puzzle) != 81:
        print("Error: puzzle string is wrog size")
        return None
    board=[]
    for i in range(9):
        row=[]
        for j in range(9):
            c=puzzle[i * 9 + j]
            if c=='.':
                row.append(0)
            elif c in '123456789':
                row.append(int(c))
            else:
                print("Error: bad charcter in puzzle")
                return None
        board.append(row)
    return board

# Checking if number fits
def is_ok(board,row,col,num):
    # Check row col
    for j in range(9):
        if board[row][j]==num and j!=col:
            return False
    for i in range(9):
        if board[i][col]==num and i!=row:
            return False

    # Checking 3x3
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num and (i, j) != (row, col):
                return False
    return True

# Get cells related to this one
def get_neighbors(row, col):
    neighbors=[]
    # Row and col neighbors
    for j in range(9):
        if j!=col:
            neighbors.append((row,j))
    for i in range(9):
        if i!=row:
            neighbors.append((i, col))

    # Box neighbors
    box_row= (row//3)*3
    box_col=(col//3)*3
    for i in range(box_row, box_row +3):
        for j in range(box_col,box_col +3):
            if (i,j)!=(row,col):
                neighbors.append((i,j))
    return neighbors


def ac3(board):
    # Seting possible vals for each cell
    possible = {}
    for i in range(9):
        for j in range(9):
            if board[i][j]==0:
                possible[(i,j)]=[1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                possible[(i,j)] =[board[i][j]]
    
    # arc listss
    arcs =[]
    for i in range(9):
        for j in range(9):
            neighbors =get_neighbors(i, j)
            for n in neighbors:
                arcs.append(((i,j),n))
    
    # Process arcs slowly
    while arcs:
        (x_row,x_col), (y_row,y_col) = arcs.pop(0)  # Slow pop
        changed =False
        x_vals =possible[(x_row,x_col)].copy()
        for val in x_vals:
            y_vals=possible[(y_row,y_col)]
            if all(val==y_val for y_val in y_vals):
                possible[(x_row,x_col)].remove(val)
                changed=True
        if changed:
            if not possible[(x_row, x_col)]:
                return False,possible
            # Add arcs again
            neighbors=get_neighbors(x_row, x_col)
            for n in neighbors:
                if n !=(y_row,y_col):
                    arcs.append((n,(x_row, x_col)))
    
    return True, possible

#to find empty cells
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j]==0:
                return i, j
    return None

#Backtracking
def backtrack(board, possible):
    empty =find_empty(board)
    if not empty:
        return True
    row, col =empty
    for num in range(1, 10):
        if is_ok(board, row, col, num):
            board[row][col] = num
            if backtrack(board, possible):
                return True
            board[row][col] = 0
    return False


def solve_sudoku(puzzle):
    start = time.time()
    board = make_board(puzzle)
    if board is None:
        return None, time.time() -start
    for i in range(9):
        for j in range(9):
            if board[i][j]!=0:
                num = board[i][j]
                board[i][j]=0
                if not is_ok(board, i, j, num):
                    return None, time.time() - start
                board[i][j] =num
    #Running ac3
    ok, possible = ac3(board)
    if not ok:
        return None, time.time() - start
    #filling easy cells
    for i in range(9):
        for j in range(9):
            if board[i][j]==0 and len(possible[(i, j)])==1:
                board[i][j]=possible[(i, j)][0]
    #Backtracking
    backtrack(board, possible)
    return board, time.time()-start

#board to string 
def board_to_string(board):
    if board is None:
        return "Nosolution"
    result=""
    for i in range(9):
        for j in range(9):
            result+=str(board[i][j])
    return result

# Main program
try:
    file =open('sudoku.txt', 'r')
    puzzles=[]
    for line in file:
        line=line.strip()
        if line:
            puzzles.append(line)
    file.close()
    
    for index in range(len(puzzles)):
        puzzle = puzzles[index]
        print("\n Puzzle", index + 1, ": ")
        print("Puzzle string :", puzzle)
        print("Solvingggg...")
        solution, elapsed = solve_sudoku(puzzle)
        print("Solution :", board_to_string(solution))
        print("Total Time :", "{:.5f}s".format(elapsed))
except:
    print("Error: something went wrong")