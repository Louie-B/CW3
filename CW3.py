import time
grid = [
		[1, 0, 0, 2],
		[0, 0, 1, 0],
		[0, 1, 0, 4],
		[0, 0, 0, 1]]
grid2 = [
[0, 0, 0, 2, 6, 0, 7, 0, 1],
[6, 8, 0, 0, 7, 0, 0, 9, 0],
[1, 9, 0, 0, 0, 4, 5, 0, 0],
[8, 2, 0, 1, 0, 0, 0, 4, 0],
[0, 0, 4, 6, 0, 2, 9, 0, 0],
[0, 5, 0, 0, 0, 3, 0, 2, 8],
[0, 0, 9, 3, 0, 0, 0, 7, 4],
[0, 4, 0, 0, 5, 0, 0, 3, 6],
[7, 0, 3, 0, 1, 8, 0, 0, 0],
]
grid3 = [
[0, 2, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 6, 0, 4, 0, 0, 0, 0],
[5, 8, 0, 0, 9, 0, 0, 0, 3],
[0, 0, 0, 0, 0, 3, 0, 0, 4],
[4, 1, 0, 0, 8, 0, 6, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 9, 5],
[2, 0, 0, 0, 1, 0, 0, 8, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 3, 1, 0, 0, 8, 0, 5, 7],
]

def check_section(section, n):

	if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n+1)]):
		return True
	return False

def get_squares(grid, n_rows, n_cols):

	squares = []
	for i in range(n_cols):
		rows = (i*n_rows, (i+1)*n_rows)
		for j in range(n_rows):
			cols = (j*n_cols, (j+1)*n_cols)
			square = []
			for k in range(rows[0], rows[1]):
				line = grid[k][cols[0]:cols[1]]
				square +=line
			squares.append(square)


	return(squares)

#To complete the first assignment, please write the code for the following function
def check_solution(grid, n_rows, n_cols):
	'''
	This function is used to check whether a sudoku board has been correctly solved

	args: grid - representation of a suduko board as a nested list.
	returns: True (correct solution) or False (incorrect solution)
	'''
	n = n_rows*n_cols

	for row in grid:
		if check_section(row, n) == False:
			return False

	for i in range(n_rows**2):
		column = []
		for row in grid:
			column.append(row[i])

		if check_section(column, n) == False:
			return False

	squares = get_squares(grid, n_rows, n_cols)
	for square in squares:
		if check_section(square, n) == False:
			return False

	return True


def find_empty(grid):
	'''
	This function returns the index (i, j) to the first zero element in a sudoku grid
	If no such element is found, it returns None

	args: grid
	return: A tuple (i,j) where i and j are both integers, or None
	'''

	for i in range(len(grid)):
		row = grid[i]
		for j in range(len(row)):
			if grid[i][j] == 0:
				return (i, j)

	return None


def recursive_solve(grid, n_rows, n_cols):
	'''
	This function uses recursion to exhaustively search all possible solutions to a grid
	until the solution is found

	args: grid, n_rows, n_cols
	return: A solved grid (as a nested list), or None
	'''

	#N is the maximum integer considered in this board
	n = n_rows*n_cols
	#Find an empty place in the grid
	empty = find_empty(grid)

	#If there's no empty places left, check if we've found a solution
	if not empty:
		#If the solution is correct, return it.
		if check_solution(grid, n_rows, n_cols):
			return grid 
		else:
			#If the solution is incorrect, return None
			return None
	else:
		row, col = empty 
	list_column = []
	list_column_grid = []
	
	for rows in range(n): 
		for coll in range(n):
			list_column.append(grid[coll][rows])
		list_column_grid.append(list_column)
		list_column = []
	#To find out what square the number is in
	x = (col)//n_rows
	y = (row)//n_rows
	num_of_square = x + (n_cols*y)
	#Loop through possible values
	for i in range(1, n+1):
		if grid[row].count(i) == 0 and list_column_grid[col].count(i) == 0 and get_squares(grid,n_rows,n_cols)[num_of_square].count(i) == 0:
			#Place the value into the grid
			grid[row][col] = i
			#Recursively solve the grid
			ans = recursive_solve(grid, n_rows, n_cols)

			#If we've found a solution, return it
			if ans:
				return ans 

			#If we couldn't find a solution, that must mean this value is incorrect.
			#Reset the grid for the next iteration of the loop
			grid[row][col] = 0 

	#If we get here, we've tried all possible values. Return none to indicate the previous value is incorrect.
	return None

def random_solve(grid, n_rows, n_cols, max_tries=50000):
	'''
	This function uses random trial and error to solve a Sudoku grid

	args: grid, n_rows, n_cols, max_tries
	return: A solved grid (as a nested list), or the original grid if no solution is found
	'''

	for i in range(max_tries):
		possible_solution = fill_board_randomly(grid, n_rows, n_cols)
		if check_solution(possible_solution, n_rows, n_cols):
			return possible_solution

	return grid

def fill_board_randomly(grid, n_rows, n_cols):
	'''
	This function will fill an unsolved Sudoku grid with random numbers

	args: grid, n_rows, n_cols
	return: A grid with all empty values filled in
	'''
	n = n_rows*n_cols
	#Make a copy of the original grid
	filled_grid = copy.deepcopy(grid)

	#Loop through the rows
	for i in range(len(grid)):
		#Loop through the columns
		for j in range(len(grid[0])):
			#If we find a zero, fill it in with a random integer
			if grid[i][j] == 0:
				filled_grid[i][j] = random.randint(1, n)

	return filled_grid 

def explain_func(grid, n_rows, n_cols):
	n = n_rows * n_cols
	x_cords = []
	y_cords = []	
	for rows in range(n): 
		for coll in range(n):
			if grid[rows][coll] == 0:
				x_cords.append(rows)
				y_cords.append(coll)
	solved = recursive_solve(grid, n_rows, n_cols)		
	for i in range(len(x_cords)):
		print("Put a " + str(solved[(x_cords[i])][(y_cords[i])]) + " in posistion (" + str(x_cords[i]) + ", " +  str(y_cords[i]) + ")")
	print(solved)
	
	
	
	'''
	not sure how to add the second part however i am going to do it by getting the posistions of the zeros in the inputed
	grid then finding what they are replaced with.
	'''
def solve(grid, n_rows, n_cols,explain = False):
	'''
	Solve function for Sudoku coursework.
	Comment out one of the lines below to either use the random or recursive solver
	'''
	if explain == True:
		explain_func(grid, n_rows, n_cols)
	#return random_solve(grid, n_rows, n_cols)
	else:
		return recursive_solve(grid, n_rows, n_cols)

def file(Input, output):
        grid_input=[]
        with open(Input, "r") as my_file:
                data = my_file.read().replace(",","")
                data = data.replace(" ","")
                data = data.replace("\n","")
                no_of_characters = len(data)
                grid_size = no_of_characters**0.5
                temp_array = []
                count = 0
                for number in data:
                        count+=1
                        if (count == grid_size):
                                count = 0
                                temp_array.append(int(number))
                                grid_input.append(temp_array)
                                temp_array = []
                        else:
                                temp_array.append(int(number))
        if (grid_size == 6):
                n_rows = 2
                n_cols = 3
        else:
                n_rows, n_cols = int(grid_size**0.5),int(grid_size**0.5)

        grid_solved = solve(grid_input, n_rows, n_cols)

        with open(output, "w") as write_file:
                for line in grid_solved:
                        write_file.write(str(line))
                        write_file.write('\n')
                
                
file("easy1.txt","easy1solved.txt")

solve(grid3,3,3,explain = True)
