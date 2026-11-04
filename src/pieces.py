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

    @property
    def enemy_color(self) -> str:
        """Returns the color of the other player."""
        return COLORS[1 - COLORS.index(self.color)]

    def possible_moves(self, board) -> list[str]:
        """Returns the squares the piece can go to. Each subclass must write its own."""
        raise NotImplementedError

    def attacked_squares(self, board) -> list[str]:
        """Returns the squares the piece attacks. They are its possible moves, except for the pawn and the king."""
        return self.possible_moves(board)

    def _slide(self, board, directions: tuple) -> list[str]:
        """Returns the squares reached by going straight in each direction, until a piece or the edge of the board."""
        moves = []

        for dx, dy in directions:
            coord = coord_utils.shift(self.position, dx, dy)

            while coord is not None:
                square = board.get_square(coord)

                if square != "":
                    if self.is_enemy(square):
                        moves.append(coord)

                    break

                moves.append(coord)
                coord = coord_utils.shift(coord, dx, dy)

        return moves

    def _jump(self, board, offsets: tuple) -> list[str]:
        """Returns the squares at the given offsets that are empty or hold an enemy."""
        moves = []

        for dx, dy in offsets:
            coord = coord_utils.shift(self.position, dx, dy)

            if coord is None:
                continue

            square = board.get_square(coord)

            if square == "" or self.is_enemy(square):
                moves.append(coord)

        return moves


class King(Piece):
    NAME = "KING"

    def possible_moves(self, board) -> list[str]:
        return self.attacked_squares(board) + self._castling_moves(board)

    def attacked_squares(self, board) -> list[str]:
        return self._jump(board, constants.STRAIGHT_DIRECTIONS + constants.DIAGONAL_DIRECTIONS)

    def _castling_moves(self, board) -> list[str]:
        """Returns the squares the king can castle to: g on the king side, c on the queen side."""
        if self.has_moved:
            return []

        column, row = coord_utils.coord_to_tuple(self.position)
        moves = []

        for rook_column, empty_columns, king_path in (("h", "fg", "fg"), ("a", "bcd", "dc")):
            rook = board.get_square(rook_column + str(row))

            if not isinstance(rook, Rook) or rook.color != self.color or rook.has_moved:
                continue

            if any(board.get_square(letter + str(row)) != "" for letter in empty_columns):
                continue

            # The king can't castle out of, through or into an attacked square.
            if any(board.is_attacked(letter + str(row), self.enemy_color) for letter in column + king_path):
                continue

            moves.append(king_path[-1] + str(row))

        return moves


class Queen(Piece):
    NAME = "QUEEN"

    def possible_moves(self, board) -> list[str]:
        return self._slide(board, constants.STRAIGHT_DIRECTIONS + constants.DIAGONAL_DIRECTIONS)


class Rook(Piece):
    NAME = "ROOK"

    def possible_moves(self, board) -> list[str]:
        return self._slide(board, constants.STRAIGHT_DIRECTIONS)


class Bishop(Piece):
    NAME = "BISHOP"

    def possible_moves(self, board) -> list[str]:
        return self._slide(board, constants.DIAGONAL_DIRECTIONS)


class Knight(Piece):
    NAME = "KNIGHT"

    def possible_moves(self, board) -> list[str]:
        return self._jump(board, constants.KNIGHT_JUMPS)


class Pawn(Piece):
    NAME = "PAWN"

    @property
    def direction(self) -> int:
        """Returns the way the pawn walks: up the board for white, down for black."""
        return 1 if self.color == "white" else -1

    def possible_moves(self, board) -> list[str]:
        moves = []

        one_step = coord_utils.shift(self.position, 0, self.direction)

        if one_step is not None and board.get_square(one_step) == "":
            moves.append(one_step)

            two_steps = coord_utils.shift(self.position, 0, 2 * self.direction)

            if not self.has_moved and two_steps is not None and board.get_square(two_steps) == "":
                moves.append(two_steps)

        for coord in self.attacked_squares(board):
            if self.is_enemy(board.get_square(coord)) or coord == board.en_passant_target:
                moves.append(coord)

        return moves

    def attacked_squares(self, board) -> list[str]:
        squares = (coord_utils.shift(self.position, dx, self.direction) for dx in (-1, 1))

        return [coord for coord in squares if coord is not None]

