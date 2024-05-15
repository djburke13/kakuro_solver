## Program works with MAC

import sys
import time

start_time = 0
num_backtracks = 0

def find_potentials(clue, clue_length): 

	potentials = set()

	# Find minimum and maximum potential values for each sum
	max_potential = min(int(clue - ((clue_length * (clue_length - 1)) / 2)), 9)
	min_potential = max(int(clue - (9 * (clue_length - 1)) + (((clue_length - 1) * (clue_length - 2)) / 2)) , 1)

	potentials = {x for x in range(min_potential, max_potential + 1)}

	# Special case for clues who have a length of 2
	if clue_length == 2 and clue % 2 == 0:
		potentials.remove(clue / 2)
	elif clue_length > 2:

		# Special case for the sum one greater than the minimum for that length
		minval_for_length = (clue_length * (clue_length + 1)) / 2
		if clue == (minval_for_length + 1):
			potentials.remove(clue_length)

		# Special case for the sum one less than the maximum for that length
		maxval_for_length = 0
		val = 10
		for _ in range(0, clue_length):
			val -= 1
			maxval_for_length += val

		if clue == (maxval_for_length - 1):
			potentials.remove(val)

	return potentials

def init_board(): 
	f = open(sys.argv[1], 'r')   ##  "4x4_medium.txt" sys.argv[1]

	board = []
	horizontal_board = []
	vertical_board = []
	# Populate the text field and boards
	for line in f.readlines():
		tokens = line.split()
		temp_line = []
		h_line = []
		v_line = []
		for token in tokens:
			idx = token.find('|')
			# Sum clue square, need to parse further
			if idx != -1:
				first_token = token[:idx]
				second_token = token[idx+1:]

				# Change character values into integers to do math with
				if first_token != '#':
					first_token = int(first_token)
				if second_token != '#':
					second_token = int(second_token)

				temp_line.append([first_token, second_token])
				h_line.append(second_token)
				v_line.append(first_token)
			# Blank square or empty cell
			else:
				h_line.append(token)
				v_line.append(token)
				temp_line.append(token)
		horizontal_board.append(h_line)
		vertical_board.append(v_line)
		board.append(temp_line)

	## use horizontal board to find potential sets of numbers for horizontal clues
	for i in range(0, len(horizontal_board)):
		for j in range(0, len(horizontal_board[i])):

			# Only need to find empty squares
			if horizontal_board[i][j] == '0':

				potentials = set()

				# Checking if the square immediately to its left is a sum clue
				if not isinstance(horizontal_board[i][j-1], set):

					clue = int(horizontal_board[i][j-1])

					# Determine how many cells are related to the given clue
					clue_length = 1
					while (j + clue_length) < len(horizontal_board[i]) and horizontal_board[i][j + clue_length] == '0':
						clue_length += 1

					# Find potentials for current clue
					potentials = find_potentials(clue, clue_length)

					# Add new list to the horizontal board
					horizontal_board[i][j] = potentials
				else:

					# Entry for empty cell should be exactly the same as the previous cell in the same row
					horizontal_board[i][j] = horizontal_board[i][j-1]

	## use vertical board to find potential sets of numbers for vertical clues
	for i in range(0, len(vertical_board)):
		for j in range(0, len(vertical_board[i])):

			# Only need to find empty squares
			if vertical_board[i][j] == '0':

				potentials = set()

				# Checking if the square immediately to its left is a sum clue
				if not isinstance(vertical_board[i-1][j], set):

					clue = int(vertical_board[i-1][j])

					# Determine how many cells are related to the given clue
					clue_length = 1
					while (i + clue_length) < len(vertical_board) and vertical_board[i + clue_length][j] == '0':
						clue_length += 1

					# Find potentials of current clue
					potentials = find_potentials(clue, clue_length)

					# Add new list to the vertical board
					vertical_board[i][j] = potentials
				else:

					# Entry for empty cell should be exactly the same as the previous cell in the same column
					vertical_board[i][j] = vertical_board[i-1][j]

	# Combine horizontal and vertical boards to create a single board, where empty cells have 
	# all possible values for that cell
 
	empty_cells = set()
 
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):

			# Only need to find empty squares
			if board[i][j] == '0':

				empty_cells.add((i, j))
				
				horizontal_entry = horizontal_board[i][j]
				vertical_entry = vertical_board[i][j]

				board[i][j] = set.intersection(horizontal_entry, vertical_entry)

	return(board, empty_cells)

