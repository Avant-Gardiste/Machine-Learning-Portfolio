# Tic-Tac-Toe

Using Minimax & Alpha-beta pruning *(AI Algorithm)*, we will implement an A.I to play Tic-Tac-Toe (or Noughts and Crosses) game optimally.

![title](img/ttt.png)

## Introduction
To solve games using A.I, we will introduce the concept of a game tree followed by *Minimax with Alpha-beta pruning* algorithm. The different states of the game are represented by nodes in the game tree, very similar to the above planning problems. The idea is just slightly different. In the game tree, the nodes are arranged in levels that correspond to each player's turns in the game so that the “root” node of the tree (usually depicted at the top of the diagram) is the beginning position in the game. In Tic-Tac-Toe, this would be the empty grid with no X's or O's played yet. Under root, on the second level, there are the possible states that can result from the first player’s moves, be it 'X' or 'O'. We call these nodes the “children” of the root node.

Each node on the second level, would further have as its children nodes the states that can be reached from it by the opposing player's moves. This is continued, level by level, until reaching states where the game is over. In Tic-Tac-Toe, this means that either one of the players gets a line of three and wins, or the board is full and the game ends in a tie.

## What is Minimax & Alpha/Beta Pruning ?
Minimax is an artificial intelligence applied in games with two players, such as Tic-Tac-Toe, Checkers, Chess and so on. This games are known as zero-sum games, because in a mathematical representation: one player wins (+1) and other player loses (-1) or both of anyone not to win (0). Alpha-beta pruning is a procedure to reduce the amount of computation and searching during minimax.

## How does it work ?
The algorithm search, recursively, the best move that leads the Max player to win or not lose (draw). It consider the current state of the game and the available moves at that state, then for each valid move it plays (alternating min and max) until it finds a terminal state (win, draw or lose).

## Game Tree 
Below, the best move is on the middle because the max value is on the second node on the left.
![title](img/game_tree.png)

We can see that the depth is equal to the valid moves on the board. 

Simplified game tree:
![title](img/simplified_GT.png)

The tree above has 11 nodes while the whole game tree has 549.946 nodes.

In a more complex game, such as chess, it's hard to search whole game tree. However, Alpha–beta Pruning is an optimization method to the minimax algorithm that allows us to disregard some branches in the search tree, because he cuts irrelevant nodes (subtrees) in search.

## Getting started 
 - Download the distribution code from https://cdn.cs50.net/ai/2020/x/projects/0/tictactoe.zip and unzip it.
 - Once in the directory for the project, run pip3 install -r requirements.txt to install the required Python package (pygame) for this project.
 
## Understanding
There are two main files in this project: ```runner.py``` and ```tictactoe.py```. ```tictactoe.py``` contains all of the logic for playing the game, and for making optimal moves. ```runner.py``` has been implemented for you, and contains all of the code to run the graphical interface for the game. Once you’ve completed all the required functions in ```tictactoe.py```, you should be able to run python ```runner.py``` to play against your AI!

Let’s open up ```tictactoe.py``` to get an understanding for what’s provided. First, we define three variables: ```X```, ```O```, and ```EMPTY```, to represent possible moves of the board.

The function ```initial_state``` returns the starting state of the board. For this problem, we’ve chosen to represent the board as a list of three lists (representing the three rows of the board), where each internal list contains three values that are either ```X```, ```O```, or ```EMPTY```. What follows are functions that we’ve left up to you to implement!

## Specification
Complete the implementations of ```player```, ```actions```, ```result```, ```winner```, ```terminal```, ```utility```, and ```minimax```.

 - The ```player``` function should take a ```board``` state as input, and return which player’s turn it is (either ```X``` or ```O```).
     - In the initial game state, ```X``` gets the first move. Subsequently, the player alternates with each additional move.
     - Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
 - The ```actions``` function should return a ```set``` of all of the possible actions that can be taken on a given board.
     - Each action should be represented as a tuple ```(i, j)``` where ```i``` corresponds to the row of the move (```0```, ```1```, or ```2```) and ```j``` corresponds to which cell in the row corresponds to the move (also ```0```, ```1```, or ```2```).
     - Possible moves are any cells on the board that do not already have an ```X``` or an ```O``` in them.
     - Any return value is acceptable if a terminal board is provided as input.
 - The ```result``` function takes a ```board``` and an ```action``` as input, and should return a new board state, without modifying the original board.
     - If ```action``` is not a valid action for the board, your program should [raise an exception](https://docs.python.org/3/tutorial/errors.html#raising-exceptions).
     - The returned board state should be the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
     - Importantly, the original board should be left unmodified : since Minimax will ultimately require considering many different board states during its computation. This means that simply updating a cell in ```board``` itself is not a correct implementation of the ```result``` function. You’ll likely want to make a [deep copy](https://docs.python.org/3/library/copy.html#copy.deepcopy) of the board first before making any changes.
 - The ```winner``` function should accept a ```board``` as input, and return the winner of the board if there is one.
     - If the X player has won the game, your function should return ```X```. If the O player has won the game, your function should return ```O```.
     - One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
     - You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
     - If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return ```None```.
 - The ```terminal``` function should accept a ```board``` as input, and return a boolean value indicating whether the game is over.
     - If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return ```True```.
     - Otherwise, the function should return ```False``` if the game is still in progress.
 - The ```utility``` function should accept a terminal ```board``` as input and output the utility of the board.
     - If X has won the game, the utility is ```1```. If O has won the game, the utility is ```-1```. If the game has ended in a tie, the utility is ```0```.
     - You may assume ```utility``` will only be called on a ```board``` if ```terminal(board)``` is ```True```.
 - The ```minimax``` function should take a ```board``` as input, and return the optimal move for the player to move on that board.
     - The move returned should be the optimal action ```(i, j)``` that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
     - If the ```board``` is a terminal board, the ```minimax``` function should return ```None```.
     
For all functions that accept a ```board``` as input, you may assume that it is a valid board (namely, that it is a list that contains three rows, each with three values of either ```X```, ```O```, or ```EMPTY```). You should not modify the function declarations (the order or number of arguments to each function) provided.

Once all functions are implemented correctly, you should be able to run ```python runner.py``` and play against your AI. And, since Tic-Tac-Toe is a tie given optimal play by both sides, you should never be able to beat the AI (though if you don’t play optimally as well, it may beat you!)

## Hints
  - If you’d like to test your functions in a different Python file, you can import them with lines like ```from tictactoe import initial_state```.
  - You’re welcome to add additional helper functions to ```tictactoe.py```, provided that their names do not collide with function or variable names already in the module.
  - Alpha-beta pruning is optional, but may make our AI run more efficiently!

## Dependencies
 - Python 3.x
 - Pygame

## Resources :
For more information, see:
 - CS50’s Introduction to Artificial Intelligence with Python : https://cs50.harvard.edu/ai/2020/
 - Algorithms Explained – minimax and alpha-beta pruning : https://www.youtube.com/watch?v=l-hh51ncgDI&t=52s&ab_channel=SebastianLague