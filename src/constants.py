

PIECES = {
    "KING": ("♔", "♚"),
    "QUEEN": ("♕", "♛"),
    "ROOK": ("♖", "♜"),
    "BISHOP": ("♗", "♝"),
    "KNIGHT": ("♘", "♞"),
    "PAWN": ("♙", "♟"),
}

EMPTY_BOARD = {chr(ord("a") + i): {(i + 1): "" for i in range(8)} for i in range(8)}
