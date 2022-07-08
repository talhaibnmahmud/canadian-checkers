from dataclasses import dataclass, field
from typing import ClassVar

from pygame import draw, image, surface, transform

from .constants import ColorType, Dimensions


@dataclass
class Piece:
    CROWN: ClassVar = transform.scale(
        image.load('assets/images/crown.png'),
        (Dimensions.SQUARE_SIZE // 3, Dimensions.SQUARE_SIZE // 3)
    )

    row: int
    col: int
    color: ColorType

    x: int = field(default=0, init=False)
    y: int = field(default=0, init=False)
    king: bool = field(default=False, init=False)

    def __post_init__(self):
        self.calculate_positions()

    def __repr__(self) -> str:
        return f"Piece({self.row}, {self.col}, {self.color}, {self.king})"

    def __str__(self) -> str:
        return f"{str(self.color)} -> ({str(self.row)}, {str(self.col)}) -> {'King' if self.king else 'Man'}"

    def make_king(self):
        self.king = True

    def calculate_positions(self):
        half_square = Dimensions.SQUARE_SIZE // 2
        self.x = self.col * Dimensions.SQUARE_SIZE + half_square
        self.y = self.row * Dimensions.SQUARE_SIZE + half_square

    def move(self, row: int, col: int):
        self.row = row
        self.col = col
        self.calculate_positions()

    def draw(self, win: surface.Surface):
        draw.circle(win, self.color, (self.x, self.y), 20)

        if self.king:
            win.blit(
                Piece.CROWN,
                (self.x - Piece.CROWN.get_width() // 2,
                 self.y - Piece.CROWN.get_height() // 2)
            )
