import time
import copy
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

grid1 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 3, 4],
    [3, 4, 2, 1]]

grid2 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 0, 4],
    [3, 4, 2, 1]]

grid3 = [
    [1, 0, 4, 2],
    [4, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid4 = [
    [1, 0, 4, 2],
    [0, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid5 = [
    [1, 0, 0, 2],
    [0, 0, 1, 0],
    [0, 1, 0, 4],
    [0, 0, 0, 1]]

grid6 = [
    [0, 0, 6, 0, 0, 3],
    [5, 0, 0, 0, 0, 0],
    [0, 1, 3, 4, 0, 0],
    [0, 0, 0, 0, 0, 6],
    [0, 0, 1, 0, 0, 0],
    [0, 5, 0, 0, 6, 4]]


grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2), (grid6,2,3)]


# start of functions of wavefront solving
def generate_range(grid, row, col):
    """
    This function replaces all the zeros in a grid into a list containing numbers from 1 to the maximum number in a grid.
    args: grid - representation of a suduko board as a nested list.
          row - number of rows in a square.
          col - number of columns in a square.
    returns: grid(The updated grid)
    """
    max = row * col
    for i in range(row * col):
        for j in range(col * row):
            if not grid[i][j]:
                grid[i][j] = [(i + 1) for i in range(max)]
    return grid


def remove(item, num):
    """
    This function will remove a number from a set. If the number is not in the set, it will pass.
    args: item - the set.
          num - the number that will be removed from item.
    returns: item(the updated item)
    """
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
    least_length = row * col
    row_num = 0
    col_num = 0
    while row_count < row * col:
        while col_count < col * row:
            if isinstance(grid[row_count][col_count], list) and len(grid[row_count][col_count]) < least_length:
                row_num = row_count
                col_num = col_count
                least_length = len(grid[row_count][col_count])
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


def wavefront_solve(grid, row, col):
    '''
    The function used for solving the sudoku.
    args: grid - representation of a suduko board as a nested list.
          row - number of rows in a square.
          col - number of columns in a square.
    returns: the solved sudoku.
    '''
    generate_range(grid, row, col)
    return check(grid, row, col)


# end of functions of wavefront solving


def check_section(section, n):
    '''
    This checks if the section is correct.
    args: section - The row or column that is being checked
    n - size of the sudoku
    '''
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True
    return False


def get_squares(grid, n_rows, n_cols):
    '''
    This function creates a list of all the squares in the sudoku.
    '''
    squares = []
    for i in range(n_cols):
        rows = (i * n_rows, (i + 1) * n_rows)
        for j in range(n_rows):
            cols = (j * n_cols, (j + 1) * n_cols)
            square = []
            for k in range(rows[0], rows[1]):
                line = grid[k][cols[0]:cols[1]]
                square += line
            squares.append(square)

    return (squares)


# To complete the first assignment, please write the code for the following function
def check_solution(grid, n_rows, n_cols):
    '''
    This function is used to check whether a sudoku board has been correctly solved

    args: grid - representation of a suduko board as a nested list.
    returns: True (correct solution) or False (incorrect solution)
    '''
    n = n_rows * n_cols

    for row in grid:
        if check_section(row, n) == False:
            return False

    for i in range(n_rows ** 2):
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

    # N is the maximum integer considered in this board
    n = n_rows * n_cols
    # Find an empty place in the grid
    empty = find_empty(grid)

    # If there's no empty places left, check if we've found a solution
    if not empty:
        # If the solution is correct, return it.
        if check_solution(grid, n_rows, n_cols):
            return grid
        else:
            # If the solution is incorrect, return None
            return None
    else:
        row, col = empty
    #this creates a list of the columns in the sudoku
    list_column = []
    list_column_grid = []
    for rows in range(n):
        for coll in range(n):
            list_column.append(grid[coll][rows])
        list_column_grid.append(list_column)
        list_column = []
    # To find out what square the number is in
    x = col // n_cols
    y = row // n_rows
    num_of_square = x + (n_rows * y)
    # Loop through possible values
    for i in range(1, n + 1):
        if grid[row].count(i) == 0 and list_column_grid[col].count(i) == 0 and get_squares(grid, n_rows, n_cols)[num_of_square].count(i) == 0: #Makes sure only the correct number
            # Place the value into the grid
            grid[row][col] = i
            # Recursively solve the grid
            ans = recursive_solve(grid, n_rows, n_cols)

            # If we've found a solution, return it
            if ans:
                return ans

            # If we couldn't find a solution, that must mean this value is incorrect.
            # Reset the grid for the next iteration of the loop
            grid[row][col] = 0

        # If we get here, we've tried all possible values. Return none to indicate the previous value is incorrect.
    return None


def fill_board_randomly(grid, n_rows, n_cols):
    """
    This function will fill an unsolved Sudoku grid with random numbers

    args: grid, n_rows, n_cols
    return: A grid with all empty values filled in
    """
    n = n_rows * n_cols
    # Make a copy of the original grid
    filled_grid = copy.deepcopy(grid)

    # Loop through the rows
    for i in range(len(grid)):
        # Loop through the columns
        for j in range(len(grid[0])):
            # If we find a zero, fill it in with a random integer
            if grid[i][j] == 0:
                filled_grid[i][j] = random.randint(1, n)

    return filled_grid


def random_solve(grid, n_rows, n_cols, max_tries=500000):
    """
    This function uses random trial and error to solve a Sudoku grid

    args: grid, n_rows, n_cols, max_tries
    return: A solved grid (as a nested list), or the original grid if no solution is found
    """

    for i in range(max_tries):
        possible_solution = fill_board_randomly(grid, n_rows, n_cols)
        if check_solution(possible_solution, n_rows, n_cols):
            return possible_solution

    return grid


def difficulty_level(grid):
    """
    A function that calls upon the grid_difficulty function, and returns the difficulty level of the grid being considered.
    args: grid
    return: 'E','M','H'
    """
    fraction = grid_difficulty(grid)
    if fraction < 0.33:
        return 'E'
    if fraction < 0.66:
        return 'M'
    else:
        return 'H'



def hint(grid, row, col, hint_num):
    '''
    This function will fill answers into the grid, which the number is due to hint_num.
    args: grid - representation of a suduko board as a nested list.
          row - number of rows in a square.
          col - number of columns in a square.
          hint_num - the number of hints to be filled.
    returns: grid(the new grid with filled hints)
    '''
    copy_grid = copy.deepcopy(grid)
    answer_grid = wavefront_solve(copy_grid, row, col)
    empty_row = []
    empty_col = []
    for i in range(row * col):
        for j in range(col * row):
            if grid[i][j] == 0:
                empty_row.append(i)
                empty_col.append(j)
    for i in range(int(hint_num)):
        list_index = random.randint(0, len(empty_row) - 1)
        answer_row = empty_row.pop(list_index)
        answer_col = empty_col.pop(list_index)
        grid[answer_row][answer_col] = answer_grid[answer_row][answer_col]
    return grid

def explain_func(grid, n_rows, n_cols, user_print=False, hints = 0):
    '''
    This function outputs a list of instructions to solve the sudoku.
    args: grid - The grid you want checked
    n_rows - number of rows.
    n_cols - number of collumns.
    user_print - Only True if only the explain flag is being ran.
    '''
    n = n_rows * n_cols
    x_cords = [] #list of X cords
    y_cords = [] #list of y cords
    #This searches through every position and appends the location if its a zero
    for rows in range(n): 
        for coll in range(n):
            if grid[rows][coll] == 0:
                x_cords.append(rows)
                y_cords.append(coll)
    if (hints == 0): # Runs if the hint flag hasnt been ran
        solved = recursive_solve(grid, n_rows, n_cols)

    else:
        solved = hint(grid, n_rows, n_cols, hints) #Sets the grid to the new amount of hints
    if (user_print == True): # If explain flag is ran on its own 
        for i in range(len(x_cords)):
            if (solved[(x_cords[i])][(y_cords[i])] != 0): 
                print("Put a " + str(solved[(x_cords[i])][(y_cords[i])]) + " in position (" + str(x_cords[i]) + ", " + str(y_cords[i]) + ")") #prints position of new additions
        print(solved) 
    else:
        explain_array = [] # A list of all the inputed numbers
        for i in range(len(x_cords)):
            explain_array.append(("Put a " + str(solved[(x_cords[i])][(y_cords[i])]) + " in position (" + str(
                x_cords[i]) + ", " + str(y_cords[i]) + ")"))
        return explain_array

def read_file(input_file):
    """
    A function that reads the file in the directory and returns the grid inside it.
    args: input_file (file name)
    return: type of grid_input
    """
    grid_input = []
    with open(input_file, "r") as my_file:
        # removes the spacing and punctuation in the grids.
        data = my_file.read().replace(",", "")
        data = data.replace(" ", "")
        data = data.replace("\n", "")
        no_of_characters = len(data)
        grid_size = no_of_characters ** 0.5
        temp_array = [] # data of numbers read from the file is stored in an array
        COUNT = 0
        for number in data:
            COUNT += 1
            if COUNT == grid_size:
                COUNT = 0
                temp_array.append(int(number))
                grid_input.append(temp_array)
                temp_array = []
            else:
                temp_array.append(int(number))
    return grid_input, grid_size


def file(file_input, output, explain=False):
    """
    A function that solves the grid from the file read using the read_file function, and outputs a file with the solved grid.
    args: grid
    return: type of grid, n_rows, n_cols
    """
    grid_input, grid_size = read_file(file_input)
    explanation = explain_func(grid_input, grid_type(grid_input)[1], grid_type(grid_input)[2]) # Calls upon the explain function and saves it within an array
    grid_solved = wavefront_solve(grid_input, grid_type(grid_input)[1], grid_type(grid_input)[2])
    file_output = str(output) + "output"
    # Writes in the fie
    with open(file_output, "w") as write_file:
        if explain:
            for line in explanation:
                write_file.write(str(line))
                write_file.write('\n')
            write_file.write('\n')
        for line in grid_solved:
            write_file.write(str(line))
            write_file.write('\n')


def grid_type(grid):
    """
    A function that returns useful information such as the type of grid as well as the number of rows and columns of the grid.
    args: grid
    return: type of grid, n_rows, n_cols
    """
    grid_size = len(grid)
    if grid_size == 6:
        n_rows = 2
        n_cols = 3
        return "3x2", n_rows, n_cols
    elif grid_size == 9:
        n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        return "3x3", n_rows, n_cols
    elif grid_size == 4:
        n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        return "2x2", n_rows, n_cols


def grid_difficulty(grid):
    """
    A function that divides the number of unfilled locations by the total number of locations, to calculate the fraction of the grid that is empty, this information can then be used to decide the difficulty level.
    args: grid
    return: fraction
    """
    unfilled_locations = sum(1 for row in grid for location in row if location == 0)
    total_locations = len(grid) ** 2
    fraction = (unfilled_locations / total_locations)
    return fraction


# Reads the files in the directory and filters it to find the files with the grids that need to be read and used in the profile function.
file_list = os.listdir(".")
filtered_list = [name for name in file_list if
                 'output' not in name and '.git' not in name and '.png' not in name and '.py' not in name and 'solved' not in name and 'README' not in name]


def average_time(grid):
    """
    This function is used to calculate the average time it takes to solve a grid using the different types of solvers.
    args: grid
    return: average_time_recursive, average_time_random, average_time_wave
    """
    total_time = 0
    # total_time_random = 0
    total_time_wavefront = 0
    grid_info = grid_type(grid)
    NUM_OF_TRIALS = 10 # decrease the number of trials to decrease time taken to perform function, however doing this will affect accuracy of results.
    grid_ran = copy.deepcopy(grid)
    print("⌛Calculating...")
    # Loops through and calculates time taken to solve the grids using the different solvers.
    for i in range(NUM_OF_TRIALS):
        grid_rec = copy.deepcopy(grid)
        rec_start_time = time.time()
        recursive_solve(grid_rec, grid_info[1], grid_info[2])
        rec_end_time = time.time()
        rec_exec_time = rec_end_time - rec_start_time
        total_time += rec_exec_time

        grid_wave = copy.deepcopy(grid)
        wave_start_time = time.time()
        wavefront_solve(grid_wave, grid_info[1], grid_info[2])
        wave_end_time = time.time()
        wave_exec_time = wave_end_time - wave_start_time
        total_time_wavefront += wave_exec_time
        """
        The code below was used to find the average time taken to randomly solve the grids, however since it takes too long and sometimes doesnt even solve it, it has been commented out"
    
        grid_ran = copy.deepcopy(grid)
        random_start_time = time.time()
        random_solve(grid_ran, grid_info[1], grid_info[2], max_tries=500000)
        random_end_time = time.time()
        random_exec_time = random_end_time - random_start_time
        total_time_random += random_exec_time
        """
    average_time_recursive = total_time / NUM_OF_TRIALS
    # average_time_random = total_time_random / num_of_trials
    average_time_wave = total_time_wavefront / NUM_OF_TRIALS
    return average_time_recursive, average_time_wave  # average_time_random,


def profile():
    """
    This function is used to plot the time taken to solve different grids using the 3 types of solvers. Presents it in a clear bar-chart with information on the grid type and difficulty.
    """
    aver_recursive_grids = []
    aver_wave_grids = []
    aver_random_grids = []
    difficulty_array = []
    grid_type_array = []
    # loops through and creates an array of the average time taken to solve each grid using the different solvers.
    for i in range(len(filtered_list)):
        aver_recursive_grids.append(average_time(read_file(filtered_list[i])[0])[0])
        # aver_random_grids.append(average_time(read_file(filtered_list[i])[0])[1])
        aver_wave_grids.append(average_time(read_file(filtered_list[i])[0])[1])
        difficulty_array.append(difficulty_level(read_file(filtered_list[i])[0]))
        grid_type_array.append(grid_type(read_file(filtered_list[i])[0])[0])
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.subplots_adjust(left=0.10, bottom=0.15, right=0.95, top=0.90) # ensures that the bar plot fits inside the figure.
    ax.set_yscale('log') # log scale in y-axis
    X = np.arange(len(filtered_list))
    ax.bar(X, aver_recursive_grids, color='b', width=0.35) # bar plot for recursive grid
    # ax.bar(X + 0.25, aver_random_grids, color='r', width=0.25)
    ax.bar(X + 0.35, aver_wave_grids, color='g', width=0.35) # bar plot for wavefront grid
    ax.legend(['Recursive Plus', 'Wavefront', 'Random'])
    concatenated_array_recursive = [i + '\n' + j + str(k) for i, j, k in
                                    zip(filtered_list, difficulty_array, grid_type_array)]
    ax.set_xticks([i + 0.25 for i in range(len(filtered_list))], concatenated_array_recursive)
    ax.set_title("Bar plot comparing the performance of each solver")
    ax.set_xlabel('Grid Files')
    ax.set_ylabel('Time (Seconds)')
    fig.savefig('solver_performance.png')
    plt.show()


def parse_command_line_arguments(argv):
    '''
    Process a list of command line arguments and determine which action to perform
    args: argv, potentially a file name
    returns:    
        explain - "explain filename"
        file - "file inputfile desired_output_file_name" '-explain' if also needed
        hint - "hint file number_of_hints" '-explain' if also needed
        profile - "profile (will read every file on list"
    '''
    do_recursive = False
    do_waveform = False
    show_explain = False
    show_file = False
    show_hint = False
    show_profile = False
    explain = False
    input_filename = ""
    output_filename = ""
    num_hints = 0
    if ('-explain' in argv and '-file' not in argv and '-hint' not in argv):
        if (len(argv) != 2):

            print("\n--------------------------------------")
            print("Error: file name cannot contain spaces and file format must be specified")
            exit()
        else:
            input_filename = argv[1]
            show_explain = True
    elif '-file' in argv:
        if ((len(argv) > 4) or (len(argv) < 3)):
            print("\n--------------------------------------")
            print(
                "Error: file names cannot contain spaces and file format must be specified (except for the output file)")
            exit()
        if '-explain' in argv:
            explain = True
        input_filename = argv[1]
        output_filename = argv[2]
        show_file = True
    elif '-hint' in argv:
        if ((len(argv) > 4) or (len(argv) < 3)):
            print("--------------------------------------")
            print(
                "Error: file names cannot contain spaces and file format must be specified. Ensure spaces are correctly")
            exit()
        if '-explain' in argv:
            explain = True
        input_filename = argv[1]
        num_hints = argv[2]
        show_hint = True
    elif '-recursive' in argv:
        if ((len(argv) > 2) or (len(argv) < 1)):
            print("\n--------------------------------------")
            print("Error: file name cannot contain spaces and file format must be specified")
            exit()
        else:
            input_filename = argv[1]
            do_recursive = True
    elif '-wavefront' in argv:
        if ((len(argv) > 2) or (len(argv) < 1)):

            print("\n--------------------------------------")
            print("Error: file name cannot contain spaces and file format must be specified")
            exit()
        else:
            input_filename = argv[1]
            do_waveform = True
    elif '-profile' in argv:
        show_profile = True
    else:
        print("\n--------------------------------------")
        for (i, (grid, n_rows, n_cols)) in enumerate(grids):
            print ("Solving provided grid number "+str(i+1))
            print (wavefront_solve(grid, n_rows, n_cols))
            print("\n--------------------------------------")
            
    return (show_explain, show_file, show_hint, show_profile, input_filename, output_filename, num_hints, do_recursive,
            do_waveform, explain)

def main(flags):
    show_explain, show_file, show_hint, show_profile, input_file, output_file, num_hints, do_recursive, do_waveform, explain = parse_command_line_arguments(
        flags)

    if show_explain: # runs Explain flag
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        explain_func(grid_input, n_rows, n_cols, True)
    if show_file: #runs file flag
        if explain:
            file(input_file, output_file, True)
        else:
            file(input_file, output_file)
        print("--------------------------------------")
        print("Solution file has been outputted")
    if show_hint: # runs hint flag
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        print("\n--------------------------------------")
        print(str(num_hints) + " hint(s) given. New grid is now:\n")
        if explain:
            print(explain_func(grid_input, n_rows, n_cols, True, num_hints))
        else:
            grid = hint(grid_input, n_rows, n_cols, num_hints)
            print(grid)
    if show_profile: #runs profile flag
        profile()
        print("\n--------------------------------------")
        print("Graph solved as solverperformance.png\n")
    if do_recursive: # runs recursive solver
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        print("\n--------------------------------------")
        print("Grid solved recursively:")
        print("--------------------------------------")
        print(recursive_solve(grid_input, n_rows, n_cols))
    if do_waveform: # runs wavefront solver
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        print("--------------------------------------")
        print("Grid solved using wavefront propogation:")
        print("--------------------------------------")
        print(wavefront_solve(grid_input, n_rows, n_cols))


if __name__ == "__main__":
    print("\n--------------------------------------")
    print("OPEN README.txt FOR HOW TO USE PROGRAM")  
    print("--------------------------------------")
    main(sys.argv[1:])