def print_board(board, clue_positions): 

	end_time = time.time_ns()
 
	print("Completed puzzle")

	RESET = '\033[0m'
 
	for i in range(0, len(board)):
		line = ""
		for j in range(0, len(board[i])):
			
			cell = board[i][j]
			temp_line = ""
			temp_cnt = 0

			if isinstance(cell, list):
				COLOR = '\033[34m'
				temp_line += str(clue_positions[(i, j)][0])
				temp_line += '|'
				temp_line += str(clue_positions[(i, j)][1])
				temp_cnt += len(temp_line)
				line += COLOR
				line += temp_line
				line += RESET
			elif cell == '#':
				line += str(board[i][j])
				temp_cnt += 1
			else:
				COLOR = '\033[32m'
				temp_line = str(board[i][j])
				temp_cnt += 1
				line += COLOR
				line += temp_line
				line += RESET

			while temp_cnt % 6 != 0:
				line += ' '
				temp_cnt += 1

		print(line)

	# print("Total time: ", (end_time - start_time)/1000000000)
	# print("Number of Backtracks: ", num_backtracks)

	## exit program
	exit()

def update_values(board, horizontal_clue_loc, vertical_clue_loc, potential_val):

	# A list of tuples representing cells and the potential values that were removed due to the update
	removed_values = []
	stop = False

	# Vertical clue checking
	vr = vertical_clue_loc[0]
	vc = vertical_clue_loc[1]

	temp_cnt = 1
	indexes = []

	# Find number of cells associated with the clue
	while (vr + temp_cnt) < len(board) and (isinstance(board[vr + temp_cnt][vc], int) or isinstance(board[vr + temp_cnt][vc], set)):
		if isinstance(board[vr + temp_cnt][vc], set):
			indexes.append(vr + temp_cnt)
		temp_cnt += 1

	cells_remaining = len(indexes)
	clue = board[vr][vc][0]

	if cells_remaining > 0:

		# Find potential values for the clue and remaining length
		potentials = find_potentials(clue, cells_remaining)
		potentials.discard(potential_val)

		# For every cell that still hasn't been assigned a value, update the set of potential values
		for k in indexes:
			diff = board[k][vc] - potentials
			if len(diff) > 0:
				removed_values.append([(k, vc), diff])
			board[k][vc] = board[k][vc].intersection(potentials)

			# Check to see if intersection resulted in an empty set
			if len(board[k][vc]) == 0:
				stop = True

	# Horizontal clue checking
	hr = horizontal_clue_loc[0]
	hc = horizontal_clue_loc[1]

	temp_cnt = 1
	indexes = []

	# Find number of cells associated with the clue
	while (hc + temp_cnt) < len(board[hr]) and (isinstance(board[hr][hc + temp_cnt], int) or isinstance(board[hr][hc + temp_cnt], set)):
		if isinstance(board[hr][hc + temp_cnt], set):
			indexes.append(hc + temp_cnt)
		temp_cnt += 1

	cells_remaining = len(indexes)
	clue = board[hr][hc][1]

	if cells_remaining > 0:

		# Find potential values for the clue and remaining length
		potentials = find_potentials(clue, cells_remaining)
		potentials.discard(potential_val)

		# For every cell that still hasn't been assigned a value, update the set of potential values
		for k in indexes:
			diff = board[hr][k] - potentials
			if len(diff) > 0:
				removed_values.append([(hr, k), diff])
			board[hr][k] = board[hr][k].intersection(potentials)

			# Check to see if intersection resulted in an empty set
			if len(board[hr][k]) == 0:
				stop = True

	# Return a list of tuples that describe the locations on the board and what was removed from their potential sets
	return removed_values, stop

def find_MRV(board, empty_cells):

	min_length = 10
	best_location = ()
	
	# Iterate through all empty cells to find the best cell
	for cell in empty_cells:

		row = cell[0]
		col = cell[1]

		# Determine the length of potential locations of each empty cell
		potentials_length = len(board[row][col])
		if potentials_length < min_length:
			min_length = potentials_length
			best_location = cell

	return board[best_location[0]][best_location[1]], best_location

# Checks the board to see if all sum clues are satisfied
def board_check(board): 
	
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):

			cell = board[i][j]

			# Check to see if cell is a sum clue
			if isinstance(cell, list):

				# Check if column sum is 0
				if isinstance(cell[0], int) and cell[0] != 0:
					return False

				# Check if row sum is 0
				if isinstance(cell[1], int) and cell[1] != 0:
					return False
				
	return True

