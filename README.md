# Battleship_Solitaire
In this project, I have developed a program to solve Battleship Solitaire puzzles. I have encoded these puzzles as a constraint satisfaction problem (CSP) and implemented a CSP solver.

**What is Battleship Solitaire**
Unlike the 2-player board game, Battleship Solitaire shows the number of ship parts in each row and column, 
and the goal is to deduce the location of each ship.

**Rules of Battleship Solitaire**
1. There are four types of ships.
      Submarines (1x1)
      Destroyers (1x2)
      Cruisers (1x3)
      Battleships (1x4)
2. Each ship can be either horizontal or vertical, but not diagonal.
3. (Ship constraints) The puzzle describes the number of each type of ship.
4. (Row constraints) The number to the left of each row describes the number of ship parts in that
row.
5. (Column constraints) The number at the top of each column describes the number of ship parts in
that column.
6. Ships cannot touch each other, not even diagonally. In other words, each ship must be
surrounded by at least one square of water on all sides and corners.

**Overview of Solution**
I have implemented a program to solve Battleship Solitaire using backtracking search and forward
checking.

To make my solution more efficient, I implemented heuristics for choosing a variable and value (e.g. Minimum-Remaining-Value 
heuristic, Degree heuristic, and Least-Constraining-Value heuristic).

**Input File Format**
- The first line describes the row constraints as a string of N numbers.
- The row constraints are usually written to the left or the right of each row when viewing
examples of these puzzles.
- The second line describes the column constraints as a string of N numbers.
- The column constraints are usually written on the top or bottom of each column when viewing
examples of these puzzles.
- The third line describes the number of each type of ship.
- The four numbers represent the number of submarines (1x1), destroyers (1x2), cruisers (1x3)
and battleships (1x4) in that order.
- The remaining lines will be an NxN grid representing the initial layout of the puzzle. There are
eight possible characters for each cell.
    ‘ 0 ’ (zero) represents no hint for that square.
    ‘ S ’ represents a submarine,
    ‘ . ’ (period) represents water.
    ‘ < ’ represents the left end of a horizontal ship,
    ‘ > ’ represents the right end of a horizontal ship,
    ‘ ^ ’ represents the top end of a vertical ship,
    ‘ v ’ (lower-cased letter v) represents the bottom end of a vertical ship.
    ‘ M ’ represents a middle segment of a ship (horizontal or vertical).

  eg.
  211222
  140212
  3210
  000000
  0000S0
  000000
  000000
  00000.
  000000

**Output File Format**
The output contains an NxN grid representing the solution to the puzzle.
