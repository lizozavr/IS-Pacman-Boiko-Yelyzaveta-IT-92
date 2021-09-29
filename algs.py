import pygame
from objects import *
from datetime import datetime
import sys
from game import *
import random


def findPathBFS(maze, startx, starty, endx, endy):
    startTime = datetime.now()
    startx = int(startx)
    starty = int(starty)
    endx = int(endx)
    endy = int(endy)

    queue = []
    queue.append((startx, starty))
    envhight = len(grid)
    envwidth = len(grid[0])
    Dir = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    weight = 1

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if maze[i][j] != 0:
                # unvisited dots
                visited[-1].append(0)
            else:
                visited[-1].append(True)

    visited[startx][starty] = 1
    oldcount = 1
    newCount = 0
    while len(queue) > 0:

        p = queue[0]
        queue.pop(0)

        if p[0] == endx and p[1] == endy:
            endTime = datetime.now()
            print('BFS work time:', endTime - startTime)
            print('path:', queue)
            return reconstructPath(visited, p[0], p[1])

        # Look at all 4 directions and add them to the queue
        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            # not blocked and valid
            if a >= 0 and b >= 0 and a < envhight and b < envwidth and visited[a][b] == 0 and visited[a][b] != True:
                visited[a][b] = weight + 1
                queue.append((a, b))
                newCount += 1

        oldcount -= 1
        if oldcount <= 0:
            oldcount = newCount
            newCount = 0
            weight += 1

    return queue


# reconstruct path for DFS algorithm
def reconstructPath(maze, x, y):
    stop = True
    envhight = len(maze)
    envwidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    queue = []
    queue.append((x, y))

    newArr = []
    for i in range(len(maze)):
        newArr.append([])
        for j in range(len(maze[i])):
            if (maze[i][j] == True):
                newArr[-1].append(0)
            else:
                newArr[-1].append(maze[i][j])

    maze = newArr

    while stop:
        p = queue[len(queue) - 1]
        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            # not blocked and valid
            if (a >= 0 and b >= 0 and a < envhight and b < envwidth and maze[a][b] != 0 and maze[a][b] < maze[p[0]][
                p[1]]):
                queue.append((a, b))
                # print(maze[a][b])
                break
        if (maze[p[0]][p[1]] == 2):
            stop = False
    return (queue)


def findPathDFS(maze, startx, starty, endx, endy):
    startTime = datetime.now()
    startx = int(startx)
    starty = int(starty)
    endx = int(endx)
    endy = int(endy)

    allpath = []
    queue = []

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if (maze[i][j] != 0):
                visited[-1].append(0)
            else:
                visited[-1].append(1)

    # Recursion func
    go_to(startx, starty, endx, endy, visited, queue, allpath)
    endTime = datetime.now()
    print('DFS work time:', endTime - startTime)
    print('path:', allpath[0])
    return allpath[0]


def go_to(startx, starty, endx, endy, visited, queue, allpath):
    if startx < 0 or starty < 0 or startx > len(visited) - 1 or starty > len(visited[0]) - 1:
        return
    # If we've already been there or there is a wall, quit
    if (startx, starty) in queue or visited[startx][starty] > 0:
        return
    queue.append((startx, starty))
    visited[startx][starty] = 2
    # if we've found goal point
    if (startx, starty) == (endx, endy):
        allpath.append(queue.copy())
        queue.pop()
        return
    else:
        go_to(startx - 1, starty, endx, endy, visited, queue, allpath)  # check top
        go_to(startx + 1, starty, endx, endy, visited, queue, allpath)  # check bottom
        go_to(startx, starty + 1, endx, endy, visited, queue, allpath)  # check right
        go_to(startx, starty - 1, endx, endy, visited, queue, allpath)  # check left
    queue.pop()
    return


class Node:
    def __init__(self, x, y, bNode=None):
        self.X = x
        self.Y = y
        self.Node = bNode

    def name(self, b):
        if self.Node != None:
            b.append(self.Node)
            print(self.X, " ", self.Y)
            return self.name(b)
        else:
            return b


def randomizeWeights(field):
    newField = []
    visitedFieldBig = []
    r = random

    for i in range(len(field) * 2 - 1):
        row = []
        clearRow = []
        for j in range(len(field[0]) * 2 - 1):
            if (i % 2 == 0) and (j % 2 == 0):
                row.append(field[int(i / 2)][int(j / 2)])
                if field[int(i / 2)][int(j / 2)] == 1:
                    clearRow.append(0)
                elif field[int(i / 2)][int(j / 2)] == 2:
                    clearRow.append(0)
                else:
                    clearRow.append(1)
            elif (i % 2 != 0) and (j % 2 != 0):
                row.append(0)
                clearRow.append(1)
            else:
                row.append(random.randint(4, 9))
                clearRow.append(0)
        newField.append(row)
        visitedFieldBig.append(clearRow)

    return newField, visitedFieldBig


def reconstructPathForUCS(node):
    queue = []
    while node != None:
        queue.append((node.X / 2, node.Y / 2))
        node = node.Node
    return queue


