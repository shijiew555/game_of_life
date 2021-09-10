# Game of Life

import numpy
import pylab
import random
import copy
from tkinter import*

# init
def init(data):
    data.game = GameOfLife(N = 100, T = 200)
    data.time = 0
    data.started = False

# redrawAll
def redrawAll(canvas, data):
    canvas.create_rectangle(550, 150, 650, 200, fill="yellow", width=0)
    canvas.create_text(600, 175, text="Start", fill="black", font="Times 30 bold")
    canvas.create_rectangle(550, 220, 650, 270, fill="yellow", width=0)
    canvas.create_text(600, 245, text="Restart", fill="black", font="Times 30 bold")
    canvas.create_text(600, 60, text="Click on grids to create cells, then \n click \"Start\". Click \"Restart\" \nto empty all grids and start over.", fill="black", font="Times 11 bold")
    drawBoard(canvas, data)

# timerFired
def timerFired(data):
    if data.started:
        #print("Change")
        data.game.play()

# draw the girds and cells
def drawBoard(c, d):
    if d.started:
        board = d.game.new_grid
    else:
        board = d.game.old_grid

    for i in range(100):
        for j in range(100):
            if board[i][j] == 1:
                c.create_rectangle(j*5, i*5, j*5+5, i*5+5, fill="yellow")
            elif board[i][j] == 0:
                c.create_rectangle(j*5, i*5, j*5+5, i*5+5, fill="darkgrey")

# mousePressed
def mousePressed(event, data):
    x = event.x//5
    y = event.y//5

    if not data.started:
        if x <= 99 and y <= 99:
            data.game.old_grid[y][x] = 1
        elif 550 < event.x < 650 and 150 < event.y < 200:
            data.started = True
    if 550 < event.x < 650 and 220 < event.y < 270:
        data.started = False
        reset(data)

# empty all grids
def reset(data):
    for i in range(100):
        for j in range(100):
            data.game.old_grid[i][j] = 0
            data.game.new_grid[i][j] = 0

# keyPressed
def keyPressed(event, data):
    pass


class GameOfLife:
    def __init__(self, N=100, T=200):
        """ Set up Game of Life. """
        self.N = N
        self.old_grid = numpy.zeros(N*N, dtype='i').reshape(N,N)
        self.new_grid = numpy.zeros(N*N, dtype='i').reshape(N,N)
        self.T = T # The maximum number of generations

    def live_neighbours(self, i, j):
        """ Count the number of live neighbours around point (i, j). """
        s = 0 # The total number of live neighbours.
        # Loop over all the neighbours.
        for x in [i-1, i, i+1]:
            for y in [j-1, j, j+1]:
                if(x == i and y == j):
                    continue
                if(x != self.N and y != self.N):
                    s += self.old_grid[x][y]
            # In this case, we loop back round such that the grid becomes a "toroidal array".
                elif(x == self.N and y != self.N):
                    s += self.old_grid[0][y]
                elif(x != self.N and y == self.N):
                    s += self.old_grid[x][0]
                else:
                    s += self.old_grid[0][0]
        return s

    def play(self):
        # Loop over each cell of the grid and apply Conway's rules.
        for i in range(self.N):
            for j in range(self.N):
                live = self.live_neighbours(i, j)
                if(self.old_grid[i][j] == 1 and live < 2):
                    self.new_grid[i][j] = 0 # Dead from starvation.
                elif(self.old_grid[i][j] == 1 and (live == 2 or live == 3)):
                    self.new_grid[i][j] = 1 # Continue living.
                elif(self.old_grid[i][j] == 1 and live > 3):
                    self.new_grid[i][j] = 0 # Dead from overcrowding.
                elif(self.old_grid[i][j] == 0 and live == 3):
                    self.new_grid[i][j] = 1 # Alive from reproduction.

        # The new configuration becomes the old configuration for the next generation.
        self.old_grid = self.new_grid.copy()

####################################
# use the run function as-is
####################################

def run(width=700, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 200 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))

    timerFiredWrapper(canvas, data)
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris(rows=15, cols=10):
    # use the rows and cols to compute the appropriate window size here!
    run()

# run tetris
playTetris()
