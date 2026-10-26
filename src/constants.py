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

MOVE_PROMPT = "> "
QUIT_COMMAND = "quit"

INVALID_COORD_ERROR = "{!r} is not a valid coordinate"
INVALID_COLOR_ERROR = "{!r} is not a valid color"
MOVE_FORMAT_ERROR = 'Type a move like "e2 e4", or "quit" to leave'
EMPTY_START_ERROR = "There is no piece on {!r}"
ILLEGAL_MOVE_ERROR = "The piece on {!r} can't go to {!r}"
