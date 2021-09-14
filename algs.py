import pygame
from objects import *
from datetime import datetime


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
            if (maze[i][j] != 0):
                visited[-1].append(0)
            else:
                visited[-1].append(True)

    visited[startx][starty] = 1
    oldcount = 1
    newCount = 0
    while len(queue) > 0:

        p = queue[0]
        queue.pop(0)

        if (p[0] == endx and p[1] == endy):
            endTime = datetime.now()
            print('BFS work time:', endTime - startTime)
            print('path:', queue)
            return reconstructPath(visited, p[0], p[1])

        # print(maze[p[0]][p[1]])

        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            # not blocked and valid
            if (a >= 0 and b >= 0 and a < envhight and b < envwidth and visited[a][b] == 0 and visited[a][b] != True):
                visited[a][b] = weight + 1
                queue.append((a, b))
                newCount += 1

        oldcount -= 1
        if (oldcount <= 0):
            oldcount = newCount
            newCount = 0
            weight += 1

    return queue


def reconstructPath(maze, x, y):
    stop = True
    envhight = len(maze)
    envwidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    queue = []
    queue.append((x, y))

    # maze[maze == True] = 0
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
    # queue.append((startx,starty))
    envhight = len(grid)
    envwidth = len(grid[0])

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if (maze[i][j] != 0):
                visited[-1].append(0)
            else:
                visited[-1].append(1)

    go_to(startx, starty, endx, endy, visited, queue, allpath)
    endTime = datetime.now()
    print('DFS work time:', endTime - startTime)
    print('path:', queue)
    return allpath[0]


def go_to(startx, starty, endx, endy, visited, queue, allpath):
    if startx < 0 or starty < 0 or startx > len(visited) - 1 or starty > len(visited[0]) - 1:
        return
    # If we've already been there or there is a wall, quit
    if (startx, starty) in queue or visited[startx][starty] > 0:
        return
    queue.append((startx, starty))
    visited[startx][starty] = 2
    if (startx, starty) == (endx, endy):
        # print("Found!", queue)
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


def uniform_cost_search(goal, start):
    global graph, cost
    answer = []
    # create a priority queue
    queue = []
    # set the answer vector to max value
    for i in range(len(goal)):
        answer.append(10 ** 8)
    # insert the starting index
    queue.append([0, start])
    # map to store visited node
    visited = {}
    # count
    count = 0
    # while the queue is not empty
    while (len(queue) > 0):

        # get the top element of the
        queue = sorted(queue)
        p = queue[-1]
        # pop the element
        del queue[-1]
        # get the original value
        p[0] *= -1
        # check if the element is part of
        # the goal list
        if (p[1] in goal):
            # get the position
            index = goal.index(p[1])
            # if a new goal is reached
            if (answer[index] == 10 ** 8):
                count += 1
            # if the cost is less
            if (answer[index] > p[0]):
                answer[index] = p[0]
            # pop the element
            del queue[-1]
            queue = sorted(queue)
            if (count == len(goal)):
                return answer

        # check for the non visited nodes
        # which are adjacent to present node
        if (p[1] not in visited):
            for i in range(len(graph[p[1]])):
                # value is multiplied by -1 so that
                # least priority is at the top
                queue.append([(p[0] + cost[(p[1], graph[p[1]][i])]) * -1, graph[p[1]][i]])

        # mark as visited
        visited[p[1]] = 1
    return answer


# main function
if __name__ == '__main__':
    # create the graph
    graph, cost = [[] for i in range(8)], {}

    # add edge
    graph[0].append(1)
    graph[0].append(3)
    graph[3].append(1)
    graph[3].append(6)
    graph[3].append(4)
    graph[1].append(6)
    graph[4].append(2)
    graph[4].append(5)
    graph[2].append(1)
    graph[5].append(2)
    graph[5].append(6)
    graph[6].append(4)

    # add the cost
    cost[(0, 1)] = 2
    cost[(0, 3)] = 5
    cost[(1, 6)] = 1
    cost[(3, 1)] = 5
    cost[(3, 6)] = 6
    cost[(3, 4)] = 2
    cost[(2, 1)] = 4
    cost[(4, 2)] = 4
    cost[(4, 5)] = 3
    cost[(5, 2)] = 6
    cost[(5, 6)] = 3
    cost[(6, 4)] = 7

    # goal state
    goal = []
    # set the goal
    # there can be multiple goal states
    goal.append(6)
    # get the answer
    answer = uniform_cost_search(goal, 0)
    # print the answer
    print("Minimum cost from 0 to 6 is = ", answer[0])
