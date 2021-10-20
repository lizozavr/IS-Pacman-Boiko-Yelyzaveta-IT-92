import csv
from datetime import datetime
from player import Player
from objects import *
import random

SCREENWIDTH = 608
SCREENHEIGHT = 544

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (51, 51, 255)
dotsCoordinates = []
secure_random = random.SystemRandom()
global alg_name


class Game(object):
    hasWon = False

    def __init__(self):
        self.startTime = datetime.now()
        self.font = pygame.font.Font(None, 40)
        # Create the player
        self.player = Player(32, 128, "pictures/player.png")
        # Create a group for the blocks
        self.blocks_group = pygame.sprite.Group()
        # Create a group for the food
        self.dots_group = pygame.sprite.Group()
        self.score = 0

        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item == 0:
                    self.blocks_group.add(Block(j * 32 + 4, i * 32 + 4, BLUE, 24, 24))

        # Create the ghosts
        self.enemies = pygame.sprite.Group()
        # self.enemies.add(Ghost(224, 224))
        # self.enemies.add(Ghost(256, 224))
        # self.enemies.add(Ghost(288, 224))
        # self.enemies.add(Ghost(256, 192))
        # Add the food
        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j * 32 + 12, i * 32 + 12, YELLOW, 8, 8))
                    dotsCoordinates.append((i, j))
        self.startPoint = secure_random.choice(dotsCoordinates)
        self.endPoint = secure_random.choice(dotsCoordinates)
        # self.dot1 = secure_random.choice(dotsCoordinates)
        # self.dot2 = secure_random.choice(dotsCoordinates)
        # self.dot3 = secure_random.choice(dotsCoordinates)
        # self.dot4 = secure_random.choice(dotsCoordinates)
        # self.pacmanCoor = secure_random.choice(dotsCoordinates)
        # self.randomDot = secure_random.choice(dotsCoordinates)
        # self.player = Player(self.pacmanCoor[0] * 32, self.pacmanCoor[1] * 32, "pictures/player.png")

        # Add objects to the field
        for i, row in enumerate(grid):
            for j, item in enumerate(row):
                if item == 2:
                    self.player = Player(j * 32, i * 32, "pictures/player.png", True)
                if item == 3:
                    self.enemies.add(Ghost(j * 32, i * 32, 0))
                if item == 4:
                    self.enemies.add(Ghost(j * 32, i * 32, 1))

        self.rand_move_enemies = []
        self.direc_move_enemies = []

        for e in self.enemies:
            if e.type == 0:
                self.rand_move_enemies.append(e)
            else:
                self.direc_move_enemies.append(e)

        self.PointToGoPlayer = algs.minimax(grid, self.player, self.enemies, self.dots_group)

    def input_handler(self):
        if self.game_over:
            return True
        # User did something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if not self.player.computerControlled:
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right()
                    elif event.key == pygame.K_LEFT:
                        self.player.move_left()
                    elif event.key == pygame.K_UP:
                        self.player.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.player.move_down()
                if event.key == pygame.K_ESCAPE:
                    self.gameOver = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

        return False

    def logic(self):
        if not self.game_over:
            self.player.update(self.blocks_group)

            # Finding collides with ghost or food
            dotsHitList = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            blockHitList = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if len(blockHitList) > 0:
                self.player.explosion = True
            if len(self.dots_group) == 0:
                self.player.explosion = True
                self.hasWon = True
            if len(dotsHitList) > 0:
                self.score += 1
            self.game_over = self.player.gameOver

            random_occure_place = random.randint(0, len(dotsCoordinates))

            for ghost in self.rand_move_enemies:
                rp = ghost.prevPoint
                if len(ghost.path) == 0:
                    for i, row in enumerate(grid):
                        for j, item in enumerate(row):
                            if random_occure_place != 0:
                                random_occure_place = random_occure_place - 1
                                rp = (j, i)
                ghost.update(rp)

            for ghost in self.direc_move_enemies:
                rp = ((self.player.rect.bottomright[1] - 16) / 32, (self.player.rect.bottomright[0] - 16) / 32)
                ghost.update(rp)

            if self.player.computerControlled:
                if not self.player.isPlayingByComputer:
                    self.PointToGoPlayer = algs.minimax(grid, self.player, self.enemies, self.dots_group)
                    self.player.isPlayingByComputer = True
                self.player.goTo(self.PointToGoPlayer)
        else:
            data = [alg_name, self.hasWon, datetime.now() - self.startTime, self.score]
            with open('results.csv', 'a', encoding='UTF8') as file:
                writer = csv.writer(file)
                writer.writerow(data)

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
        # bfsPath = findPathBFS(grid, 2, 0, 12, 10)
        # ucsPath = UCS(grid, 2, 0, 12, 10) # каждый раз считается новая масса от того и меняется маргрут
        # for item in ucsPath:
        #     pygame.draw.rect(screen, GREEN, pygame.Rect(item[1] * 32 + 9, item[0] * 32 + 9, 16, 16))
        #     pygame.draw.rect(screen, RED, pygame.Rect(0 * 32 + 9, 2 * 32 + 9, 16, 16))
        #     pygame.draw.rect(screen, RED, pygame.Rect(10 * 32 + 9, 12 * 32 + 9, 16, 16))
        #
        # aStarPath, field = Astar(grid, startPoint[0], startPoint[1], endPoint[0], endPoint[1], heuristic)
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
