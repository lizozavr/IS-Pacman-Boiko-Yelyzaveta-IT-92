import random

from game import Grid
import os


# Керує статичною інформацією про поле гри
class Layout:

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agentPositions = []
        self.numGhosts = 0
        self.processLayoutText(layoutText)
        self.layoutText = layoutText

    # Отримати кількість привидів
    def getNumGhosts(self):
        return self.numGhosts

    def deepCopy(self):
        return Layout(self.layoutText[:])

    # Опрацювання символів із написаних полів для гри
    # % - Стіна
    # . - Їжа
    # o - Капсула
    # G - Привид
    # P - Pac-man
    def processLayoutText(self, layoutText):
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)
        self.agentPositions.sort()
        self.agentPositions = [(i == 0, pos) for i, pos in self.agentPositions]

    # Опрацювання одного символу
    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.food[x][y] = True
        elif layoutChar == 'o':
            self.capsules.append((x, y))
        elif layoutChar == 'P':
            self.agentPositions.append((0, (x, y)))
        elif layoutChar in ['G']:
            self.agentPositions.append((1, (x, y)))
            self.numGhosts += 1
        elif layoutChar in ['1', '2', '3', '4']:
            self.agentPositions.append((int(layoutChar), (x, y)))
            self.numGhosts += 1


# Завантаження поля
def getLayout(name, numGhosts=1, back=2):
    if name == 'randomClassic':
        return randomClassic(numGhosts)
    if name == 'randomMaze':
        return randomMaze()
    if name == 'randomCorners':
        return randomCorners()
    if name == 'randomSearch':
        return randomSearch()
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name)
        if layout is None:
            layout = tryToLoad(name)
    else:
        layout = tryToLoad('layouts/' + name + '.lay')
        if layout is None:
            layout = tryToLoad(name + '.lay')
    if layout is None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back - 1)
        os.chdir(curdir)
    return layout


# Генерація поля для для класичної гри
def randomClassic(numGhosts):
    height = 15
    width = 15
    layout_2d = initRandMaze(width, height, 220)
    curr_num_ghost = numGhosts
    pacman_count = 1
    while curr_num_ghost != 0:
        y = int(random.random() * height)
        x = int(random.random() * width)
        if x != height - 1 and x > 2 and y != width - 1 and y > 2:
            if layout_2d[x][y] != '%':
                layout_2d[x][y] = 'G'
                curr_num_ghost -= 1
    while pacman_count != 0:
        y = int(random.random() * height)
        x = int(random.random() * width)
        if x != height - 1 and x > 2 and y != width - 1 and y > 2:
            if layout_2d[x][y] != '%' and layout_2d[x][y] != 'G' and layout_2d[x + 1][y] != 'G' \
                    and layout_2d[x - 1][y] != 'G' and layout_2d[x][y - 1] != 'G' and layout_2d[x][y + 1] != 'G':
                layout_2d[x][y] = 'P'
                pacman_count -= 1
    for i in range(0, height):
        for j in range(0, width):
            if layout_2d[i][j] == ' ':
                layout_2d[i][j] = '.'
    return Layout(flattedMaze(layout_2d))


# Генерація поля для для проблеми пошуку точки
def randomMaze():
    layout_2d = initRandMaze(20, 20)
    layout_2d[18][1] = '.'
    layout_2d[1][18] = 'P'
    return Layout(flattedMaze(layout_2d))


# Генерація поля для проблеми пошуку 4 точок
def randomCorners():
    layout_2d = initRandMaze(20, 20, 7)
    layout_2d[18][1] = '.'
    layout_2d[1][18] = '.'
    layout_2d[1][1] = '.'
    layout_2d[18][18] = '.'
    layout_2d[10][10] = 'P'
    return Layout(flattedMaze(layout_2d))


# Генерація поля для проблеми пошуку всієї їжі
def randomSearch():
    height = 20
    width = 20
    layout_2d = initRandMaze(height, width, 25)

    num_of_rand_dots = 7

    while num_of_rand_dots != 0:
        y = int(random.random() * height)
        x = int(random.random() * width)
        if x != height - 1 and x > 2 and y != width - 1 and y > 2:
            if layout_2d[x][y] != '%':
                layout_2d[x][y] = '.'
                num_of_rand_dots -= 1
    layout_2d[10][10] = 'P'
    return Layout(flattedMaze(layout_2d))


