import pygame
import heapq
import math

size = 800
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pathfinding Visualizer")

green = (51, 255, 51)
yellow = (248, 255, 51)
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 22, 11)
blue = (11, 27, 240)

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

class Pathfinder:

    def __init__(self, start, end, board):
        self.start = start
        self.end = end
        self.board = board

    def mDist(self, pos):
        return abs(pos[0] - self.end[0]) + abs(pos[1] - self.end[1])

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

    def getNode(self, pos):
        return self.board[pos[0]][pos[1]]

    def getNodeColor(self, pos):
        return self.board[pos[0]][pos[1]].getColor()

    def clickPos(self, pos):
        row = pos[0] // self.nodeWidth
        col = pos[1] // self.nodeWidth

        return (col, row)

    def changeColor(self, pos, newColor):
        self.board[pos[0]][pos[1]].setColor(newColor)

    def setBarrier(self, pos, bar):
        self.board[pos[0]][pos[1]].setBarrier(bar)


def main(window):
    rows = 50
    vis = Visualizer(rows)
    start = False
    end = False
    startPos = (-1, -1)
    endPos = (-1, -1)
    run = True
    started = False
    while run:
        vis.draw(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = vis.clickPos(pygame.mouse.get_pos())
                if not start:
                    start = True
                    vis.changeColor(pos, red)
                    startPos = pos
                elif not end:
                    end = True
                    vis.changeColor(pos, blue)
                    endPos = pos
                elif start and pos == startPos:
                    start = False
                    vis.changeColor(pos, white)
                elif end and pos == endPos:
                    end = False
                    vis.changeColor(pos, white)
            elif pygame.mouse.get_pressed()[2]:
                pos = vis.clickPos(pygame.mouse.get_pos())
                vis.changeColor(pos, black)
                vis.setBarrier(pos, True)


    pygame.quit()

if __name__ == "__main__":
    main(window)