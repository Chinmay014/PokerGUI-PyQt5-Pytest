## About this repository
This repository contains a mini-project submitted as a part of a university course in Python 'Object-oriented programming in Python'. This contains a small GUI made through PyQt5 which simulates a game of Texas hold'em poker between two players. Cards are dealt on the table below the players cards in succession as first two cards, then the flop, the turn and finally the river. Both players start with $250 as the starting bet.
![alt text](image.png)

players can either fold their cards and accept defeat. Or they can call on ongoing bet to stay in the game. if they are feeling lucky however, they can raise the bet by any amount of money through the input box provided to them. 

![alt text](image-1.png)

The player with the greater hand wins and gets the pot money. On restarting, the winning player start with greater money.

## How to run
After cloning it to a local directory, the desktop app can be launched using:
<code>py -3 pokergame.py</code> (for windows)
<code>python3 pokergame.py</code> (for mac/linux)

