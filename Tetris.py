import random

import pygame, sys
import heapq
import math

pygame.init()

size = 800
blockSize = size // 20
print(blockSize)
halfBlock = blockSize // 2
print(halfBlock)
offsetL = (size - (blockSize * 10)) // 2
offSetR = size - offsetL
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Tetris")
font = pygame.font.SysFont('Constantia', 30)

green = (114, 203, 59)
yellow = (255, 213, 0)
orange = (255, 151, 28)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 50, 19)
blue = (3, 65, 174)
buttonCol = 189, 181, 177

colorList = [blue, green, yellow, orange, red]

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
        self.y = pos[0]
        self.x = pos[1]

    def getColor(self):
        self.color = red
        return self.color

    def setColor(self, newColor):
        self.color = newColor

    def getPosition(self):
        return self.pos

    def drawRect(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

# Makes and renders shape
class TetrisPiece:

    def __init__(self, pieceNum, color):
        self.color = color
        self.y = 0
        self.x = (blockSize * 4) + offsetL
        self.rotateNum = 1
        self.shape = None
        self.posList = []
        if pieceNum == 1:
            self.shape = self.sShape
        elif pieceNum == 2:
            self.shape = self.zShape
        elif pieceNum == 3:
            self.shape = self.iShape
        elif pieceNum == 4:
            self.shape = self.boxShape
        elif pieceNum == 5:
            self.shape = self.jShape
        elif pieceNum == 6:
            self.shape = self.lShape
        elif pieceNum == 7:
            self.shape = self.tShape

    def drawPiece(self, window):
        self.shape(window)

    def moveY(self, increment):
        self.y += increment

    def moveX(self, increment):
        self.x += increment * blockSize

    def getY(self):
        return self.y

    def newRotate(self, num):
        if self.rotateNum + num < 1:
            self.rotateNum = 4
        elif self.rotateNum + num > 4:
            self.rotateNum = 1
        else:
            self.rotateNum += num

    def rotate(self, x, y):
        if self.rotateNum == 1:
            return (self.x + x, self.y + y)
        elif self.rotateNum == 2:
            return (self.x + (y * -1), self.y + x)
        elif self.rotateNum == 3:
            return (self.x + (x * -1), self.y + (y * -1) - blockSize)
        elif self.rotateNum == 4:
            return (self.x + y, self.y + (x * -1))

    def sShape(self, window):
        pos = self.rotate(blockSize, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(-blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

    def zShape(self, window):
        pos = self.rotate(-blockSize, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

    def iShape(self, window):
        pos = self.rotate(-(blockSize * 2), 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(-blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

    def boxShape(self, window):
        pos = self.rotate(-blockSize, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(-blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

    def jShape(self, window):
        pos = self.rotate(-blockSize, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(-blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

    def lShape(self, window):
        pos = self.rotate(blockSize, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(-blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

    def tShape(self, window):
        pos = self.rotate(blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(-blockSize, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, 0)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pos = self.rotate(0, -blockSize)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))

# Handles rendering board and running pathfinding algorithms
class Visualizer:

    def __init__(self):
        self.nodeWidth = (size - 100) // 10
        self.board = self.makeBoard()
        # self.curPiece = TetrisPiece(random.randrange(1,7),colorList[random.randrange(0,4)])
        self.curPiece = TetrisPiece(1,colorList[random.randrange(0,4)])
        self.pieceSpeed = 1

    def makeBoard(self):
        retBoard = []
        for i in range(20):
            rowList = []
            for j in range(10):
                newNode = Node(((i * blockSize), (j * blockSize) + offsetL), buttonCol, blockSize)
                rowList.append(newNode)

            retBoard.append(rowList)

        return retBoard

    def drawBoard(self, window):
        for i in range(20):
            y = i * blockSize
            pygame.draw.line(window, black, (offsetL, y), (offSetR, y))

        for j in range(11):
            x = offsetL + (j * blockSize)
            pygame.draw.line(window, black, (x, 0), (x, size))

    def draw(self, window):
        for row in self.board:
            for n in row:
                n.drawRect(window)

        self.drawBoard(window)
        self.curPiece.drawPiece(window)
        if self.curPiece.getY() < size - blockSize * 2:
            self.curPiece.moveY(self.pieceSpeed)
        pygame.display.update()

    def resetBoard(self):
        self.board = self.makeBoard()

    def getNode(self, pos):
        return self.board[pos[0]][pos[1]]

    def clickPos(self, pos):
        row = pos[0] // self.nodeWidth
        col = pos[1] // self.nodeWidth

        return (col, row)

    def addPiece(self, piece):
        self.curPiece = piece

    def movePieceX(self, incr):
        self.curPiece.moveX(incr)

    def movePiecey(self, incr):
        self.curPiece.moveY(incr)

    def rotatePiece(self, num):
        self.curPiece.newRotate(num)

    def dropPiece(self):
        self.pieceSpeed = 20

def main(window):
    vis = Visualizer()
    run = True
    clock = pygame.time.Clock()
    while run:
        vis.draw(window)
        clock.tick(60)
        for event in pygame.event.get():
            # If user presses x in corner of window
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    vis.movePieceX(-1)
                    vis.draw(window)
                elif event.key == pygame.K_d:
                    vis.movePieceX(1)
                    vis.draw(window)
                elif event.key == pygame.K_q:
                    vis.rotatePiece(-1)
                elif event.key == pygame.K_e:
                    vis.rotatePiece(1)
                elif event.key == pygame.K_SPACE:
                    vis.dropPiece()


    pygame.quit()

if __name__ == "__main__":
    main(window)