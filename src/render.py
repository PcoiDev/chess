import constants
import coord_utils
from board import Board

COLUMNS = [chr(ord("a") + i) for i in range(8)]


def render_board(board: Board) -> None:
    """Prints the board in the console, from row 8 at the top to row 1 at the bottom."""
    render_board_with_hints(board)


def render_board_with_hints(board: Board, coords: list[str] | None = None) -> None:
    """Prints the board like render_board, and marks the squares in coords (like the possible moves of a piece)."""
    if coords is None:
        coords = []

    letters = "  " + "".join(f" {column} " for column in COLUMNS)

    print(letters)

    for row in range(8, 0, -1):
        line = f"{row} "

        for column in COLUMNS:
            coord = coord_utils.tuple_to_coord((column, row))
            line += render_square(board.get_square(coord), coord in coords)

        print(line + f" {row}")

    print(letters)


def render_square(square, is_hint: bool) -> str:
    """Returns the text of one square: the piece, an empty square, or a hint if is_hint is True."""
    if square == "":
        return constants.HINT_SQUARE if is_hint else constants.EMPTY_SQUARE

    if is_hint:
        return constants.CAPTURE_HINT_SQUARE.format(square)

    return f" {square} "
