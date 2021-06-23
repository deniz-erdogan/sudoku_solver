from pprint import PrettyPrinter, pprint

# Sudoku text based logic. 

# Find and return first empty cell in the board
def find_empty(board):
	for row in range(9):
		for col in range(9):
			if board[row][col] == 0:
				return (row, col)

	return None


# Check if a slot is valid for a number
def is_valid(board, pos, num):
	for i in range(9):
		if board[i][pos[1]] == num and (i,pos[1]) != pos:
			return False

	for i in range(9):
		if board[pos[0]][i] == num and (pos[0],i) != pos:
			return False

	start_row = pos[0] - (pos[0] % 3)
	start_column = pos[1] - (pos[1] % 3)

	for i in range(3):
		for j in range(3):
			if board[start_row+i][start_column+j] == num and (start_row+i, start_column+j) != pos:
				return False

	return True


# Solve board with backtracking
def solve(board):
	empty_slot = find_empty(board)

	if not empty_slot:
		return True

	for num in range(1,10):
		if is_valid(board, empty_slot, num):
			board[empty_slot[0]][empty_slot[1]] = num

			if solve(board):
				return True
			
			board[empty_slot[0]][empty_slot[1]] = 0
	
	return False


def print_board(board):
	pp = PrettyPrinter(indent=4, width=40, compact=True)
	pp.pprint(board)


if __name__ == "__main__":
	board =  [
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 8, 0, 0, 0, 7, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 3],
        [0, 9, 0, 4, 0, 0, 0, 7, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0]
    ]

	solve(board)
	print_board(board)