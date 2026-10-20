import copy

import constants
import coord_utils
from pieces import Bishop, King, Knight, Pawn, Queen, Rook

BACK_ROW = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)


class Board:
    """Recreates the chess board onto the console"""

    def __init__(self):
        self._board = copy.deepcopy(constants.EMPTY_BOARD)

    def setup(self) -> None:
        """Empties the board and places the 32 pieces at their starting position."""
        self._board = copy.deepcopy(constants.EMPTY_BOARD)

        for color, back_row, pawn_row in (("white", 1, 2), ("black", 8, 7)):
            for i, piece_class in enumerate(BACK_ROW):
                column = chr(ord("a") + i)

                self.add_piece(piece_class(color, coord_utils.tuple_to_coord((column, back_row))))
                self.add_piece(Pawn(color, coord_utils.tuple_to_coord((column, pawn_row))))

    def get_square(self, coord: str):
        """Returns what is on the square coord: a piece, or "" if the square is empty."""
        column, row = coord_utils.coord_to_tuple(coord)
        return self._board[column][row]

    def add_piece(self, piece) -> bool:
        # TODO: docstring
        column, row = coord_utils.coord_to_tuple(piece.position)

        if self._board[column][row] != "":
            return False
        
        self._board[column][row] = piece
        return True

    def remove_piece(self, piece) -> None:
        # TODO: look if we need a piece.destroy() method and if we need to remove_piece(piece) when calling it.
        # TODO: docstring
        column, row = coord_utils.coord_to_tuple(piece.position)
        self._board[column][row] = ""

    def move_piece(self, piece, new_coord: str) -> bool:
        # TODO: docstring
        if not coord_utils.is_coord(new_coord):
            raise ValueError(constants.INVALID_COORD_ERROR.format(new_coord))
        
        column, row = coord_utils.coord_to_tuple(piece.position)
        
        new_column, new_row = coord_utils.coord_to_tuple(new_coord)
        new_coord_piece = self._board[new_column][new_row]
        
        if new_coord_piece == "" or piece.is_enemy(new_coord_piece):
            piece.move(new_coord) # TODO: what to do with new_coord_piece cuz it will be eaten? destroy the piece?

            self._board[column][row] = ""
            self._board[new_column][new_row] = piece

            return True

        return False