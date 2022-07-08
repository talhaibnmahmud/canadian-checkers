# [American Checkers](https://en.wikipedia.org/wiki/English_draughts) Game in Python

Checkers, also known as draughts, is a group of strategy board games for two players which involve diagonal moves of uniform game pieces and mandatory captures by jumping over opponent pieces. Checkers is developed from alquerque. The term "checkers" derives from the checkered board which the game is played on, whereas "draughts" derives from the verb "to draw" or "to move".

The most popular forms of checkers in Anglophone countries are [American checkers](https://en.wikipedia.org/wiki/English_draughts) (also called [English draughts](https://en.wikipedia.org/wiki/English_draughts)), which is played on an 8×8 checkerboard; Russian draughts, Turkish draughts both on an 8x8 board, and International draughts, played on a 10×10 board -the latter is widely played in many countries worldwide. There are many other variants played on 8×8 boards. Canadian checkers and Singaporean/Malaysian checkers (also locally known as dum) are played on a 12×12 board.

American checkers was weakly solved in 2007 by a team of Canadian computer scientists led by Jonathan Schaeffer. From the standard starting position, perfect play by each side would result in a draw.

Visit the [Wikipedia page](https://en.wikipedia.org/wiki/Checkers) for more information.

## Requirements

- Python 3.10+

  The game uses several features introduced in Python 3.10 like [Union Types](https://peps.python.org/pep-0604/) and some others.
  So you need to have Python 3.10 or later installed.

## Installation

- Clone the repository:

```bash
git clone https://github.com/talhaibnmahmud/python-checkerboard.git
```

- Create a virtual environment:

```PowerShell
python -m venv venv
```

- Activate the virtual environment:

```PowerShell
. venv\Scripts\activate
```

- Upgrade pip:

```PowerShell
python -m pip install --upgrade pip
```

- Installing dependencies:

```PowerShell
python -m pip install -r requirements.txt
```

## Running the game

```PowerShell
python main.py
```

## How to play

- Use right mouse button to select a piece to move.

- If the selected piece has any valid moves, it will be highlighted.

- Use left mouse button to move the piece to any of the highlighted squares.

## Game Rules

Checkers is played by two opponents on opposite sides of the game board. One player has the dark pieces (usually black); the other has the light pieces (usually white or red). Players alternate turns. A player can not move an opponent's pieces. A move consists of moving a piece diagonally to an adjacent unoccupied square. If the adjacent square contains an opponent's piece, and the square immediately beyond it is vacant, the piece may be captured (and removed from the game) by jumping over it.

Only the dark squares of the checkerboard are used. A piece can only move diagonally into an unoccupied square. When capturing an opponent's piece is possible, capturing is mandatory in most official rules. If the player does not capture, the other player can remove the opponent's piece as penalty (or muffin). And where there are two or more such positions, the player forfeits pieces that cannot be moved. Although some rule variations make capturing optional. In almost all variants, the player without pieces remaining, or who cannot move due to being blocked, loses the game.

- Man

  An uncrowned piece (man) moves one step diagonally forwards and captures an adjacent opponent's piece by jumping over it and landing on the next square. Multiple enemy pieces can be captured in a single turn provided this is done by successive jumps made by a single piece; the jumps do not need to be in the same line and may "zigzag" (change diagonal direction). In American checkers, men can jump only forwards; in international draughts and Russian draughts, men can jump both forwards and backwards.

- King

  When a man reaches the farthest row forward, known as the kings row or crownhead, it becomes a king. It is marked by placing an additional piece on top of, or crowning, the first man. The king has additional powers, including the ability to move backwards and, in variants where men cannot already do so, capture backwards. Like a man, a king can make successive jumps in a single turn, provided that each jump captures an enemy piece.

  A king's only advantage over a man is the additional ability to move and capture backwards.
