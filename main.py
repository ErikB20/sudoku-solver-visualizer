import pygame
import sys
import random
from puzzles import puzzleList
pygame.init()

# Global variables
global BASICFONTSIZE, BASICFONT
BASICFONTSIZE = 45
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
WN_HEIGHT = 800
WN_WIDTH = 720
# Colors
BLACK = (0, 0, 0)
GREY = (204, 198,194)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (9, 148, 65)
BLUE = (52, 204, 255)
LIGHT_BLUE = (110, 255, 255)
RED = (202, 0, 42)
LIGHT_RED = (255, 88, 79)

# Window, Caption, and Clock creation
WN = pygame.display.set_mode((WN_WIDTH, WN_HEIGHT))
caption = pygame.display.set_caption('Sudoku Solver')
clock = pygame.time.Clock()

# Grid class creates a grid object that uses a matrix to create
# and update a pygame grid
class Grid:
    def __init__(self, matrix, length):
        self.matrix = matrix
        self.length = length
        self.squareSize = self.length / 9

    # draws the sudoku grid, using pygame.draw.line()
    def updateGrid(self, solved=False):
        # if the puzzle has been solved, make the entire grid green
        if solved:
            color = DARK_GREEN
        # else (while still solving), color grid black
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
    # if potential passes all the checks, return true
    return True

# Method to solve a sudoku puzzle using backtracking algorithm
def visualize(grid, updating=True):
    for row in range(9):
        for col in range(9):
            if grid.matrix[row][col] == 0:
                for pot in range(1, 10):
                    # unnecessary for algorithm, but displays on screen the algorithm
                    # looping through each num
                    if updating:
                        grid.matrix[row][col] = pot
                        WN.fill( GREY )
                        grid.updateGrid()
                        drawBorder(RED, row, col)
                        grid.matrix[row][col] = 0

                    if isValid(pot, grid.matrix, row, col):
                        if updating:
                            drawBorder(DARK_GREEN, row, col)
                        # if the potential num is valid, change it in the grid
                        grid.matrix[row][col] = pot
                        visualize(grid, updating)
                        grid.matrix[row][col] = 0 # backtracking step
                return
    grid.updateGrid(True)
    finished()

# Pauses the program to prevent recursion stack from 'unwinding'
# displays solved messages too
def finished():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        solved = BASICFONT.render('Solved!', False, BLACK)
        # rec(surface, color, ( x, y, width, height))
        pygame.draw.rect(WN, DARK_GREEN, (WN_WIDTH/2 - 160, WN_HEIGHT - 70, 320, 65))
        pygame.draw.rect(WN, BLACK, (WN_WIDTH/2 - 160, WN_HEIGHT - 70, 320, 65), 4)
        WN.blit(solved, (WN_WIDTH//2 - 80, WN_HEIGHT - 55))
        pygame.display.update()

# Draws a border around each square
def drawBorder(color, row, col):
    pygame.draw.rect(WN, color, (col * 80, row * 80, 80, 80), 6)
    pygame.display.update()

# Title screen for game
def titleScreen():
    # - Design code -
    WN.fill(GREY)
    pygame.draw.rect(WN, BLACK, (20, 20, 680, 760), 20)
    # draw 'sudoku' title
    title = BASICFONT.render('Sudoku Visualizer', True, WHITE)
    pygame.draw.rect(WN, DARK_GREEN, (125, 125, 470, 100))
    pygame.draw.rect(WN, BLACK, (125, 125, 470, 100), 3)
    WN.blit(title, (150, 150))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # create buttons for easy, medium, and hard
        if button('    Easy', 245, 350, 230, 60, GREEN, DARK_GREEN):
            return puzzleList[0]
        if button(' Medium', 245, 440, 230, 60, LIGHT_BLUE, BLUE):
            return puzzleList[1]
        if button('    Hard', 245, 530, 230, 60, LIGHT_RED, RED):
            return puzzleList[2]
        pygame.display.update()

# Creates a button and returns true or false depending on if the button has
# been clicked or not
def button(msg, x, y, w, h, color_1, color_2):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(WN, color_1, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(WN, color_2, (x, y, w, h))
    pygame.draw.rect(WN, BLACK, (x, y, w, h), 3)
    text = BASICFONT.render(msg, True, BLACK)
    WN.blit(text, (x+10, y+10))
    return False

# Main game loop; creates a grid object from two-dimensional list
# and runs the program
def game():
    sudokuPuzzle = formMatrix(titleScreen())
    gameGrid = Grid(sudokuPuzzle, WN_WIDTH)
    WN.fill( GREY )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()        
            elif event.type == pygame.KEYDOWN:
                # press space to visualize
                if event.key == pygame.K_SPACE:
                    visualize(gameGrid)
                # press return to quickSolve
                elif event.key == pygame.K_RETURN:
                    visualize(gameGrid, False)
        gameGrid.updateGrid()
        pygame.display.update()

game()