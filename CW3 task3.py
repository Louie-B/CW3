#To use this code, call improved_solve(<grid>, <row length>, <column length>)
import copy


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

	for i in range(n_rows):
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


def generate_range(grid, row, col):
    '''
    This function replaces all the zeros in a grid into a list containing numbers from 1 to the maximum number in a grid.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: grid(The updated grid)
    '''
    max = row * col
    for i in range(row * col):
        for j in range(col * row):
            if not grid[i][j]:
                grid[i][j] = [(i + 1) for i in range(max)]
    return grid


def remove(item, num):
    '''
    This function will remove a number from a set. If the number is not in the set, it will pass.
    args: item - the set.
		  num - the number that will be removed from item.
    returns: item(the updated item)
    '''
    try:
        item.remove(num)
        return item
    except ValueError:
        return item
    

def simplify(grid, row, col):
    '''
    This function will search for sets of length 1 in a grid and change it into the integer. 
    If the solution was wrong, the function will return False.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: grid(The updated grid) or False(if an empty set appeared)
    '''
    for i in range(row * col):
        for j in range(col * row):
            if not isinstance(grid[i][j], int) and len(grid[i][j]) == 1:
                grid[i][j] = grid[i][j][0]
            elif not isinstance(grid[i][j], int) and len(grid[i][j]) == 0:
                return False
    return grid


def find_least(grid, row, col):
    '''
    This function searches for the set in a grid with the least length, and returns its list index.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: row_num(the row index of the least length set) and col_num(the column index of the least length set)
    '''
    row_count = 0
    col_count = 0
    least_lenth = row * col
    row_num = 0
    col_num = 0
    while row_count < row * col:
        while col_count < col * row:
            if isinstance(grid[row_count][col_count], list) and len(grid[row_count][col_count]) < least_lenth:
                row_num = row_count
                col_num = col_count
                least_lenth = len(grid[row_count][col_count])
            col_count += 1
        col_count = 0
        row_count += 1
    return row_num, col_num
    

def check_row(grid, row, col):
    '''
    Start eliminating by row elements.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: result(The updated grid)
    '''
    appeared = []
    blank = []
    for i in range(row * col):
        for j in range(col * row):
            if isinstance(grid[i][j], int):
                appeared.append(grid[i][j])
            else:
                blank.append(j)
        for j in blank:
            for k in appeared:
                remove(grid[i][j], k)
        appeared = []
        blank = []
    result = simplify(grid, row, col)
    return result
    

def check_col(grid, row, col):
    '''
    Start eliminating by column elements.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: result(The updated grid)
    '''
    appeared = []
    blank = []
    for i in range(row * col):
        for j in range(col * row):
            if isinstance(grid[j][i], int):
                appeared.append(grid[j][i])
            else:
                blank.append(j)
        for j in blank:
            for k in appeared:
                remove(grid[j][i], k)
        appeared = []
        blank = []
    result = simplify(grid, row, col)
    return result


def check_box(grid, row, col):
    '''
    Start eliminating by square elements.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: result(The updated grid)
    '''
    appeared = []
    blank_row = []
    blank_col = []
    row_count = 0
    column_count = 0
    while column_count < row:
        while row_count < col:
            for i in range(row):
                for j in range(col):
                    if isinstance(grid[i + row * row_count][j + col * column_count], int):
                        appeared.append(grid[i + row * row_count][j + col * column_count])
                    else:
                        blank_row.append(i + row * row_count)
                        blank_col.append(j + col * column_count)
            for i in range(len(blank_row)):
                for j in appeared:
                    remove(grid[blank_row[i]][blank_col[i]], j)
            row_count += 1
            appeared = []
            blank_row = []
            blank_col = []
        column_count += 1
        row_count = 0
    result = simplify(grid, row, col)
    return result
    

def check_fin(grid, row, col):
    '''
    Checks if there are still sets remained in a grid. If no, then the grid is finished.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: True(if the sudoku is fully filled) or False(if there is still blanks to be filled)
    '''
    for i in range(row * col):
        for j in range(col * row):
            if isinstance(grid[i][j], list):
                return False
    return True


def stuck(grid, row, col):
    '''
    Start a set of eliminating based on the value returned from the 'find_least' function.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: result(The updated grid)
    '''
    copylist = copy.deepcopy(grid)
    r, c = find_least(grid, row, col)
    least = copy.deepcopy(grid[r][c])
    for x in least:
        grid = copy.deepcopy(copylist)
        grid[r][c] = x
        result = check_for_m(grid, row, col)
        if result:
            return result
    return False


def check(grid, row, col):
    '''
    Simplified function to call all the checkers.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: grid(The updated grid)
    '''
    while not check_fin(grid, row, col):
        copylist = copy.deepcopy(grid)
        grid = check_box(check_col(check_row(grid, row, col), row, col), row, col)
        if copylist == grid:
            grid = stuck(grid, row, col)
    return grid


def check_for_m(grid, row, col):
    '''
    A complex function to use the checkers, with more if statement to prevent crash.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: result(The updated grid)
    '''
    while grid and not check_fin(grid, row, col):
        copylist = copy.deepcopy(grid)
        if grid:
            grid = check_row(grid, row, col)
        if grid:
            grid = check_col(grid, row, col)
        if grid:
            grid = check_box(grid, row, col)
        if not grid:
            return False
        if copylist == grid:
            grid = stuck(grid, row, col)
    if grid and check_solution(grid, row, col):
        return grid
    return False


def improved_solve(grid, row, col):
    '''
    The function used for solving the soduku.
    args: grid - representation of a suduko board as a nested list.
		  row - number of rows in a square.
		  col - number of columns in a square.
    returns: the solved sudoku.
    '''
    generate_range(grid, row, col)
    return check(grid, row, col)

