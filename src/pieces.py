import constants
import coord_utils

COLORS = ("white", "black")


class Piece:
    """A class to make subclasses to make pieces."""

    NAME = None

    def __init__(self, color: str, position: str):
        if color not in COLORS:
            raise ValueError(constants.INVALID_COLOR_ERROR.format(color))

        if not coord_utils.is_coord(position):
            raise ValueError(constants.INVALID_COORD_ERROR.format(position))

        self.color = color
        self.position = position
        self.has_moved = False

    @property
    def symbol(self) -> str:
        """Returns the unicode symbol of the piece, depending on its color."""
        return constants.PIECES[self.NAME][COLORS.index(self.color)]

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"{type(self).__name__}({self.color!r}, {self.position!r})"

    def move(self, new_position: str):
        """Moves the piece without checking if the move is legal."""
        if not coord_utils.is_coord(new_position):
            raise ValueError(constants.INVALID_COORD_ERROR.format(new_position))

        self.position = new_position
        self.has_moved = True

    def is_enemy(self, other) -> bool:
        """Returns True if other is a piece of the other color, False otherwise (empty square or ally)."""
        return isinstance(other, Piece) and other.color != self.color

    def possible_moves(self, board) -> list[str]:
        """Returns the squares the piece can go to. Each subclass must write its own."""
        raise NotImplementedError


class King(Piece):
    NAME = "KING"


class Queen(Piece):
    NAME = "QUEEN"


class Rook(Piece):
    NAME = "ROOK"


class Bishop(Piece):
    NAME = "BISHOP"


class Knight(Piece):
    NAME = "KNIGHT"


class Pawn(Piece):
    NAME = "PAWN"

