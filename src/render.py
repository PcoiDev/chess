import constants
import coord_utils
from board import Board
from pieces import COLORS

COLUMNS = [chr(ord("a") + i) for i in range(8)]


def render_board(board: Board, side: str = "white") -> None:
    """Prints the board in the console, seen from the side of the player (white or black)."""
    render_board_with_hints(board, side=side)


def render_board_with_hints(board: Board, coords: list[str] | None = None, side: str = "white") -> None:
    """Prints the board like render_board, and marks the squares in coords (like the possible moves of a piece)."""
    if side not in COLORS:
        raise ValueError(constants.INVALID_COLOR_ERROR.format(side))

    if coords is None:
        coords = []

    # White sees row 8 at the top and column a on the left, black sees the opposite.
    if side == "white":
        rows = range(8, 0, -1)
        columns = COLUMNS
    else:
        rows = range(1, 9)
        columns = COLUMNS[::-1]

    letters = "  " + "".join(f" {column} " for column in columns)

    print(letters)

    for row in rows:
        line = f"{row} "

        for column in columns:
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
