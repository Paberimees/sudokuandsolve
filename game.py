import sys
import pygame
from pygame.locals import *

#important pregame variables
sudokuSquareSize = 48
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
RED = (255, 0, 0)
pygame.font.init()
font = pygame.font.SysFont("arialblack", round(sudokuSquareSize/1.25))
font_sidenumber = pygame.font.SysFont("arialblack", round(sudokuSquareSize/1.75))
#font = pygame.font.SysFont("Arial", sudokuSquareSize) FONT = ARIAL
#font_sidenumber = pygame.font.SysFont("Arial", round(sudokuSquareSize/1.5)) FONT = ARIAL

#setting up pygame and the window
pygame.init()
gamefps = 60
gameClock = pygame.time.Clock()
displayWidth, displayHeight = sudokuSquareSize*11,sudokuSquareSize*11
gameScreen = pygame.display.set_mode((displayWidth, displayHeight))

#Functions
def checkIfOutOfBounds(indexes, speed_row, speed_col):
    newIndexes = (indexes[0]+speed_row, indexes[1]+speed_col)
    if newIndexes[0] > 8 or newIndexes[0] < 0 or newIndexes[1] > 8 or newIndexes[1] < 0:
        return True #yes, it's out of bounds.
    return False #no it's not going out of bounds.

def getNewSelectedSquare(currentSquare, speed_row, speed_col):
    oldIndexes = currentSquare.getIndexes()
    newIndexes = (oldIndexes[0]+speed_row,oldIndexes[1]+speed_col)
    currentSquare.setSelected(False)
    newSquare = gameSquares[newIndexes[0]][newIndexes[1]]
    newSquare.setSelected(True)
    return newSquare




"""

    http://byteauthor.com/2010/08/sudoku-solver/

    1.No other value is allowed according to the allowed values matrix.
    2.A certain value is allowed in no other square in the same section.
    3.A certain value is allowed in no other square in the same row or column.
    4.A certain value is allowed only on one column or row inside a section, thus we can eliminate this value from that row or column in the other sections.

"""

def translateBoard(gameBoard):
    newBoard = []
    for row in gameBoard:
        newRow = []
        for square in row:
            newRow.append(square.getNumber())
        newBoard.append(newRow)
    return newBoard

def checkMatrixForDuplicates(gameBoard, idx_row, idx_col):
    matrix_start_row = idx_row - idx_row%3
    matrix_start_col = idx_col - idx_col%3
    for r in range(matrix_start_row, matrix_start_row+3):
        for c in range(matrix_start_col, matrix_start_col+3):
            if gameBoard[r][c] == gameBoard[idx_row][idx_col] and not (r == idx_row and c == idx_col):
                return True #found duplicate
    return False #no duplicate found

def checkRowAndColForDuplicates():
    pass

gameBoard = [
    [0, 0, 0, 0, 0, 0, 0, 6, 0],
    [7, 2, 0, 0, 4, 0, 9, 0, 3],
    [0, 1, 0, 3, 0, 0, 4, 0, 5],
    [2, 3, 0, 0, 6, 0, 0, 0, 8],
    [8, 0, 1, 4, 0, 5, 6, 0, 2],
    [9, 0, 0, 0, 7, 0, 0, 3, 4],
    [1, 0, 9, 0, 0, 3, 0, 7, 0],
    [5, 0, 7, 0, 2, 0, 0, 8, 1],
    [0, 8, 0, 0, 0, 0, 0, 0, 0]
]




""" OLD, WORKS ONLY FOR SQUARE OBJECTS.
def checkMatrixForDuplicates(idx_row, idx_col):
    matrix_x = idx_col - idx_col%3
    matrix_y = idx_row - idx_row%3
    for r in range(matrix_y, matrix_y+3):
        for c in range(matrix_x, matrix_x+3):
            if gameSquares[r][c].getNumber() == gameSquares[idx_row][idx_col].getNumber() and not (r == idx_row and c == idx_col):
                return True #duplicate found!
    return False #no duplicate found
"""

