# ChainReaction
Battle Of Bots #7 - Hackerearth

Chain Reaction is a two playerboard game played on an 8X8 grid of cells. We will play it as two player game on a 5X5 grid of cells. Each player has an allocated color, Red ( First Player ) or Blue ( Second Player ). The objective of the game is to take control of the board by eliminating your opponents' orbs.

**Rules:**

Players take it in turns to place their orbs in a cell. Once a cell has reached critical mass the orbs explode into the surrounding cells adding an extra orb and claiming the cell for the player. Chain reactions cannot occur diagonally. The first figure below shows the critical mass of some cells, but the same logic can be applied to all cells. The explosions might result in overloading of an adjacent cell and the chain reaction of explosion continues until every cell is stable. When a red cell explodes and there are blue cells around, the blue cells are converted to red and the other rules of explosions still follow. The same rule is applicable for other colors. A player may only place their orbs in a blank cell or a cell that contains orbs of their own color. As soon as a player looses all their orbs they are out of the game.

This is a visual representation of the board.

![alt text](https://i.imgur.com/IlvAcDt.jpg)

Note that the critical mass of the top-left most cell is 2 because there are only two adjacent cells that go either vertically or horizontally. Once there are two pieces on the top-left most cell then a chain reaction can occur.

**Running the Bot**

To run the bot, run bot.py and input a 5*5 grid filled with 0's, 1's, and 2's. followed by a number either 1 or 2 to indicate which players turn it is. For examples on how a standard input looks like open files startingBoard.txt, earlyBoard.txt or finalBoard.txt. Input can be piped in or entered manually. Empty cells are denoted by 00. The cell marked 0 means it doesn't contain any orbs. The cell marked 1 means it contains first player's orbs which is Red in color. The cell marked 2 means it contains second player's orbs which is Blue in color.


**Results**

My Bot placed 35th out of 1899 in the competition.
