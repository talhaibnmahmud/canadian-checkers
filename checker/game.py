""" Game Class """
import logging

import pygame

from ai.algorithm import Algorithm
from checker.board import Board
from checker.constants import Coordinate, Dimensions


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
        self.ai = "white"
        self.human = "black"

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
                    # if self.current_player == self.ai:
                    #     continue

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

    # def get_all_moves(self, board: Board, color: ColorType):
    #     """
    #     Get all possible moves
    #     """
    #     MoveType = tuple[Piece, list[Coordinate]]
    #     moves: list[MoveType] = []

    #     for piece in board.get_all_pieces(color):
    #         new_moves = [(piece, board.get_valid_moves(piece))]

    #         if len(new_moves[0][1]) != 0:
    #             moves.extend(new_moves)

    #     return moves

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
        self.current_player = "black"
        self.selected_piece = None
        self.valid_moves = []
        self.winner = None


# def minimax(game: Game, board: Board, depth: int, max_player: ColorType):
#     if depth == 0 or board.check_winner() != None:
#         return board.evaluate(), board

#     if max_player:
#         maxEval = float('-inf')
#         best_move = None
#         for move in get_all_moves(board, "white", game):
#             evaluation: float = minimax(game, move, depth-1, False)[0]
#             maxEval = max(maxEval, evaluation)
#             if maxEval == evaluation:
#                 best_move = move

#         return maxEval, best_move
#     else:
#         minEval = float('inf')
#         best_move = None
#         for move in get_all_moves(board, "black", game):
#             evaluation = minimax(game, move, depth-1, True)[0]
#             minEval = min(minEval, evaluation)
#             if minEval == evaluation:
#                 best_move = move

#         return minEval, best_move


# def simulate_move(piece: Piece, move: Coordinate, board: Board, game: Game):
#     board.move_piece(piece, move[0], move[1])
#     return board


# def get_all_moves(board: Board, color: ColorType, game: Game):
#     moves: list[Board] = []

#     for piece in board.get_all_pieces(color):
#         # game.logger.info(f"Getting valid moves for {piece}")

#         valid_moves = board.get_valid_moves(piece)
#         for move in valid_moves:
#             # game.logger.info(f"Moving {piece} to {move}")
#             # draw_moves(game, board, piece)
#             board_copy = deepcopy(board)
#             piece_copy = board_copy.get_piece(piece.row, piece.col)
#             if piece_copy is None:
#                 continue
#             board_copy = simulate_move(piece_copy, move, board_copy, game)
#             moves.append(board_copy)

#     return moves


# def draw_moves(game: Game, board: Board, piece: Piece):
#     valid_moves = board.get_valid_moves(piece)
#     board.draw(game.window)
#     pygame.draw.circle(game.window, (0, 255, 0), (piece.x, piece.y), 50, 5)
#     board.draw_valid_moves(game.window, valid_moves)
#     pygame.display.update()
#     pygame.time.delay(10)


# def alpha_beta(game: Game, board: Board, depth: int, max_player: bool, alpha: float, beta: float):
#     game.logger.info(f"Alpha-beta search started. Depth: {depth}")
#     if depth == 0 or board.check_winner() != None:
#         value = board.evaluate()
#         game.logger.info(f"Value: {value}")
#         return value, board

#     if max_player:
#         best_value = float('-inf')
#         best_move = None
#         for move in get_all_moves(board, "white", game):
#             value, _new_board = alpha_beta(             # type: ignore
#                 game, move, depth-1, False, alpha, beta
#             )
#             best_value = max(best_value, value)         # type: ignore
#             alpha = max(alpha, best_value)
#             if best_value == value:
#                 best_move = move

#             if beta <= alpha:
#                 break

#         return best_value, best_move
#     else:
#         best_value = float('inf')
#         best_move = None
#         for move in get_all_moves(board, "black", game):
#             value, _new_board = alpha_beta(             # type: ignore
#                 game, move, depth-1, True, alpha, beta
#             )
#             best_value = min(best_value, value)         # type: ignore
#             beta = min(beta, best_value)
#             if best_value == value:
#                 best_move = move

#             if beta <= alpha:
#                 break

#         return best_value, best_move
