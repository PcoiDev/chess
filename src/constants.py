# (white, black): the filled symbols are for white because they look white on a dark terminal.
PIECES = {
    "KING": ("♚", "♔"),
    "QUEEN": ("♛", "♕"),
    "ROOK": ("♜", "♖"),
    "BISHOP": ("♝", "♗"),
    "KNIGHT": ("♞", "♘"),
    "PAWN": ("♟", "♙"),
}

EMPTY_BOARD = {chr(ord("a") + i): {(i + 1): "" for i in range(8)} for i in range(8)}

EMPTY_SQUARE = " . "
HINT_SQUARE = " • "
CAPTURE_HINT_SQUARE = "[{}]"

CLEAR_SCREEN = "\033[2J\033[3J\033[H"

CHOOSE_PIECE_PROMPT = "Choose a piece to play: "
CHOOSE_DESTINATION_PROMPT = "Where does it go? "
QUIT_COMMAND = "quit"

TURN_MESSAGE = "\n{} to play"
TOUCH_MOVE_MESSAGE ="Piece touched, piece played! You touched your {} on {!r}, no going back now."

INVALID_COORD_ERROR = "{!r} is not a valid coordinate"
INVALID_COLOR_ERROR = "{!r} is not a valid color"
EMPTY_START_ERROR = "There is no piece on {!r}"
NOT_YOUR_PIECE_ERROR = "Hands off! The {} on {!r} belongs to {}"
ILLEGAL_MOVE_ERROR = "The piece on {!r} can't go to {!r}"
