import time
import copy
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

grid1 = [
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

grid4 = [
    [0, 3, 0, 4, 0, 0],
    [0, 0, 5, 6, 0, 3],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 3, 0, 5],
    [0, 6, 4, 0, 3, 1],
    [0, 0, 1, 0, 4, 6],
]


#start of functions of wavefront solving
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


def wavefront_solve(grid, row, col):
    '''
    The function used for solving the soduku.
    args: grid - representation of a suduko board as a nested list.
          row - number of rows in a square.
          col - number of columns in a square.
    returns: the solved sudoku.
    '''
    generate_range(grid, row, col)
    return check(grid, row, col)
#end of functions of wavefront solving


def check_section(section, n):
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True
    return False


def get_squares(grid, n_rows, n_cols):
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
        if grid[row].count(i) == 0 and list_column_grid[col].count(i) == 0 and get_squares(grid, n_rows, n_cols)[num_of_square].count(i) == 0:
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
    fraction = grid_difficulty(grid)
    if fraction < 0.33:
        return 'easy'
    if fraction < 0.66:
        return 'medium'
    else:
        return 'hard'

def explain_func(grid, n_rows, n_cols, user_print=False):
    n = n_rows * n_cols
    x_cords = []
    y_cords = []
    for rows in range(n):
        for coll in range(n):
            if grid[rows][coll] == 0:
                x_cords.append(rows)
                y_cords.append(coll)
    solved = recursive_solve(grid, n_rows, n_cols)
    if (user_print == True):
        for i in range(len(x_cords)):
            print("Put a " + str(solved[(x_cords[i])][(y_cords[i])]) + " in posistion (" + str(x_cords[i]) + ", " + str(
                y_cords[i]) + ")")
        print(solved)
    else:
        explain_array = []
        for i in range(len(x_cords)):
            explain_array.append(("Put a " + str(solved[(x_cords[i])][(y_cords[i])]) + " in posistion (" + str(
                x_cords[i]) + ", " + str(y_cords[i]) + ")"))
        return explain_array



def solve(grid, n_rows, n_cols, explain=False):
    '''
    Solve function for Sudoku coursework.
    Comment out one of the lines below to either use the random or recursive solver
    '''
    if explain == True:
        explain_func(grid, n_rows, n_cols, True)
    # return random_solve(grid, n_rows, n_cols)
    else:
        return recursive_solve(grid, n_rows, n_cols)


file_names = ['easy1.txt', 'easy2.txt', 'med1', 'med2', 'hard1']

def read_file(input_file):
    grid_input = []
    with open(input_file, "r") as my_file:
        data = my_file.read().replace(",", "")
        data = data.replace(" ", "")
        data = data.replace("\n", "")
        no_of_characters = len(data)
        grid_size = no_of_characters ** 0.5
        temp_array = []
        count = 0
        for number in data:
            count += 1
            if count == grid_size:
                count = 0
                temp_array.append(int(number))
                grid_input.append(temp_array)
                temp_array = []
            else:
                temp_array.append(int(number))
    return grid_input, grid_size


def file(file_input, output):
    grid_input, grid_size = read_file(file_input)
    if grid_size == 6:
        n_rows = 2
        n_cols = 3
    else:
        n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
    explaination = explain_func(grid_input, n_rows, n_cols)
    grid_solved = solve(grid_input, n_rows, n_cols)
    file_output = str(output) + "solved.txt"
    with open(file_output, "w") as write_file:
        for line in explaination:
            write_file.write(str(line))
            write_file.write('\n')
        write_file.write('\n')
        for line in grid_solved:
            write_file.write(str(line))
            write_file.write('\n')

def grid_type(grid):
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
    unfilled_locations = sum(1 for row in grid for location in row if location == 0)
    total_locations = len(grid) ** 2
    fraction = (unfilled_locations / total_locations)
    print(unfilled_locations, total_locations, fraction)
    return fraction


file_list = os.listdir(".")
filtered_list = [name for name in file_list if
                'solved' not in name and '.git' not in name and '.png' not in name and '.py' not in name]


def hint(grid, row, col, hint_num):
    copy_grid = copy.deepcopy(grid)
    answer_grid = wavefront_solve(copy_grid, row, col)
    empty_row = []
    empty_col = []
    for i in range(row*col):
        for j in range(col*row):
            if grid[i][j] == 0:
                empty_row.append(i)
                empty_col.append(j)
    for i in range(int(hint_num)):
        list_index = random.randint(0, len(empty_row) - 1)
        answer_row = empty_row.pop(empty_row[list_index])
        answer_col = empty_col.pop(empty_col[list_index])
        grid[answer_row][answer_col] = answer_grid[answer_row][answer_col]
    return grid


def average_time(grid):
    total_time = 0
    # total_time_random = 0
    # average_time_random = 0
    average_time_recursive = 0
    grid_info = grid_type(grid)
    num_of_trials = 10
    for i in range(num_of_trials):
        grid_copy = copy.deepcopy(grid)
        start_time = time.time()
        recursive_solve(grid_copy, grid_info[1], grid_info[2])
        end_time = time.time()
        # random_start_time = time.time()
        # random_solve(grid_copy, grid_info[1], grid_info[2], max_tries=500000)
        # random_end_time = time.time()
        execution_time = end_time - start_time
        # random_exec_time = random_end_time - random_start_time
        total_time += execution_time
        # total_time_random += random_exec_time
    average_time_recursive = total_time / num_of_trials
    # average_time_random = total_time_random / num_of_trials
    # print("Average time of execution for a ", grid_info[0], "is", (total_time / 10), "seconds. Grid difficulty is", grid_difficulty(grid))
    return average_time_recursive  # average_time_random


