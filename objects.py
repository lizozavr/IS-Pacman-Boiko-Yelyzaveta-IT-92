import pygame

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 544

# Define some colors
BLACK = (0, 0, 0)
BLUE = (51, 51, 255)

# game field
grid = ((1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,),
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
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,))


# environment hight and width
envhight = len(grid)
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
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # image of ghost
        self.image = pygame.image.load("pictures/Ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Draw walls
def draw_enviroment(screen):
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 1:
                if j + 1 < envwidth and grid[i][j + 1] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32 + 32, i * 32], 3)
                elif j + 1 == envwidth:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32 + 32, i * 32], 3)
                if grid[i][j - 1] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                elif j == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                if i + 1 < envhight and grid[i + 1][j] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32, i * 32 + 32], 3)
                elif i + 1 == envhight:
                    pygame.draw.line(screen, BLUE, [j * 32 + 32, i * 32 + 32], [j * 32, i * 32 + 32], 3)
                if grid[i - 1][j] == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
                elif i == 0:
                    pygame.draw.line(screen, BLUE, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
