import pygame
from game import Game

SCREEN_WIDTH = 544
SCREEN_HEIGHT = 544


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman")
    # done game variable
    done = False
    # fps variable
    clock = pygame.time.Clock()
    # Create a game object
    game = Game()
    game.__init__()
    game.game_over = False
    # game
    while not done:
        # input handler
        done = game.input_handler()
        game.logic()
        # draw frame
        game.display_frame(screen)
        # 30 frames per second
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
