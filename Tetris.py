import random

import pygame, sys
from multiprocessing import pool
import collections
import math

pygame.init()

size = 800
blockSize = size // 20
halfBlock = blockSize // 2
offsetL = (size - (blockSize * 10)) // 2
offSetR = size - offsetL
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Tetris")
font = pygame.font.SysFont('Constantia', 30)

green = (114, 203, 59)
teal = (0, 255, 255)
yellow = (255, 213, 0)
purple = (128, 0, 128)
orange = (255, 151, 28)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 50, 19)
blue = (3, 65, 174)
buttonCol = 189, 181, 177

colorList = [blue, green, yellow, orange, red, teal, purple]

# Allows for the creation of a button with text and reaction to being pressed
class Button:

    def __init__(self, x, y, wide, high, text, onlyText):
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
        self.filled = False

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getColor(self):
        self.color = red
        return self.color

    def moveY(self, incr):
        self.y += blockSize * incr

    def setColor(self, newColor):
        self.color = newColor

    def getPosition(self):
        return self.pos

    def isFilled(self):
        self.filled = True

    def getFilled(self):
        return self.filled

    def drawRect(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def drawOutline(self, window):
        if self.filled:
            pygame.draw.line(window, black, (self.x, self.y), (self.x + self.width, self.y))
            pygame.draw.line(window, black, (self.x, self.y), (self.x, self.y + self.width))
            pygame.draw.line(window, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.width))
            pygame.draw.line(window, black, (self.x, self.y + self.width), (self.x + self.width, self.y + self.width))

