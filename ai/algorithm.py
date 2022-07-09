import logging
from copy import deepcopy

import pygame
from checker.board import Board
from checker.constants import ColorType, Coordinate
from checker.piece import Piece


class Algorithm:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initalizing AI algorithm')

    def simulate_move(self,  board: Board, piece: Piece, move: Coordinate):
        board.move_piece(piece, move[0], move[1])
        return board

    def draw_moves(self, board: Board, piece: Piece, window: pygame.Surface):
        valid_moves = board.get_valid_moves(piece)
        board.draw(window)
        pygame.draw.circle(window, (0, 255, 0), (piece.x, piece.y), 50, 5)
        board.draw_valid_moves(window, valid_moves)
        pygame.display.update()
        pygame.time.delay(100)

    def get_all_moves(self, board: Board, color: ColorType):
        moves: list[Board] = []

        for piece in board.get_all_pieces(color):
            # self.logger.info(f"Getting valid moves for {piece}")

            valid_moves = board.get_valid_moves(piece)
            for move in valid_moves:
                # self.logger.info(f"Moving {piece} to {move}")
                # self.draw_moves(board, piece, board.window)
                board_copy = deepcopy(board)
                piece_copy = board_copy.get_piece(piece.row, piece.col)
                if piece_copy is None:
                    continue
                board_copy = self.simulate_move(board_copy, piece_copy, move)
                moves.append(board_copy)

        return moves

    def minimax(self, board: Board, depth: int, max_player: ColorType):
        if depth == 0 or board.check_winner() != None:
            return board.evaluate(), board

        if max_player:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(board, "white"):
                evaluation: float = self.minimax(move, depth-1, False)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move

            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in self.get_all_moves(board, "black"):
                evaluation = self.minimax(move, depth-1, True)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move

            return minEval, best_move

    def alpha_beta(self, board: Board, depth: int, max_player: bool, alpha: float, beta: float):
        self.logger.info(f"Alpha-beta search started. Depth: {depth}")
        if depth == 0 or board.check_winner() != None:
            value = board.evaluate()
            self.logger.info(f"Value: {value}")
            return value, board

        if max_player:
            best_value = float('-inf')
            best_move = None
            for move in self.get_all_moves(board, "white"):
                value: float = self.alpha_beta(
                    move, depth-1, False, alpha, beta
                )[0]
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if best_value == value:
                    best_move = move

                if beta <= alpha:
                    break

            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            for move in self.get_all_moves(board, "black"):
                value = self.alpha_beta(
                    move, depth-1, True, alpha, beta
                )[0]
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if best_value == value:
                    best_move = move

                if beta <= alpha:
                    break

            return best_value, best_move
