from copy import deepcopy

from .board import Board
from .constants import ColorType, Coordinate
from .game import Game


def minmax(game: Game, move: Coordinate, depth: int, max_player: bool):
    """
    Minmax algorithm with alpha-beta pruning
    """
    if depth == 0 or game.winner is not None:
        return game.evaluate()

    if max_player:
        best_score = float("-inf")
        for move in get_all_moves(game, game.board, game.ai):
            score = minmax(game, move, depth - 1, False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for move in get_all_moves(game, game.board, game.human):
            score = minmax(game, move, depth - 1, True)
            best_score = min(best_score, score)
        return best_score


def minimax(game: Game, board: Board, depth: int, max_player: bool):
    """
    Minimax algorithm with alpha-beta pruning
    """
    if depth == 0 or game.winner is not None:
        return game.score()

    if max_player:
        best_score = float("-inf")
        for move in board.get_valid_moves():
            board_copy = deepcopy(board)
            board_copy.move_piece(move[0], move[1])
            score = minimax(game, board_copy, depth - 1, False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for move in board.get_valid_moves():
            board_copy = deepcopy(board)
            board_copy.move_piece(move[0], move[1])
            score = minimax(game, board_copy, depth - 1, True)
            best_score = min(best_score, score)
        return best_score



