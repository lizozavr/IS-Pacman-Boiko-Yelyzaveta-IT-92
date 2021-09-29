from algs import Astar
from player import Player
from objects import *
from algs import *
import random

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 544

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (51, 51, 255)
dotsCoordinates = []
secure_random = random.SystemRandom()



class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        # Create the player
        self.player = Player(32, 128, "pictures/player.png")
        # Create a group for the blocks
        self.blocks_group = pygame.sprite.Group()
        # Create a group for the food
        self.dots_group = pygame.sprite.Group()

        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item == 0:
                    self.blocks_group.add(Block(j * 32 + 4, i * 32 + 4, BLUE, 24, 24))

        # Create the ghosts
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Ghost(224, 224))
        self.enemies.add(Ghost(256, 224))
        self.enemies.add(Ghost(288, 224))
        self.enemies.add(Ghost(256, 192))
        # Add the food
        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j * 32 + 12, i * 32 + 12, YELLOW, 8, 8))
                    dotsCoordinates.append((i, j))
        self.startPoint = secure_random.choice(dotsCoordinates)
        self.endPoint = secure_random.choice(dotsCoordinates)
        self.dot1 = secure_random.choice(dotsCoordinates)
        self.dot2 = secure_random.choice(dotsCoordinates)
        self.dot3 = secure_random.choice(dotsCoordinates)
        self.dot4 = secure_random.choice(dotsCoordinates)
        self.pacmanCoor = secure_random.choice(dotsCoordinates)
        self.randomDot = secure_random.choice(dotsCoordinates)
        self.player = Player(self.pacmanCoor[0]*32, self.pacmanCoor[1]*32, "pictures/player.png")

    def input_handler(self):
        if self.game_over == True:
            return True
        # User did something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return False

    def logic(self):
        if not self.game_over:
            self.player.update(self.blocks_group)
            # detecting collide with ghost or food
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if len(block_hit_list) > 0:
                self.player.explosion = True
            if len(self.dots_group) == 0:
                self.player.explosion = True
            self.game_over = self.player.game_over

    def display_frame(self, screen):
        # clear screen from previous frame
        screen.fill(BLACK)
        # draw walls
        draw_enviroment(screen)
        # draw yellow dots
        self.dots_group.draw(screen)
        # draw ghosts
        self.enemies.draw(screen)
        # draw player on field
        screen.blit(self.player.image, self.player.rect)
        # call algorithms

        startPoint = self.startPoint
        endPoint = self.endPoint

        # dfsPath = findPathDFS(grid, 2, 0, 12, 10)
        # for p in dfsPath:
        #     pygame.draw.rect(screen, GREEN, pygame.Rect(p[1] * 32 + 9, p[0] * 32 + 9, 16, 16))
        # pygame.draw.rect(screen, RED, pygame.Rect(0 * 32 + 9, 2 * 32 + 9, 16, 16))
        # pygame.draw.rect(screen, RED, pygame.Rect(10 * 32 + 9, 12 * 32 + 9, 16, 16))
        #
        # bfsPath = findPathBFS(grid, 2, 0, 12, 10)
        # for p in bfsPath:
        #     pygame.draw.rect(screen, GREEN, pygame.Rect(p[1] * 32 + 9, p[0] * 32 + 9, 16, 16))
        # pygame.draw.rect(screen, RED, pygame.Rect(0 * 32 + 9, 2 * 32 + 9, 16, 16))
        # pygame.draw.rect(screen, RED, pygame.Rect(10 * 32 + 9, 12 * 32 + 9, 16, 16))
        #
        # ucsPath = UCS(grid, 2, 0, 12, 10) # каждый раз считается новая масса от того и меняется маргрут
        # for item in ucsPath:
        #     pygame.draw.rect(screen, GREEN, pygame.Rect(item[1] * 32 + 9, item[0] * 32 + 9, 16, 16))
        #     pygame.draw.rect(screen, RED, pygame.Rect(0 * 32 + 9, 2 * 32 + 9, 16, 16))
        #     pygame.draw.rect(screen, RED, pygame.Rect(10 * 32 + 9, 12 * 32 + 9, 16, 16))
        #
        aStarPath, field = Astar(grid, startPoint[0], startPoint[1], endPoint[0], endPoint[1], heuristic)
        # aStarPath, field = Astar(grid, startPoint[0], startPoint[1], endPoint[0], endPoint[1], euclidean)
        # aStarPath, field = Astar(grid, startPoint[0], startPoint[1], endPoint[0], endPoint[1], euclideanSquared)
        for item in aStarPath:
            pygame.draw.rect(screen, GREEN, pygame.Rect(item[1] * 32 + 9, item[0] * 32 + 9, 16, 16))
        pygame.draw.rect(screen, RED, pygame.Rect(startPoint[1] * 32 + 9, startPoint[0] * 32 + 9, 16, 16))
        pygame.draw.rect(screen, RED, pygame.Rect(endPoint[1] * 32 + 9, endPoint[0] * 32 + 9, 16, 16))

        # 4 dots
        # dotsListToFindPath = []
        # dotsListToFindPath.append(self.pacmanCoor)
        # dotsListToFindPath.append(self.dot1)
        # dotsListToFindPath.append(self.dot2)
        # dotsListToFindPath.append(self.dot3)
        # dotsListToFindPath.append(self.dot4)
        # result = buildPathThrowDots(dotsListToFindPath)
        # for item in result:
        #     pygame.draw.rect(screen, GREEN, pygame.Rect(item[1] * 32 + 9, item[0] * 32 + 9, 16, 16))
        # for item in dotsListToFindPath:
        #     pygame.draw.rect(screen, RED, pygame.Rect(item[1] * 32 + 9, item[0] * 32 + 9, 16, 16))

        # All dots
        # dotsListToFindPathThrowAllDots = []
        # dotsListToFindPathThrowAllDots.append(self.pacmanCoor)
        # dotsListToFindPathThrowAllDots.append(self.randomDot)
        # result = buildPathThrowDots(dotsCoordinates)
        # for item in result:
        #     pygame.draw.rect(screen, GREEN, pygame.Rect(item[1] * 32 + 9, item[0] * 32 + 9, 16, 16))

        # update screen
        pygame.display.flip()