aver_recursive_grids = []
aver_random_grids = []
for i in range(len(filtered_list)):
    aver_recursive_grids.append(average_time(read_file(filtered_list[i])[0]))
    # aver_random_grids.append(average_time(read_file(filtered_list[i])[0]))


def plot():
    # Declaring the figure or the plot (y, x) or (width, height)
    # plt.figure(figsize=[20, 15])
    # Data to be plotted
    totalDeath = [113055, 37312, 5971, 7473, 33964, 20002]
    totalRecovery = [773480, 325602, 230688, 129095, 166584, 20200]
    activeCases = [1139958, 347973, 239999, 129360, 34730, 30000]
    X = np.arange(len(filtered_list))
    plt.bar(X, aver_recursive_grids, color='black', width=0.25)
    # plt.bar(X + 0.25, totalRecovery, color='g', width=0.25)
    # plt.bar(X + 0.5, activeCases, color='b', width=0.25)
    plt.legend(['Recursive', 'Recursive', 'other_solver'])
    plt.xticks([i + 0.25 for i in range(len(filtered_list))], filtered_list)
    plt.title("Bar plot comparing the performance of each solver")
    plt.xlabel('files')
    plt.ylabel('Time')
    plt.savefig('solver_performance.png')
    plt.show()


def profile(grid):
    av_time_recursive = []
    av_time_random = []
    grid_info = grid_type(grid)
    # av_time_recursive.append(average_time(grid)[0])
    # av_time_random.append(average_time(grid)[1])
    print(
        f"Average time of execution to recursively solve this {grid_info[0]} grid of difficulty {difficulty_level(grid)} is {average_time(grid)[0]} secs.")
    print(
        f"Average time of execution to randomly solve this {grid_info[0]} grid of difficulty {difficulty_level(grid)} is {average_time(grid)[1]} secs.")

def parse_command_line_arguments(argv):
    '''
    Process a list of command line arguments and determine which action to perform

    args: argv, potentially a file name
    returns:    
        explain - "explain filename"
        file - "file inputfile desired_output_file_name"
        hint - "hint file number_of_hints"
        profile - "profile (will read every file on list"
    '''
    do_recursive = False
    do_waveform = False
    show_explain = False
    show_file = False
    show_hint = False
    show_profile = False
    input_filename = ""
    output_filename = ""
    num_hints = 0
    if '-explain' in argv:
            if len(argv) > 2:
                print ("\n--------------------------------------")
                print ("Error: file name cannot contain spaces and file format must be specified")
                exit()
            else:
                input_filename = argv[1]
                show_explain = True
    elif '-file' in argv:
        if len(argv) > 3:
            print ("\n--------------------------------------")
            print ("Error: file names cannot contain spaces and file format must be specified (except for the output file)")
            exit()
        else:
            input_filename = argv[1]
            output_filename = argv[2]
            show_file = True
    elif '-hint' in argv:
        if len(argv) > 3:
            print ("--------------------------------------")
            print ("Error: file names cannot contain spaces and file format must be specified")
            exit()
        else:
            input_filename = argv[1]
            num_hints = argv[2]
            show_hint = True
    elif '-recursive' in argv:
        if len(argv) > 2:
            print ("\n--------------------------------------")
            print ("Error: file name cannot contain spaces and file format must be specified")
        else:
            input_filename = argv[1]
            do_recursive = True
    elif '-waveform' in argv:
        if len(argv) > 2:
            print ("\n--------------------------------------")
            print ("Error: file name cannot contain spaces and file format must be specified")
        else:
            input_filename = argv[1]
            do_waveform = True
    else:
        print ("\n--------------------------------------")
        print ("LIST OF HOW TO WORK IT")#this needs to be done after every flag is finished
        print ("--------------------------------------")

    return (show_explain, show_file, show_hint, show_profile, input_filename, output_filename, num_hints, do_recursive, do_waveform)

def main(flags):
    show_explain, show_file, show_hint, show_profile, input_file, output_file, num_hints, do_recursive, do_waveform = parse_command_line_arguments(flags)

    if show_explain:
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        explain_func(grid_input, n_rows, n_cols, True)
    if show_file:
        file(input_file, output_file)
        print ("--------------------------------------")
        print ("Solution file has been outputted")
    if show_hint:
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        grid = hint(grid_input, n_rows, n_cols, num_hints)
        print ("\n--------------------------------------")
        print (str(num_hints) + " hint(s) given. New grid is now:\n")
        print (grid)
    if do_recursive:
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        print ("\n--------------------------------------")
        print ("Grid solved recursively:")
        print ("--------------------------------------")
        print (recursive_solve(grid_input, n_rows, n_cols))
    if do_waveform:
        grid_input, grid_size = read_file(input_file)
        if grid_size == 6:
            n_rows = 2
            n_cols = 3
        else:
            n_rows, n_cols = int(grid_size ** 0.5), int(grid_size ** 0.5)
        print ("--------------------------------------")
        print ("Grid solved using waveform propogation:")
        print ("--------------------------------------")
        print (wavefront_solve(grid_input, n_rows, n_cols))


if __name__ == "__main__":
    main(sys.argv[1:])
