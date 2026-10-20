from board import Board


def render_board(board: Board) -> None:
    """Prints the board in the console, from row 8 at the top to row 1 at the bottom."""
    raise NotImplementedError


def render_board_with_hints(board: Board, coords: list[str] | None = None) -> None:
    """Prints the board like render_board, and marks the squares in coords (like the possible moves of a piece)."""
    raise NotImplementedError
