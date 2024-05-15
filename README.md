# Kakuro Solver

This is a repository that contains two programs to solve kakuro boards using backtracking algorithms: 
- forward_checking.py uses forward checking
- mac.py uses maintaining arc consistency

The forward-checking algorithm is faster than arc consistency, although they both run in under a second
for a 9x17 board. 

To use the forward checking algorithm to solve a kakuro board, the forward_checking.py file should be located 
at the same level as the Boards folder. The command to run the program should be executed within the main folder
and should look something like:

python3 forward_checking.py Boards/4x4_easy.txt
python3 forward_checking.py Boards/9x11_expert.txt

To use the maintaining arc consistency (MAC) algorithm to solve a kakuro board, the mac.py file should be located 
at the same level as the Boards folder. The command to run the program should be executed within the main folder
and should look something like:

python3 mac.py Boards/6x6_hard.txt
python3 mac.py Boards/9x17_expert.txt

The specific Board text files used for all algorithms can be replaced with other board files in the same location. 
The solution to the boards will print to the console, not to an output file. 

When printing the board to the console, the clue cells on the board will print in a blue color, 
while the cells that were filled in with a number 1-9 will print in a green color. 

### Boards

If one wants to make a new board that is not included in the Boards folder, they have to follow a specific format
for the program to parse them. 

A completely blank cell (not a sum clue or open cell) is represented with '#'. 
A cell that ONLY contains a column clue, x, should be represented with 'x|#', where x is an integer
A cell that ONLY contains a row clue, y, should be represented with '#|y', where y is an integer
A cell that contains BOTH a column and row clue, x and y respectively, should be represented with 'x|y', where x and y
are integers
An empty cell that needs to be filled in with a number 1-9 should be represented with a '0'

Though it does not affect the algorithm, making the board have equal column widths makes it easier to read and understand
what cells correspond to which column clues. To do this, each column should be 6 characters in width. To add extra 
characters, use spaces instead of tabs to get to a width of 6.