## Additional check for MAC
def MAC_check(board, horizontal_clue_loc, vertical_clue_loc):
	
	# Vertical clue checking
	vr = vertical_clue_loc[0]
	vc = vertical_clue_loc[1]

	temp_cnt = 1
	list_of_stops = []

	# Find the number of cells associated with the clue
	while (vr + temp_cnt) < len(board) and (isinstance(board[vr + temp_cnt][vc], int) or isinstance(board[vr + temp_cnt][vc], set)):
		if isinstance(board[vr + temp_cnt][vc], set):

			## Try to solve the board and ensure that the board remains solvable with all possible values of 
			## this certain unsolved cell
   
			best_cell = board[vr + temp_cnt][vc]

			for value in best_cell:

				stop = False
				board[vr + temp_cnt][vc] = value

				# Removing the value assigned to the empty cell from the current row and column
				temp_row = vr + temp_cnt
				temp_col = vc
	
				## Go left and find where sum clue starts -> iterate through row until end of board or blank/sum cell
				while not isinstance(board[vr + temp_cnt][temp_col], list):
					temp_col -= 1

				board[vr + temp_cnt][temp_col][1] -= value
				
				# Check if sum is now negative (impossible for a solution
				if board[vr + temp_cnt][temp_col][1] < 0: 
					stop = True

				## Go up and find where sum clue starts -> iterate through col until end of board or blank/sum cell
				while not isinstance(board[temp_row][vc], list):
					temp_row -= 1

				board[temp_row][vc][0] -= value

				# Check if sum becomes negative (impossible for solution)
				if board[temp_row][vc][0] < 0:
					stop = True

				# Updates the potential values for unfilled cells
				if stop:
					list_of_stops.append(stop)
				else:
					mac_removed_values, extra_stop = update_values(board, (vr + temp_cnt, temp_col), (temp_row, vc), value)

				# Return board back to state
				temp_row = vr + temp_cnt
				temp_col = vc
				## Go left and find where sum clue starts -> iterate through row until end of board or blank/sum cell
				while not isinstance(board[vr + temp_cnt][temp_col], list):
					temp_col -= 1

				board[vr + temp_cnt][temp_col][1] += value

				## Go up and find where sum clue starts -> iterate through col until end of board or blank/sum cell
				while not isinstance(board[temp_row][vc], list):
					temp_row -= 1

				board[temp_row][vc][0] += value

				# Re-add items that were removed for MAC checking back to the potential values
				for item in mac_removed_values:
					row = item[0][0]
					col = item[0][1]

					board[row][col] = board[row][col].union(item[1])

				list_of_stops.append(extra_stop)

				board[vr + temp_cnt][vc] = best_cell
			
		temp_cnt += 1

	# Horizontal clue checking
	hr = horizontal_clue_loc[0]
	hc = horizontal_clue_loc[1]

	temp_cnt = 1

	# Find the number of cells associated with the clue
	while (hc + temp_cnt) < len(board[hr]) and (isinstance(board[hr][hc + temp_cnt], int) or isinstance(board[hr][hc + temp_cnt], set)):
		if isinstance(board[hr][hc + temp_cnt], set):

			## Try to solve the board and ensure that the board remains solvable with all possible values of 
			## this certain unsolved cell
   
			best_cell = board[hr][hc + temp_cnt]

			for value in best_cell:

				stop = False
				board[hr][hc + temp_cnt] = value

				# Removing the value assigned to the empty cell from the current row and column
				temp_row = hr
				temp_col = hc + temp_cnt
	
				## Go left and find where sum clue starts -> iterate through row until end of board or blank/sum cell
				while not isinstance(board[hr][temp_col], list):
					temp_col -= 1

				board[hr][temp_col][1] -= value
				
				# Check if sum is now negative (impossible for a solution
				if board[hr][temp_col][1] < 0: 
					stop = True

				## Go up and find where sum clue starts -> iterate through col until end of board or blank/sum cell
				while not isinstance(board[temp_row][hc + temp_cnt], list):
					temp_row -= 1

				board[temp_row][hc + temp_cnt][0] -= value

				# Check if sum becomes negative (impossible for solution)
				if board[temp_row][hc + temp_cnt][0] < 0:
					stop = True

				# Updates the potential values for unfilled cells
				if stop: 
					list_of_stops.append(stop)
				else:
					mac_removed_values, extra_stop = update_values(board, (hr, temp_col), (temp_row, hc + temp_cnt), value)

				# Return board back to state
				temp_row = hr
				temp_col = hc + temp_cnt
				## Go left and find where sum clue starts -> iterate through row until end of board or blank/sum cell
				while not isinstance(board[hr][temp_col], list):
					temp_col -= 1

				board[hr][temp_col][1] += value

				## Go up and find where sum clue starts -> iterate through col until end of board or blank/sum cell
				while not isinstance(board[temp_row][hc + temp_cnt], list):
					temp_row -= 1

				board[temp_row][hc + temp_cnt][0] += value

				# Re-add items that were removed for MAC checking back to the potential values
				for item in mac_removed_values:
					row = item[0][0]
					col = item[0][1]

					board[row][col] = board[row][col].union(item[1])

				list_of_stops.append(extra_stop)

				board[hr][hc + temp_cnt] = best_cell
			
		temp_cnt += 1

	# If all possible future assignments end with a dead end, then current assignment is incorrect
	if len(list_of_stops) > 0  and all(list_of_stops):
		return True

	return False

