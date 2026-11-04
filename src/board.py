import copy

import constants
import coord_utils
from pieces import Bishop, King, Knight, Pawn, Queen, Rook

BACK_ROW = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)
PROMOTIONS = {"queen": Queen, "rook": Rook, "bishop": Bishop, "knight": Knight}


class Board:
    """Recreates the chess board onto the console"""

    def __init__(self):
        self._board = copy.deepcopy(constants.EMPTY_BOARD)
        self.en_passant_target = None

    def setup(self) -> None:
        """Empties the board and places the 32 pieces at their starting position."""
        self._board = copy.deepcopy(constants.EMPTY_BOARD)
        self.en_passant_target = None

        for color, back_row, pawn_row in (("white", 1, 2), ("black", 8, 7)):
            for i, piece_class in enumerate(BACK_ROW):
                column = chr(ord("a") + i)

                self.add_piece(piece_class(color, coord_utils.tuple_to_coord((column, back_row))))
                self.add_piece(Pawn(color, coord_utils.tuple_to_coord((column, pawn_row))))

    def get_square(self, coord: str):
        """Returns what is on the square coord: a piece, or "" if the square is empty."""
        column, row = coord_utils.coord_to_tuple(coord)
        return self._board[column][row]

    def is_attacked(self, coord: str, by_color: str) -> bool:
        """Returns True if a piece of by_color attacks the square coord, False otherwise."""
        for column in self._board.values():
            for square in column.values():
                if square != "" and square.color == by_color and coord in square.attacked_squares(self):
                    return True

        return False

    def add_piece(self, piece) -> bool:
        # TODO: docstring
        column, row = coord_utils.coord_to_tuple(piece.position)

        if self._board[column][row] != "":
            return False
        
        self._board[column][row] = piece
        return True

    def remove_piece(self, piece) -> None:
        # TODO: docstring
        column, row = coord_utils.coord_to_tuple(piece.position)
        self._board[column][row] = ""

    def move_piece(self, piece, new_coord: str) -> bool:
        """Plays the move if it's one of the piece's possible moves, castling and en passant included. Returns False otherwise."""
        if not coord_utils.is_coord(new_coord):
            raise ValueError(constants.INVALID_COORD_ERROR.format(new_coord))

        if new_coord not in piece.possible_moves(self):
            return False

        column, row = coord_utils.coord_to_tuple(piece.position)
        new_column, new_row = coord_utils.coord_to_tuple(new_coord)

        # The pawn taken en passant is next to the start square, not on the end square.
        if isinstance(piece, Pawn) and new_coord == self.en_passant_target:
            self._board[new_column][row] = ""

        if isinstance(piece, King) and abs(ord(new_column) - ord(column)) == 2:
            self._move_castling_rook(new_column, row)

        self.en_passant_target = None

        if isinstance(piece, Pawn) and abs(new_row - row) == 2:
            self.en_passant_target = coord_utils.tuple_to_coord((column, (row + new_row) // 2))

        piece.move(new_coord)

        # Writing on the new square also removes the piece that was taken, if there is one.
        self._board[column][row] = ""
        self._board[new_column][new_row] = piece

        return True

    def _move_castling_rook(self, king_column: str, row: int) -> None:
        """Moves the rook to the other side of the king, who is castling to king_column."""
        rook_column, new_rook_column = ("h", "f") if king_column == "g" else ("a", "d")

        rook = self._board[rook_column][row]
        rook.move(coord_utils.tuple_to_coord((new_rook_column, row)))

        self._board[rook_column][row] = ""
        self._board[new_rook_column][row] = rook

    def can_promote(self, piece) -> bool:
        """Returns True if the piece is a pawn that reached the last row, False otherwise."""
        _, row = coord_utils.coord_to_tuple(piece.position)

        return isinstance(piece, Pawn) and row in (1, 8)

    def promote(self, pawn, choice: str) -> None:
        """Replaces the pawn by the piece named by choice (like "queen")."""
        if choice not in PROMOTIONS:
            raise ValueError(constants.INVALID_PROMOTION_ERROR.format(choice))

        column, row = coord_utils.coord_to_tuple(pawn.position)

        promoted = PROMOTIONS[choice](pawn.color, pawn.position)
        promoted.has_moved = True

        self._board[column][row] = promoted