# Конвертація двувимірної матриці у список
def flattedMaze(layout_2d):
    layout = []
    for i in range(len(layout_2d)):
        flat_line = ''
        for j in range(len(layout_2d[i])):
            flat_line += layout_2d[i][j]
        layout.append(flat_line)
    return layout


# Алгоритм генерації випадкового лабіринту (за випадковим алгоритмом Прима)
def initRandMaze(width, height, num_of_rand_holes=120):
    maze = []
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append('u')
        maze.append(line)

    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)

    if starting_height == 0:
        starting_height += 1
    if starting_height == height - 1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width - 1:
        starting_width -= 1

    maze[starting_height][starting_width] = ' '
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    maze[starting_height - 1][starting_width] = '%'
    maze[starting_height][starting_width - 1] = '%'
    maze[starting_height][starting_width + 1] = '%'
    maze[starting_height + 1][starting_width] = '%'

    def surroundingCells(rand_wall):
        s_cells = 0
        if maze[rand_wall[0] - 1][rand_wall[1]] == ' ':
            s_cells += 1
        if maze[rand_wall[0] + 1][rand_wall[1]] == ' ':
            s_cells += 1
        if maze[rand_wall[0]][rand_wall[1] - 1] == ' ':
            s_cells += 1
        if maze[rand_wall[0]][rand_wall[1] + 1] == ' ':
            s_cells += 1
        return s_cells

    while walls:
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        if rand_wall[1] != 0:
            if maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze[rand_wall[0]][rand_wall[1] + 1] == ' ':
                s_cells = surroundingCells(rand_wall)

                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = ' '

                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != ' ':
                            maze[rand_wall[0] - 1][rand_wall[1]] = '%'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != ' ':
                            maze[rand_wall[0] + 1][rand_wall[1]] = '%'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != ' ':
                            maze[rand_wall[0]][rand_wall[1] - 1] = '%'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        if rand_wall[0] != 0:
            if maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze[rand_wall[0] + 1][rand_wall[1]] == ' ':

                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:

                    maze[rand_wall[0]][rand_wall[1]] = ' '

                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != ' ':
                            maze[rand_wall[0] - 1][rand_wall[1]] = '%'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != ' ':
                            maze[rand_wall[0]][rand_wall[1] - 1] = '%'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != ' ':
                            maze[rand_wall[0]][rand_wall[1] + 1] = '%'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        if rand_wall[0] != height - 1:
            if maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze[rand_wall[0] - 1][rand_wall[1]] == ' ':

                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = ' '

                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != ' ':
                            maze[rand_wall[0] + 1][rand_wall[1]] = '%'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != ' ':
                            maze[rand_wall[0]][rand_wall[1] - 1] = '%'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != ' ':
                            maze[rand_wall[0]][rand_wall[1] + 1] = '%'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        if rand_wall[1] != width - 1:
            if maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze[rand_wall[0]][rand_wall[1] - 1] == ' ':

                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = ' '

                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != ' ':
                            maze[rand_wall[0]][rand_wall[1] + 1] = '%'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])
                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != ' ':
                            maze[rand_wall[0] + 1][rand_wall[1]] = '%'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != ' ':
                            maze[rand_wall[0] - 1][rand_wall[1]] = '%'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == 'u':
                maze[i][j] = '%'

    while num_of_rand_holes != 0:
        y = int(random.random() * height)
        x = int(random.random() * width)
        if x != height - 1 and x > 2 and y != width - 1 and y > 2:
            maze[x][y] = ' '
            num_of_rand_holes -= 1

    return maze


# Завантаження поля із заданою назвою
def tryToLoad(fullname):
    if not os.path.exists(fullname):
        return None
    f = open(fullname)
    try:
        return Layout([line.strip() for line in f])
    finally:
        f.close()