# Makes and renders shape
class TetrisPiece:

    def __init__(self, pieceNum, color):
        self.color = color
        self.y = 0
        self.x = (blockSize * 4) + offsetL
        self.rotateNum = 1
        self.shape = None
        self.posList = []
        self.xMax = blockSize * 2
        self.xMin = -blockSize
        self.yMax = blockSize
        self.yMin = -blockSize
        self.pieceNum = pieceNum
        if pieceNum == 1:
            self.shape = self.sShape
        elif pieceNum == 2:
            self.shape = self.zShape
        elif pieceNum == 3:
            self.shape = self.iShape
            self.xMin = -blockSize * 2
            self.yMin = 0
        elif pieceNum == 4:
            self.shape = self.boxShape
            self.xMax = blockSize
        elif pieceNum == 5:
            self.shape = self.jShape
            self.xMin = -blockSize
        elif pieceNum == 6:
            self.shape = self.lShape
            self.xMin = -blockSize
        elif pieceNum == 7:
            self.shape = self.tShape

    def drawPiece(self, window):
        self.shape(window)

    def getColor(self):
        return self.color

    def moveY(self, increment):
        self.y += increment

    def moveX(self, increment):
        self.x += increment * blockSize

    def getY(self):
        return self.y

    def getXMax(self):
        return self.x + self.xMax

    def getXMin(self):
        return self.x + self.xMin

    def getYMax(self):
        return self.y + self.yMax

    def getYMin(self):
        return self.y + self.yMin

    def newRotate(self, num):
        if self.rotateNum + num < 1:
            self.rotateNum = 4
        elif self.rotateNum + num > 4:
            self.rotateNum = 1
        else:
            self.rotateNum += num

        if self.rotateNum == 1:
            self.yMax = blockSize
            self.yMin = -blockSize
            if self.pieceNum == 4:
                self.xMax = blockSize
                self.xMin = -blockSize
            elif self.pieceNum == 3:
                self.yMin = 0
                self.xMax = blockSize * 2
                self.xMin = -blockSize * 2
            else:
                self.xMax = blockSize * 2
                self.xMin = -blockSize
        elif self.rotateNum == 2:
            self.xMin = 0
            self.yMin = -blockSize
            if self.pieceNum == 3:
                self.xMax = blockSize
                self.yMax = blockSize * 2
                self.yMin = -blockSize * 2
            elif self.pieceNum == 4:
                self.xMax = blockSize * 2
                self.yMax = blockSize
            else:
                self.xMax = blockSize * 2
                self.yMax = blockSize * 2
        elif self.rotateNum == 3:
            self.yMin = 0
            if self.pieceNum == 3:
                self.xMax = blockSize * 3
                self.xMin = -blockSize
                self.yMax = blockSize
            elif self.pieceNum == 4:
                self.xMax = blockSize * 2
                self.xMin = 0
                self.yMax = blockSize * 2
            else:
                self.xMax = blockSize * 2
                self.xMin = -blockSize
                self.yMax = blockSize * 2
        else:
            self.yMin = -blockSize
            if self.pieceNum == 3:
                self.xMax = blockSize
                self.xMin = 0
                self.yMax = blockSize * 3
            elif self.pieceNum == 4:
                self.yMin = 0
                self.xMax = blockSize
                self.xMin = -blockSize
                self.yMax = blockSize
            else:
                self.xMax = blockSize
                self.xMin = -blockSize
                self.yMax = blockSize * 2

        if self.x + self.xMax > offSetR:
            self.x -= ((self.x + self.xMax) - offSetR)
        elif self.x + self.xMin < offsetL:
            self.x += (offsetL - (self.x + self.xMin))

    def rotate(self, x, y):
        if self.rotateNum == 1:
            return (self.x + x, self.y + y)
        elif self.rotateNum == 2:
            return (self.x + (y * -1), self.y + x)
        elif self.rotateNum == 3:
            return (self.x + (x * -1), self.y + (y * -1))
        elif self.rotateNum == 4:
            return (self.x + y, self.y + (x * -1))

    def getPosList(self):
        return self.posList

    def sShape(self, window):
        self.posList.clear()
        pos = self.rotate(blockSize, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(-blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

    def zShape(self, window):
        self.posList.clear()
        pos = self.rotate(-blockSize, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

    def iShape(self, window):
        self.posList.clear()
        pos = self.rotate(-(blockSize * 2), 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(-blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

    def boxShape(self, window):
        self.posList.clear()
        pos = self.rotate(-blockSize, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(-blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

    def jShape(self, window):
        self.posList.clear()
        pos = self.rotate(-blockSize, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(-blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

    def lShape(self, window):
        self.posList.clear()
        pos = self.rotate(blockSize, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(-blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

    def tShape(self, window):
        self.posList.clear()
        pos = self.rotate(blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(-blockSize, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, 0)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))
        pos = self.rotate(0, -blockSize)
        self.posList.append(pos)
        pygame.draw.rect(window, self.color, (pos[0], pos[1], blockSize, blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0] + blockSize, pos[1]))
        pygame.draw.line(window, black, (pos[0], pos[1]), (pos[0], pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0] + blockSize, pos[1]), (pos[0] + blockSize, pos[1] + blockSize))
        pygame.draw.line(window, black, (pos[0], pos[1] + blockSize), (pos[0] + blockSize, pos[1] + blockSize))

# Handles rendering board and running pathfinding algorithms
class Visualizer:

    def __init__(self):
        self.nodeWidth = (size - 100) // 10
        self.board = self.makeBoard()
        self.curPiece = TetrisPiece(random.randrange(1,8),colorList[random.randrange(0,7)])
        self.pieceSpeed = 1
        self.gameOver = False
        self.score = 0
        self.scoreMap = {0 : 0, 1 : 40, 2 : 100, 3 : 300, 4 : 1200}

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
        for i in range(20):
            iL = 0
            iR = 1
            while iR < 10:
                self.board[i][iL].drawRect(window)
                self.board[i][iR].drawRect(window)
                self.board[i][iL].drawOutline(window)

                if iR == 9:
                    self.board[i][iR].drawOutline(window)

                if iL != 0:
                    self.board[i][iL - 1].drawOutline(window)

                iL += 1
                iR += 1

        self.drawScore(window)

        if not self.gameOver:
            self.curPiece.drawPiece(window)
            if self.curPiece.getYMax() < size:
                self.curPiece.moveY(self.pieceSpeed)
                for pos in self.curPiece.getPosList():
                    y = ((pos[1] + blockSize) // blockSize)
                    x = ((pos[0] - offsetL) // blockSize)
                    if x >= 0 and x < 10 and y >= 0 and self.board[y][x].getFilled():
                        self.boardAdd()
                        break
            else:
                self.boardAdd()

        pygame.display.update()

    def boardAdd(self):
        for pos in self.curPiece.getPosList():
            y = (pos[1] // blockSize)
            x = ((pos[0] - offsetL) // blockSize)
            if y >= 0:
                self.board[y][x].setColor(self.curPiece.getColor())
                self.board[y][x].isFilled()

        self.rowCheck()

        if self.curPiece.getYMin() // blockSize <= 0:
            self.gameOver = True
        else:
            self.pieceSpeed = 1
            self.curPiece = TetrisPiece(random.randrange(1,8),colorList[random.randrange(0,7)])

    def rowCheck(self):
        prevRow = -1
        rowDrop = 0
        for i in range(19, -1, -1):
            count = 0
            if prevRow == 0:
                break
            for j in range(10):
                curSquare = self.board[i][j]

                if curSquare.getFilled():
                    count += 1

                if rowDrop != 0:
                    curSquare.moveY(rowDrop)
                    self.board[i + rowDrop][j] = curSquare
                    newNode = Node(((i * blockSize), (j * blockSize) + offsetL), buttonCol, blockSize)
                    self.board[i][j] = newNode

            if count == 10:
                rowDrop += 1
                self.score += self.scoreMap[rowDrop] * (i + 1)

            prevRow = count

    def drawScore(self, window):
        text1 = font.render("Score", True, white)
        text2 = font.render("{0}".format(self.score), True, white)
        sideRect = pygame.Rect(offSetR, 0, size - offSetR, blockSize * 10)
        pygame.draw.rect(window, black, sideRect)
        scoreText = pygame.Rect(offSetR + 50, 25, 50, 25)
        scoreRect = pygame.Rect(offSetR + 50, 50, 50, 50)
        window.blit(text1, scoreText.center)
        window.blit(text2, scoreRect.center)

    def resetBoard(self):
        self.board = self.makeBoard()

    def getNode(self, pos):
        return self.board[pos[0]][pos[1]]

    def addPiece(self, piece):
        self.curPiece = piece

    def movePieceX(self, incr):
        if incr == 1 and self.curPiece.getXMax() < offSetR or incr == -1 and self.curPiece.getXMin() > offsetL:
            self.curPiece.moveX(incr)

    def movePieceY(self, incr):
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