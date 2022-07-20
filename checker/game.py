""" Game Class """
import logging

import pygame

from ai.algorithm import Algorithm
from checker.board import Board
from checker.constants import Colors, Coordinate, Dimensions


def get_row_col_from_mouse_pos(mouse_pos: tuple[float, float]) -> Coordinate:
    """ Get the row and column from the mouse position. """

    x, y = mouse_pos
    row = int(y // Dimensions.SQUARE_SIZE)
    col = int(x // Dimensions.SQUARE_SIZE)

    return row, col


class Game:
    """ Game class """

    def __init__(self, window: pygame.Surface):
        """ Initialize the game """

        self.algorithm = Algorithm()
        self.window = window
        self.ai = Colors.RED
        self.human = Colors.WHITE

        self._reset()

        self.logger = logging.getLogger(__name__)
        self.logger.info('Game is successfully initialized')

    def run(self, FPS: int = 60):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)

            if self.current_player == self.ai:
                self.ai_move(self.board)
                self.logger.info("AI moved.")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = get_row_col_from_mouse_pos(event.pos)

                    if pygame.mouse.get_pressed()[2]:
                        self.select_piece(row, col)
                    if pygame.mouse.get_pressed()[0]:
                        self.move_piece(row, col)

            self.play()

        pygame.quit()

    def play(self):
        """ Play the game """

        self.board.draw(self.window)
        pygame.display.update()

    def switch_player(self):
        """ Switch the current player """

        if self.current_player == self.human:
            self.current_player = self.ai
        else:
            self.current_player = self.human

    def select_piece(self, row: int, col: int):
        """ Select a piece """

        piece = self.board.get_piece(row, col)
        if piece is None:
            return

        if piece.color == self.current_player:
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)

            self.board.set_valid_moves(self.valid_moves)
            self.refresh()
        else:
            self.selected_piece = None
            self.valid_moves = []
            self.board.set_valid_moves(self.valid_moves)
            self.refresh()

    def move_piece(self, row: int, col: int):
        """ Move a piece """

        if self.selected_piece is None:
            return

        if (row, col) in self.valid_moves:
            self.board.move_piece(self.selected_piece, row, col)
            self.selected_piece = None
            self.valid_moves = []
            self.board.set_valid_moves(self.valid_moves)
            self.switch_player()
            self.winner = self.board.check_winner()

            self.refresh()
        else:
            self.selected_piece = None
            self.valid_moves = []
            self.board.set_valid_moves(self.valid_moves)
            self.refresh()

    def ai_move(self, board: Board):
        """ AI move """

        self.logger.info("AI is making a move.")
        value, new_board = self.algorithm.alpha_beta(
            board, 3, True, float("-inf"), float("inf")
        )
        self.logger.info(f"AI value: {value}")

        if new_board is not None:
            self.board = new_board

        self.selected_piece = None
        self.valid_moves = []
        self.board.set_valid_moves(self.valid_moves)

        self.switch_player()
        self.winner = board.check_winner()

        self.refresh()

    def evaluate(self):
        """ Evaluate the game """

        return self.board.evaluate()

    def refresh(self):
        """ Refresh the game window """

        self.board.draw(self.window)
        pygame.display.update()

    def reset(self):
        """ Reset the game """

        self._reset()

    def _reset(self):
        self.board = Board()
        self.current_player = self.human
        self.selected_piece = None
        self.valid_moves = []
        self.winner = None
