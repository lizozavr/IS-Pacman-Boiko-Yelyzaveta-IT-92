import enum
import pygame
import algs
import generateLabirinth

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 544

# Define some colors
BLACK = (0, 0, 0)
BLUE = (51, 51, 255)

# game field
# grid = generateLabirinth.generateMaze(17, 17)
grid = ((2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,),
        (1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1,),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,),
        (1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,),
        (1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,),
        (1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1,),
        (1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1,),
        (1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,),
        (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,),
        (1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1,),
        (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,),
        (1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,),
        (1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1,),
        (1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1,),
        (1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,),
        (1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1,),
        (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4,))

# environment height and width
envheight = len(grid)
envwidth = len(grid[0])


# Block that keep player in playfield
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Food
class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Enemies
class Ghost(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    def __init__(self, x, y, t):
        pygame.sprite.Sprite.__init__(self)
        # image of ghost
        self.image = pygame.image.load("pictures/Ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.path = []
        self.step_value = 1
        self.prevPoint = (0, 0)
        self.nextPoint = (0, 0)
        self.type = t

    def update(self, point):
        self.nextPoint = point

        if len(self.path) == 0 or self.nextPoint != self.prevPoint:
            self.path = algs.findPathBFS(grid, (self.rect.y + 16) / 32, (self.rect.x + 16) / 32, point[0], point[1])
            self.prevPoint = self.nextPoint
            self.path.reverse()
        self.goTo(self.path)
        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def goTo(self, path):
        if len(path) >= 1:
            next = path[0]
            x = (self.rect.x / 32)
            y = (self.rect.y / 32)

            if next[1] == x and next[0] == y:
                path.remove(next)
                self.change_x = 0
                self.change_y = 0
            else:
                if abs(x - next[1]) == 0:
                    self.change_x = 0
                    if y - next[0] < 0:
                        self.change_y = self.step_value
                    if y - next[0] > 0:
                        self.change_y = -self.step_value
                if y - next[0] == 0:
                    self.change_y = 0
                    if x - next[1] < 0:
                        self.change_x = self.step_value
                    if x - next[1] > 0:
                        self.change_x = -self.step_value


class ghostType(enum.Enum):
    random_moving_type = 1
    directed_moving_type = 2


# Draw walls
def draw_enviroment(screen):
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item >= 1:
                if j + 1 < envwidth and grid[i][j + 1] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32 + 32, i * 32], 3)
                elif j + 1 == envwidth:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32 + 32, i * 32], 3)
                if grid[i][j - 1] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                elif j == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                if i + 1 < envheight and grid[i + 1][j] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32, i * 32 + 32], 3)
                elif i + 1 == envheight:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32, i * 32 + 32], 3)
                if grid[i - 1][j] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
                elif i == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
