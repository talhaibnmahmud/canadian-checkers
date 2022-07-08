import random
import pygame

from .constants import ColorType, Colors, Coordinate, Dimensions, Direction
from .piece import Piece


class Board:
    def __init__(self):
        self.selected_piece = None
        self.black_left = self.white_left = 30
        self.black_kings = self.white_kings = 0
        self.valid_moves: list[Coordinate] = []
        self.marked_for_remove: dict[Coordinate, list[Coordinate]] = {}

        self.create_board()

    def set_valid_moves(self, valid_moves: list[Coordinate]):
        self.valid_moves = valid_moves

    def draw_squares(self, win: pygame.Surface):
        win.fill(Colors.LIGHT)

        width = Dimensions.SQUARE_SIZE
        height = Dimensions.SQUARE_SIZE
        for row in range(Dimensions.ROW):
            for col in range(row % 2, Dimensions.COL, 2):
                pygame.draw.rect(
                    win,
                    Colors.DARK,
                    (
                        col * Dimensions.SQUARE_SIZE,
                        row * Dimensions.SQUARE_SIZE,
                        width,
                        height
                    )
                )

    def _draw_circle_alpha(
        self,
        win: pygame.Surface,
        center: Coordinate,
        radius: int,
        color: tuple[int, int, int, int]
    ):
        target_rect = pygame.Rect(center, (0, 0)).inflate(
            radius * 2, radius * 2)
        shape_surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surface, color, (radius, radius), radius)
        win.blit(shape_surface, target_rect)

    def draw_valid_moves(self, win: pygame.Surface, valid_moves: list[Coordinate]):
        half_square = Dimensions.SQUARE_SIZE // 2

        for row, col in valid_moves:
            x = col * Dimensions.SQUARE_SIZE + half_square
            y = row * Dimensions.SQUARE_SIZE + half_square
            pygame.draw.circle(win, (0, 200, 0), (x, y), 15)

    def create_board(self):
        self.board: list[list[Piece | None]] = []
        for row in range(Dimensions.ROW):
            self.board.append([])
            for col in range(Dimensions.COL):
                if col % 2 == ((row + 1) % 2):
                    if row < 5:
                        self.board[row].append(Piece(row, col, "white"))
                    elif row > 6:
                        self.board[row].append(Piece(row, col, "black"))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def get_piece(self, row: int, col: int) -> Piece | None:
        return self.board[row][col]

    def get_all_pieces(self, color: ColorType) -> list[Piece]:
        pieces: list[Piece] = []
        for row in range(Dimensions.ROW):
            for col in range(Dimensions.COL):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_random(self):
        row = random.randint(0, Dimensions.ROW - 1)
        col = random.randint(0, Dimensions.COL - 1)

        return row, col

    def get_random_piece(self, color: ColorType):
        while(True):
            row, col = self.get_random()
            piece = self.get_piece(row, col)
            if piece is not None and piece.color == color:
                return self.board[row][col]

    def get_random_move(self, color: ColorType):
        piece = self.get_random_piece(color)
        if piece is None:
            return None
        return self.get_valid_moves(piece)

    def get_valid_moves(self, piece: Piece):
        valid_moves: list[Coordinate] = []
        self.marked_for_remove = {}

        if piece.color == "white":
            direction = Direction.DOWN
            moves = self.adjacent_move(piece, direction)
            valid_moves.extend(moves)

            if piece.king:
                top = self.adjacent_move(piece, -direction)
                valid_moves.extend(top)
        else:
            direction = Direction.UP
            moves = self.adjacent_move(piece, direction)
            valid_moves.extend(moves)

            if piece.king:
                bottom = self.adjacent_move(piece, -direction)
                valid_moves.extend(bottom)

        return valid_moves

    def adjacent_move(self, piece: Piece, direction: int):
        valid: list[Coordinate] = []
        row, col = piece.row, piece.col

        if (direction == Direction.DOWN and row == Dimensions.ROW - 1) or (direction == Direction.UP and row == 0):
            return valid

        x = row + direction
        if col == 0:
            y = col + Direction.RIGHT
            self._find_moves(piece, row, col, x, y, direction, valid)
        elif col == Dimensions.COL - 1:
            y = col + Direction.LEFT
            self._find_moves(piece, row, col, x, y, direction, valid)
        else:
            y = col + Direction.RIGHT
            self._find_moves(piece, row, col, x, y, direction, valid)

            y = col + Direction.LEFT
            self._find_moves(piece, row, col, x, y, direction, valid)

        return valid

    def _check_adjacent(self, row: int, col: int):
        if not -1 < row < Dimensions.ROW or not -1 < col < Dimensions.COL:
            return None

        if self.board[row][col] is None:
            return row, col
        return None

    def _find_moves(
        self,
        piece: Piece,
        row: int,
        col: int,
        x: int,
        y: int,
        direction: int,
        valid: list[Coordinate]
    ):
        if self._check_adjacent(x, y) is not None:
            valid.append((x, y))
        else:
            cell = self.board[x][y]
            if cell is not None and cell.color != piece.color:
                jumps = self.jump(row, col, piece.color, direction)
                valid.extend(jumps)

    def jump(self, row: int, col: int, color: ColorType, direction: int):
        valid: list[Coordinate] = []

        if (direction == Direction.DOWN and row > Dimensions.ROW - 3) or (direction == Direction.UP and row < 2):
            return valid

        if -1 < col < 2:
            y_direction = Direction.RIGHT
            self._find_jumps(row, col, color, direction, y_direction, valid)
        elif Dimensions.COL - 3 < col < Dimensions.COL:
            y_direction = Direction.LEFT
            self._find_jumps(row, col, color, direction, y_direction, valid)
        else:
            y_direction = Direction.RIGHT
            self._find_jumps(row, col, color, direction, y_direction, valid)

            y_direction = Direction.LEFT
            self._find_jumps(row, col, color, direction, y_direction, valid)

        return valid

    def _find_jumps(
        self,
        row: int,
        col: int,
        color: ColorType,
        x_ditection: int,
        y_direction: int,
        valid: list[Coordinate]
    ):
        ax, ay = row + x_ditection, col + y_direction
        jx, jy = row + x_ditection * 2, col + y_direction * 2

        adjacent_cell = self.board[ax][ay]
        if adjacent_cell is not None and adjacent_cell.color != color:
            cell = self.board[jx][jy]
            if cell is None:
                valid.append((jx, jy))

                if (row, col) in self.marked_for_remove:
                    marked = self.marked_for_remove[(row, col)]
                    marked.append((ax, ay))
                    self.marked_for_remove[(jx, jy)] = marked
                else:
                    self.marked_for_remove[(jx, jy)] = [(ax, ay)]

                r_jumps = self.jump(jx, jy, color, x_ditection)

                valid.extend(r_jumps)

    def move_piece(self, piece: Piece, row: int, col: int):
        self.board[piece.row][piece.col] = self.board[row][col]
        self.board[row][col] = piece

        piece.move(row, col)

        if (row, col) in self.marked_for_remove:
            for item in self.marked_for_remove[(row, col)]:
                self.board[item[0]][item[1]] = None

        if (row == 0 or row == Dimensions.ROW - 1) and not piece.king:
            piece.make_king()

            if piece.color == "white":
                self.white_kings += 1 if piece.king else 0
            else:
                self.black_kings += 1 if piece.king else 0

    def remove_piece(self, piece: Piece):
        row, col = piece.row, piece.col
        self.board[row][col] = None

    def check_winner(self):
        if self.black_left == 0:
            return "white"
        elif self.white_left == 0:
            return "black"

        white_pieces = self.get_all_pieces("white")
        black_pieces = self.get_all_pieces("black")

        white_valid_moves: list[Coordinate] = []
        for piece in white_pieces:
            white_valid_moves.extend(self.get_valid_moves(piece))

        black_valid_moves: list[Coordinate] = []
        for piece in black_pieces:
            black_valid_moves.extend(self.get_valid_moves(piece))

        if white_valid_moves == [] and black_valid_moves == []:
            return "draw"
        elif white_valid_moves == []:
            return "black"
        elif black_valid_moves == []:
            return "white"

        return None

    def evaluate(self) -> float:
        return (self.white_left - self.black_left) + (self.white_kings - self.black_kings) * 0.5

    def draw(self, win: pygame.Surface):
        self.draw_squares(win)
        self.draw_valid_moves(win, self.valid_moves)

        for row in range(Dimensions.ROW):
            for col in range(Dimensions.COL):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(win)