def solve_puzzle(board, empty_cells, clue_positions):

	global num_backtracks
	
	# If we have successfully filled all empty cells, then print the solution
	if len(empty_cells) == 0: 

		if board_check(board):
			print_board(board, clue_positions)
		else:
			return False

	else:

		# Find empty cell with fewest possible values
		best_cell, best_location = find_MRV(board, empty_cells)

		if len(best_cell) == 0:
			num_backtracks += 1
			return False

		# Iterate over all possible values in that cell
		for potential_val in best_cell:

			empty_cells.remove(best_location)

			row_loc = best_location[0]
			col_loc = best_location[1]

			board[row_loc][col_loc] = potential_val
			stop = False

			# Removing the value assigned to the empty cell from the current row and column
			temp_row = row_loc
			temp_col = col_loc
   
			## Go left and find where sum clue starts -> iterate through row until end of board or blank/sum cell
			while not isinstance(board[row_loc][temp_col], list):
				temp_col -= 1

			board[row_loc][temp_col][1] -= potential_val
			
			# Check if sum is now negative (impossible for a solution
			if board[row_loc][temp_col][1] < 0: 
				stop = True

			## Go up and find where sum clue starts -> iterate through col until end of board or blank/sum cell
   
			while not isinstance(board[temp_row][col_loc], list):
				temp_row -= 1

			board[temp_row][col_loc][0] -= potential_val

			# Check if sum becomes negative (impossible for solution)
			if board[temp_row][col_loc][0] < 0:
				stop = True

			# Updates the potential values for unfilled cells
			removed_values, extra_stop = update_values(board, (row_loc, temp_col), (temp_row, col_loc), potential_val)

			mac_stop = False
			if not extra_stop:
				mac_stop = MAC_check(board, (row_loc, temp_col), (temp_row, col_loc))

			# Recursively call the method while the algorithm can give valid assignments to empty cells
			if (not stop and not extra_stop and not mac_stop and solve_puzzle(board, empty_cells, clue_positions)):
				return True
			
			# Will revert to how the board and potential values were before the recursion if the 
			# recursion returns a false value, meaning the value assignment was incorrect
   
			# From best_location, find sum clue for row and column and iterate through rows and columns
			# Check to see, for each location, if it is contained within affected locations so the value can
			# be added back into the potential values
			# For all cells in the row/column, add the potential_value to the row/column total contained within the cell
			temp_row = row_loc
			temp_col = col_loc

			## Go left and find where sum clue starts -> iterate through row until end of board or blank/sum cell
			while not isinstance(board[row_loc][temp_col], list):
				temp_col -= 1

			board[row_loc][temp_col][1] += potential_val

			## Go up and find where sum clue starts -> iterate through col until end of board or blank/sum cell
   
			while not isinstance(board[temp_row][col_loc], list):
				temp_row -= 1

			board[temp_row][col_loc][0] += potential_val

			for item in removed_values:
				row = item[0][0]
				col = item[0][1]

				board[row][col] = board[row][col].union(item[1])

			# Return cell back to original state and add it back to set of empty cells
			empty_cells.add(best_location)
			board[row_loc][col_loc] = best_cell

		# Increments the number of backtracks and returns false, meaning the algorithm could not find a 
		# valid assignment for a value given the current board status
		num_backtracks += 1
		return False

if __name__ == "__main__":

	num_backtracks = 0
	start_time = time.time_ns()

	# Initialize board and potential values
	board, empty_cells = init_board()

	clue_positions = dict()

	# Creating a list of all clue positions so printing is easier
	for i in range(0, len(board)):
		for j in range(0, len(board[i])): 

			cell = board[i][j]
			if isinstance(cell, list):

				if cell[0] != '#' and cell[1] != '#':
					clue_positions[(i, j)] = (board[i][j][0], board[i][j][1])
				elif cell[0] != '#':
					clue_positions[(i, j)] = (board[i][j][0], '#')
				elif cell[1] != '#':
					clue_positions[(i, j)] = ('#', board[i][j][1])

	# Solve the puzzle
	solution = solve_puzzle(board, empty_cells, clue_positions)

	if not solution:
		print("Board does not have a solution")
	