#Objects
class sudokuSquare():
    def __init__(self, x, y, number=0, preset=False):
        self.x = x
        self.y = y
        self.number = number
        self.preset = preset
        #other variables
        self.sideNumber = 0
        self.selected = False
    def setNumber(self, number):
        if not self.preset:
            self.number = number
    def getNumber(self):
        return self.number
    def setSideNumber(self, number):
        if not self.preset:
            self.sideNumber = number
    def getSideNumber(self):
        return self.sideNumber
    def setSelected(self, bool):
        self.selected = bool
    def getIndexes(self):
        idx_col = int((self.x-sudokuSquareSize)/sudokuSquareSize)
        idx_row = int((self.y-sudokuSquareSize)/sudokuSquareSize)
        return (idx_row, idx_col)
    def drawSelf(self):
        if not self.selected:
            pygame.draw.rect(gameScreen, BLACK, (self.x,self.y,sudokuSquareSize,sudokuSquareSize), 1)
        else:
            pygame.draw.rect(gameScreen, RED, (self.x, self.y, sudokuSquareSize, sudokuSquareSize), 3)
        if self.number != 0:
            if self.preset:
                text = font.render(str(self.number), True, BLACK)
            else:
                text = font.render(str(self.number), True, GRAY)
            #gameScreen.blit(text, (self.x+sudokuSquareSize/2, self.y)) FONT = ARIAL
            gameScreen.blit(text, (self.x+sudokuSquareSize/2.25, self.y+sudokuSquareSize/15))
        if self.sideNumber != 0:
            text = font_sidenumber.render(str(self.sideNumber), True, GRAY)
            #gameScreen.blit(text, (self.x+sudokuSquareSize/8, self.y)) FONT = ARIAL
            gameScreen.blit(text, (self.x+sudokuSquareSize/10, self.y-sudokuSquareSize/8))
    def setPreset(self): #todo remove this, this is for testing purposes only.
        self.preset = True

#Some variables for game
gameSquares = []
selectedSquare = None

#Creating the game field.
for i in range(0, 9):
    arr = []
    for j in range(0, 9):
        preset = False #todo removeme
        if gameBoard[i][j] != 0: #todo removeme
            preset = True #todo removeme
        arr.append(sudokuSquare(sudokuSquareSize+j*sudokuSquareSize, sudokuSquareSize+i*sudokuSquareSize, gameBoard[i][j], preset))
    gameSquares.append(arr)

#Testing purposes. #todo deleteme
gameSquares[0][2].setNumber(3)
gameSquares[0][2].setPreset()
gameSquares[1][5].setNumber(7)
gameSquares[1][5].setPreset()

# Game loop.
while True:
    #Event handling.
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            idx_col = int(((mousePos[0]-mousePos[0]%sudokuSquareSize)-sudokuSquareSize)/sudokuSquareSize)
            idx_row = int(((mousePos[1]-mousePos[1]%sudokuSquareSize)-sudokuSquareSize)/sudokuSquareSize)
            if selectedSquare != None:
                selectedSquare.setSelected(False)
            if idx_row >= 0 and idx_row < 9 and idx_col >= 0 and idx_col < 9:
                selectedSquare = gameSquares[idx_row][idx_col]
                selectedSquare.setSelected(True)
        elif event.type == pygame.KEYDOWN and selectedSquare != None:
            if event.unicode in ["0","1","2","3","4","5","6","7","8","9"]:
                selectedSquare.setSideNumber(int(event.unicode))
            elif event.key == pygame.K_RETURN:
                selectedSquareSideNumber = selectedSquare.getSideNumber()
                if selectedSquareSideNumber != 0:
                    selectedSquare.setNumber(selectedSquareSideNumber)
                    selectedSquare.setSideNumber(0)
            elif event.key == pygame.K_BACKSPACE:
                if selectedSquare.getSideNumber() != 0:
                    selectedSquare.setSideNumber(0)
                else:
                    selectedSquare.setSideNumber(selectedSquare.getNumber())
                    selectedSquare.setNumber(0)
            #CONTROLS FOR MOVING, todo maybe optimize this?
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if not checkIfOutOfBounds(selectedSquare.getIndexes(), -1, 0):
                    selectedSquare = getNewSelectedSquare(selectedSquare,-1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if not checkIfOutOfBounds(selectedSquare.getIndexes(), 1, 0):
                    selectedSquare = getNewSelectedSquare(selectedSquare,1, 0)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if not checkIfOutOfBounds(selectedSquare.getIndexes(), 0, -1):
                    selectedSquare = getNewSelectedSquare(selectedSquare,0, -1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if not checkIfOutOfBounds(selectedSquare.getIndexes(), 0, 1):
                    selectedSquare = getNewSelectedSquare(selectedSquare,0, 1)







    #Drawing.
    #Draws the background.
    gameScreen.fill(WHITE)
    #Draws the bigger lines.
    pygame.draw.line(gameScreen,BLACK,(4*sudokuSquareSize, sudokuSquareSize), (4*sudokuSquareSize, 10*sudokuSquareSize), 4)
    pygame.draw.line(gameScreen, BLACK, (7 * sudokuSquareSize, sudokuSquareSize),(7 * sudokuSquareSize, 10 * sudokuSquareSize), 4)
    pygame.draw.line(gameScreen, BLACK, (sudokuSquareSize,4 * sudokuSquareSize),(10 * sudokuSquareSize, 4 * sudokuSquareSize), 4)
    pygame.draw.line(gameScreen, BLACK, (sudokuSquareSize, 7 * sudokuSquareSize),(10 * sudokuSquareSize, 7 * sudokuSquareSize), 4)
    #Draws all the objects.
    for row in gameSquares:
        for item in row:
            item.drawSelf()
    #Draws to the screen and makes the game tick.
    pygame.display.flip()
    gameClock.tick(gamefps)


