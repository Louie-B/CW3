How to use the flags:

Note: These flags all take into consideration that the files being inputted containing the grids are in the same directory as the program itself and should either be a .txt file or normal textfile. 

 1. for getting an explaination of how a grid is solved, input: '-explain "input filename"' (where filename is specified to its filetype as well if necessary)

 2. for reading the grid from a file and saving the solution as an output, input: '-file "input filename" "desired output file name"' (where the desired output filename DOES NOT require specifying a file type). This will output only the solution. If the output should also contain the explanation of how the grid is solved, add the -explain flag. For eg, using an input file called "easy1.txt" and wanting to output the file with the name "easy1solved", input: -file easy1.txt easy1solved -explain

 3. for n number of hints being provided for a specific grid, input: '-hint "input filename" "number of hints wanted"
    Once again, if an explaination is wanted for which hints are given and their positions, add the -explain flag. For eg:  -hint easy1.txt 5 -explain

 4. for getting a profile to measure the performance of different solvers across different grid types within the program, input -profile

 5. for simply solving a grid using a recursive algorithm, input: -recursive "input filename"

 6. for simply solving a grid using wavefront propogation algorithms, input: -wavefront "input filename"

Task 2.4: Ensure the only files in the directory are the CW3.py file and the grid files. Files containing the grid must be a text file as mentioned above. 

Note- Random is not plotted as it takes on average around a minute to carry out the function and sometimes does not provide a solution. This could lead to calculation times of up to an hour to calculate all six grids 10 times. Thus, the code for random has been commented out.