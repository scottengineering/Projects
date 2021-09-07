import pygame, sys
import heapq
import math

pygame.init()

size = 800
window = pygame.display.set_mode((size, size + 50))
pygame.display.set_caption("Tetris")
font = pygame.font.SysFont('Constantia', 30)

green = (51, 255, 51)
yellow = (248, 255, 51)
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 22, 11)
blue = (11, 27, 240)
buttonCol = 189, 181, 177

# Allows for the creation of a button with text and reaction to being pressed
class Button:

    def __init__(self, x, y, wide, high, text):
        self.buttonRect = pygame.Rect((x, y), (wide, high))
        self.font = pygame.font.SysFont("Arial", 30)
        self.text = font.render(text, True, black)
        self.textRect = self.text.get_rect(center = self.buttonRect.center)

    def render(self, window):
        mPos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            if self.buttonRect.collidepoint(mPos):
                pygame.draw.rect(window, red, self.buttonRect)
        else:
            pygame.draw.rect(window, buttonCol, self.buttonRect)

        window.blit(self.text, self.textRect)

    def getButtonRect(self):
        return self.buttonRect

# Class allows creates a node in the board that holds render information as well as position
class Node:

    def __init__(self, pos, color, width):
        self.pos = pos
        self.color = color
        self.width = width
        self.y = pos[0] * width
        self.x = pos[1] * width
        self.barrier = False

    def getColor(self):
        self.color = red
        return self.color

    def setColor(self, newColor):
        self.color = newColor

    def getPosition(self):
        return self.pos

    def isBarrier(self):
        return self.barrier

    def setBarrier(self, bar):
        self.barrier = bar

    def drawRect(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

# Handles rendering board and running pathfinding algorithms
class Visualizer:

    def __init__(self, rows):
        self.rows = rows
        self.nodeWidth = size // rows
        self.board = self.makeBoard()

    def makeBoard(self):
        retBoard = []
        for i in range(self.rows):
            rowList = []
            for j in range(self.rows):
                newNode = Node((i,j), white, self.nodeWidth)
                rowList.append(newNode)

            retBoard.append(rowList)

        return retBoard

    def drawBoard(self, window):
        for i in range(self.rows):
            y = i * self.nodeWidth
            pygame.draw.line(window, black, (0, y), (size, y))

        for j in range(self.rows):
            x = j * self.nodeWidth
            pygame.draw.line(window, black, (x, 0), (x, size))

    def draw(self, window):
        for row in self.board:
            for n in row:
                n.drawRect(window)

        self.drawBoard(window)
        pygame.display.update()

    def resetBoard(self):
        self.board = self.makeBoard()

    def getNode(self, pos):
        return self.board[pos[0]][pos[1]]

    def clickPos(self, pos):
        row = pos[0] // self.nodeWidth
        col = pos[1] // self.nodeWidth

        return (col, row)

def main(window):
    rows = 10
    vis = Visualizer(10)
    run = True
    while run:
        vis.draw(window)
        for event in pygame.event.get():
            # If user presses x in corner of window
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main(window)