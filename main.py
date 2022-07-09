"""Main entry point for the application."""
import logging

import pygame

import logger.custom_logger as cl
from checker.constants import Dimensions
from checker.game import Game


FPS = 60
SIZE = (Dimensions.WIDTH, Dimensions.HEIGHT)
WIN: pygame.Surface = pygame.display.set_mode(size=SIZE)  # type: ignore
pygame.display.set_caption("Canadian Checkers")


def main():
    """ Main Function"""

    cl.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Game started.")

    game = Game(WIN)
    game.run(FPS)

    logger.info("Game closed.")


if __name__ == '__main__':
    main()