def UCS(maze, startX, startY, endX, endY):
    startX = int(startX) * 2
    startY = int(startY) * 2
    endX = int(endX) * 2
    endY = int(endY) * 2

    # list of Nodes (with coordinates)
    nodesList = []
    # Nodes weights
    nodesWeightsList = []

    nodesList.append(Node(startX, startY, None))
    nodesWeightsList.append(0)

    # randomize weights for fields
    field, visited = randomizeWeights(maze)

    startNode = None

    startTime = datetime.now()
    while len(nodesList) > 0:
        minIndex = nodesWeightsList.index(min(nodesWeightsList))
        node = nodesList[minIndex]
        weightNode = nodesWeightsList[minIndex]
        nodesWeightsList[minIndex] = sys.maxsize

        startNode = Node(node.X, node.Y, startNode)
        visited[node.X][node.Y] = 1

        # if we find endpoint
        if node.X == endX and node.Y == endY:
            endTime = datetime.now()
            print('UCS work time:', endTime - startTime)
            print('Path:', reconstructPathForUCS(node))
            return reconstructPathForUCS(node)

        tempArray = []
        tempWeightIndexesArray = []
        # check all 4 directions
        if node.X - 2 >= 0 and visited[node.X - 2][node.Y] != 1:
            tempArray.append(Node(node.X - 2, node.Y, node))
            asd = field[node.X - 1][node.Y]
            tempWeightIndexesArray.append(weightNode + field[node.X - 1][node.Y])
        if node.Y - 2 >= 0 and visited[node.X][node.Y - 2] != 1:
            tempArray.append(Node(node.X, node.Y - 2, node))
            asd = field[node.X][node.Y - 1]
            tempWeightIndexesArray.append(weightNode + field[node.X][node.Y - 1])
        if node.X + 2 < len(field) and visited[node.X + 2][node.Y] != 1:
            tempArray.append(Node(node.X + 2, node.Y, node))
            asd = field[node.X + 1][node.Y]
            tempWeightIndexesArray.append(weightNode + field[node.X + 1][node.Y])
        if node.Y + 2 < len(field[0]) and visited[node.X][node.Y + 2] != 1:
            tempArray.append(Node(node.X, node.Y + 2, node))
            asd = field[node.X][node.Y + 1]
            tempWeightIndexesArray.append(weightNode + field[node.X][node.Y + 1])

        # collect found dots from all directions to lists
        while len(tempArray) > 0:
            tempNode = tempArray.pop()
            nodesList.append(tempNode)
            nodesWeightsList.append(tempWeightIndexesArray.pop())


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def euclideanSquared(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def Astar(maze, startX, startY, endX, endY, heuristic):
    startX = int(startX) * 2
    startY = int(startY) * 2
    endX = int(endX) * 2
    endY = int(endY) * 2

    # list of Nodes (with coordinates)
    nodesList = []
    # Nodes weights
    nodesWeightsList = []

    nodesList.append(Node(startX, startY, None))
    nodesWeightsList.append(0)

    # randomize weights for fields
    field, visited = randomizeWeights(maze)

    startTime = datetime.now()
    startNode = None

    while len(nodesList) > 0:
        minIndex = nodesWeightsList.index(min(nodesWeightsList))
        node = nodesList[minIndex]
        weightNode = nodesWeightsList[minIndex]
        field[node.X][node.Y] = weightNode
        nodesWeightsList[minIndex] = sys.maxsize

        startNode = Node(node.X, node.Y, startNode)
        visited[node.X][node.Y] = 1

        # if we find endpoint
        if node.X == endX and node.Y == endY:
            endTime = datetime.now()
            print('Astar work time:', endTime - startTime)

            queue = reconstructPathForUCS(node)
            print('Path:', queue)
            return queue, field

        tempArray = []
        tempWeightIndexesArray = []
        if node.X - 2 >= 0 and visited[node.X - 2][node.Y] != 1:
            tempArray.append(Node(node.X - 2, node.Y, node))
            asd = field[node.X - 1][node.Y]
            tempWeightIndexesArray.append(
                weightNode + field[node.X - 1][node.Y] + heuristic((node.X - 1, node.Y), (endX, endY)))
        if node.Y - 2 >= 0 and visited[node.X][node.Y - 2] != 1:
            tempArray.append(Node(node.X, node.Y - 2, node))
            asd = field[node.X][node.Y - 1]
            tempWeightIndexesArray.append(
                weightNode + field[node.X][node.Y - 1] + heuristic((node.X, node.Y - 1), (endX, endY)))
        if node.X + 2 < len(field) and visited[node.X + 2][node.Y] != 1:
            tempArray.append(Node(node.X + 2, node.Y, node))
            asd = field[node.X + 1][node.Y]
            tempWeightIndexesArray.append(
                weightNode + field[node.X + 1][node.Y] + heuristic((node.X + 1, node.Y), (endX, endY)))
        if node.Y + 2 < len(field[0]) and visited[node.X][node.Y + 2] != 1:
            tempArray.append(Node(node.X, node.Y + 2, node))
            asd = field[node.X][node.Y + 1]
            tempWeightIndexesArray.append(
                weightNode + field[node.X][node.Y + 1] + heuristic((node.X, node.Y + 1), (endX, endY)))

        while len(tempArray) > 0:
            tempNode = tempArray.pop()
            nodesList.append(tempNode)
            nodesWeightsList.append(tempWeightIndexesArray.pop())

    # back to normal array
    a = []
    for item in nodesList:
        hehe = nodesList.pop()
        a.append((int(hehe[0] / 2), int(hehe[1] / 2)))
    queue = a
    print(queue)
    print(nodesWeightsList)
    for i in range(len(field) - 1):
        if i % 2 == 0:
            print()
            for j in range(len(field[0]) - 1):
                if j % 2 == 0:
                    print(field[i][j], end='')

    for i in range(len(visited)):
        print(visited[i])


def buildPathThrowDots(dots):
    fullPath = []
    for item in range(len(dots) - 1):
        aStarPath, field = Astar(grid, dots[item][0], dots[item][1], dots[item + 1][0], dots[item + 1][1], heuristic)
        aStarPath.reverse()
        fullPath.append(aStarPath)
    path = []
    for row in fullPath:
        for item in row:
            path.append(item)
    return path
