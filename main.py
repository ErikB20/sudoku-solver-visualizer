import pygame
import sys
import random
from puzzles import puzzleList

pygame.init()

# Global variables
global BASICFONTSIZE, BASICFONT
BASICFONTSIZE = 45
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (9, 148, 65)
RED = (255, 0, 0)
WN_HEIGHT = 800
WN_WIDTH = 720

# Window & Caption creation
WN = pygame.display.set_mode((WN_WIDTH, WN_HEIGHT))
caption = pygame.display.set_caption('Sudoku Solver')
clock = pygame.time.Clock()


class Grid:
    def __init__(self, matrix, length):
        self.matrix = matrix
        self.length = length
        self.squareSize = self.length / 9

    # draws the sudoku grid, using pygame.draw.line()
    def updateGrid(self, solved=False):
        if solved:
            color = DARK_GREEN
        else:
            color = BLACK
        for dir in range(2):
            for line in range(0, 10):
                if line == 0 or line == 3 or line == 6 or line == 9:
                    width = 7
                else:
                    width = 3
                if dir == 0:
                    pygame.draw.line(WN, color, (line * self.squareSize, 0), (line * self.squareSize, self.length), width)
                elif dir == 1:
                    pygame.draw.line( WN, color, (0, line * self.squareSize), (self.length, line * self.squareSize), width )
        self.fillNums()
        pygame.display.update()

    # method to populate the grid with numbers from a matrix
    def fillNums(self):
        for row in range(9):
            for col in range(9):
                if self.matrix[row][col] != 0:
                    squareNum = BASICFONT.render(str(self.matrix[row][col]), False, BLACK)
                    WN.blit(squareNum, (25 + col * self.squareSize, 20 + row * self.squareSize))

# takes in a string puzzle and returns a matrix form
def formMatrix(stringPuzzle):
    grid = []
    row = []
    for index in range(len(stringPuzzle)):
        if index != 0 and index % 9 == 0:
            grid.append(row)
            row = []
        row.append(int(stringPuzzle[index]))
    grid.append(row)
    return grid

# Method to check if a possible position in square is valid
def isValid(potential, matrix, row, col):
    for num in range(9):
        # check row
        if matrix[row][num] == potential:
            return False
        # check column
        if matrix[num][col] == potential:
            return False
    # check box
    row_init = (row // 3)*3
    col_init = (col // 3)*3
    for i in range(3):
        for j in range(3):
            if matrix[row_init+i][col_init+j] == potential:
                return False
    # if it passes all the checks, return true
    return True

# Method to solve a sudoku puzzle using backtracking algorithm
def visualize(grid, coloring=True):
    for row in range(9):
        for col in range(9):
            if grid.matrix[row][col] == 0:
                for pot in range(1, 10):
                    # unnecessary for algorithm, but displays on screen the algorithm
                    # looping through each num, at a reasonable speed
                    if coloring:
                        grid.matrix[row][col] = pot
                        clock.tick(30)
                        WN.fill( WHITE )
                        grid.updateGrid()
                        drawBorder(RED, row, col)
                        grid.matrix[row][col] = 0

                    if isValid(pot, grid.matrix, row, col):
                        if coloring:
                            drawBorder(GREEN, row, col)
                        # if the potential num is valid, change it in the grid
                        grid.matrix[row][col] = pot
                        visualize(grid, coloring)
                        grid.matrix[row][col] = 0 # backtracking step
                return
    grid.updateGrid(True)
    finished()

def finished():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        solved = BASICFONT.render('Solved!', False, BLACK)
        # rec(surface, color, ( x, y, width, height))
        pygame.draw.rect(WN, GREEN, (WN_WIDTH/2 - 160, WN_HEIGHT - 70, 320, 65))
        pygame.draw.rect(WN, BLACK, (WN_WIDTH/2 - 160, WN_HEIGHT - 70, 320, 65), 4)
        WN.blit(solved, (WN_WIDTH//2 - 80, WN_HEIGHT - 55))
        pygame.display.update()

# Draws a border around each square
def drawBorder(color, row, col):
    pygame.draw.rect(WN, color, (col * 80, row * 80, 80, 80), 3)
    pygame.display.update()

def game(sudokuPuzzle):
    gameGrid = Grid(sudokuPuzzle, WN_WIDTH)
    WN.fill( WHITE )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    visualize(gameGrid)
                elif event.key == pygame.K_RETURN:
                    visualize(gameGrid, False)
        gameGrid.updateGrid()
        pygame.display.update()

puz = puzzleList[random.randint(0,len(puzzleList)-1)]
puz = formMatrix(puz)
game(puz)