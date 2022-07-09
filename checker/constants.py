from enum import IntEnum
from typing import ClassVar

from pygame import color


Coordinate = tuple[int, int]
ColorType = color.Color \
    | int \
    | str \
    | tuple[int, int, int] \
    | list[int]


class Direction(IntEnum):
    UP = -1
    DOWN = 1
    LEFT = -1
    RIGHT = 1


class Colors:
    # RED: ClassVar = color.Color(255, 000, 000)
    RED: ClassVar = color.Color('#F21905')
    BLUE: ClassVar = color.Color(000, 000, 255)
    # DARK: ClassVar = color.Color(218, 160, 109)
    DARK: ClassVar = color.Color('#608C1F')
    BLACK: ClassVar = color.Color(000, 000, 000)
    # BROWN: ClassVar = color.Color(128, 128, 128)
    BROWN: ClassVar = color.Color('#730202')
    GREEN: ClassVar = color.Color(000, 255, 000)
    # LIGHT: ClassVar = color.Color(128, 128, 000)
    LIGHT: ClassVar = color.Color('#F2E3B6')
    # WHITE: ClassVar = color.Color(255, 255, 255)
    WHITE: ClassVar = color.Color('#F2F2F2')
    ORANGE: ClassVar = color.Color(255, 128, 000)
    PURPLE: ClassVar = color.Color(128, 000, 128)
    YELLOW: ClassVar = color.Color(255, 255, 000)


class Dimensions:
    ROW: ClassVar = 12      # 12
    COL: ClassVar = 12      # 12
    WIDTH: ClassVar = 720
    HEIGHT: ClassVar = 720
    SQUARE_SIZE: ClassVar = WIDTH // ROW
