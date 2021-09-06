import pygame, sys
import heapq
import math

pygame.init()

size = 800
window = pygame.display.set_mode((size, size + 50))
pygame.display.set_caption("Pathfinding Visualizer")
font = pygame.font.SysFont('Constantia', 30)

green = (51, 255, 51)
yellow = (248, 255, 51)
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 22, 11)
blue = (11, 27, 240)
buttonCol = 189, 181, 177

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

    def isBarrier(self, pos):
        return self.board[pos[0]][pos[1]].isBarrier()

    def mDist(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def aStar(self, start, end, window):
        pq = []
        heapq.heappush(pq, (0, start, 0))
        visited = set()
        while len(pq) != 0:
            cur = heapq.heappop(pq)
            pos = cur[1]
            trav = cur[2]
            self.changeColor(pos, green)

            if self.mDist(pos, end) == 0:
                break

            if pos[0] - 1 >= 0:
                newPos1 = (pos[0] - 1, pos[1])
                if newPos1 not in visited and not self.isBarrier(newPos1):
                    visited.add(newPos1)
                    self.changeColor(newPos1, yellow)
                    heapq.heappush(pq, (trav + 1 + self.mDist(newPos1, end), newPos1, trav + 1))

            if pos[0] + 1 < self.rows:
                newPos2 = (pos[0] + 1, pos[1])
                if newPos2 not in visited and not self.isBarrier(newPos2):
                    visited.add(newPos2)
                    self.changeColor(newPos2, yellow)
                    heapq.heappush(pq, (trav + 1 + self.mDist(newPos2, end), newPos2, trav + 1))

            if pos[1] - 1 >= 0:
                newPos3 = (pos[0], pos[1] - 1)
                if newPos3 not in visited and not self.isBarrier(newPos3):
                    visited.add(newPos3)
                    self.changeColor(newPos3, yellow)
                    heapq.heappush(pq, (trav + 1 + self.mDist(newPos3, end), newPos3, trav + 1))

            if pos[1] + 1 < self.rows:
                newPos4 = (pos[0], pos[1] + 1)
                if newPos4 not in visited and not self.isBarrier(newPos4):
                    visited.add(newPos4)
                    self.changeColor(newPos4, yellow)
                    heapq.heappush(pq, (trav + 1 + self.mDist(newPos4, end), newPos4, trav + 1))

            self.draw(window)

def main(window):
    rows = 50
    vis = Visualizer(rows)
    start = False
    end = False
    startPos = (0,0)
    endPos = (0,0)
    run = True
    started = False
    button1 = Button(10, 810, 100, 30, 'A*')
    button2 = Button(120, 810, 100, 30, 'Start')
    button3 = Button(230, 810, 100, 30, 'Reset')
    startRect = button2.buttonRect
    resetRect = button3.buttonRect
    while run:
        vis.draw(window)
        button1.render(window)
        button2.render(window)
        button3.render(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            mousePos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                pos = vis.clickPos(mousePos)
                if mousePos[1] < size:
                    if not start:
                        start = True
                        vis.changeColor(pos, red)
                        startPos = pos
                    elif not end:
                        end = True
                        vis.changeColor(pos, blue)
                        endPos = pos
                    else:
                        vis.changeColor(pos, black)
                        vis.setBarrier(pos, True)
                elif startRect.collidepoint(mousePos) and start and end:
                    vis.aStar(startPos, endPos, window)
                elif resetRect.collidepoint(mousePos):
                    start = False
                    end = False
                    vis.resetBoard()

    pygame.quit()

if __name__ == "__main__":
    main(window)