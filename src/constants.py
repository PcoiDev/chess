PIECES = {
    "KING": ("♔", "♚"),
    "QUEEN": ("♕", "♛"),
    "ROOK": ("♖", "♜"),
    "BISHOP": ("♗", "♝"),
    "KNIGHT": ("♘", "♞"),
    "PAWN": ("♙", "♟"),
}

EMPTY_BOARD = {chr(ord("a") + i): {(i + 1): "" for i in range(8)} for i in range(8)}

EMPTY_SQUARE = " . "
HINT_SQUARE = " • "
CAPTURE_HINT_SQUARE = "[{}]"

INVALID_COORD_ERROR = "{!r} is not a valid coordinate"
INVALID_COLOR_ERROR = "{!r} is not a valid color"
