import constants
from board import Board
from render import clear_terminal, render_board_with_hints


class QuitGame(Exception):
    """Raised when the player types the quit command."""


def ask(prompt: str) -> str:
    """Asks the player something and returns the answer in lowercase. Raises QuitGame if they type quit."""
    answer = input(prompt).strip().lower()

    if answer == constants.QUIT_COMMAND:
        raise QuitGame

    return answer


def refresh(board: Board, turn: str, message: str = "", hints: list[str] | None = None) -> None:
    """Clears the terminal, draws the board from the side of the player whose turn it is and shows the message."""
    clear_terminal()
    render_board_with_hints(board, hints, side=turn)
    print(constants.TURN_MESSAGE.format(turn.capitalize()))

    if board.is_in_check(turn):
        print(constants.CHECK_MESSAGE)

    if message:
        print(message)


def other_color(color: str) -> str:
    """Returns the color of the other player."""
    return "black" if color == "white" else "white"


def game_is_over(board: Board, turn: str) -> bool:
    """Shows the result and returns True if the player can't move (checkmate or stalemate), returns False otherwise."""
    if board.has_legal_moves(turn):
        return False

    clear_terminal()
    render_board_with_hints(board, side=turn)

    if board.is_in_check(turn):
        print(constants.CHECKMATE_MESSAGE.format(other_color(turn).capitalize()))
    else:
        print(constants.STALEMATE_MESSAGE)

    return True


def ask_promotion(board: Board, pawn, turn: str) -> None:
    """Asks the player what their pawn becomes, until they give a valid answer."""
    message = ""

    while True:
        refresh(board, turn, message)

        try:
            board.promote(pawn, ask(constants.PROMOTION_PROMPT))
            return
        except ValueError as error:
            message = str(error)


def play() -> None:
    """Runs a game: each player in turn chooses a piece, then where it goes, until the game ends or they type quit."""
    board = Board()
    board.setup()
    turn = "white"
    message = ""

    while True:
        refresh(board, turn, message)
        message = ""

        start = ask(constants.CHOOSE_PIECE_PROMPT)

        try:
            piece = board.get_square(start)
        except ValueError as error:
            message = str(error)
            continue

        if piece == "":
            message = constants.EMPTY_START_ERROR.format(start)
            continue

        if piece.color != turn:
            message = constants.NOT_YOUR_PIECE_ERROR.format(type(piece).__name__.lower(), start, piece.color)
            continue

        hints = board.legal_moves(piece)

        if not hints:
            message = constants.NO_MOVES_ERROR.format(type(piece).__name__.lower(), start)
            continue

        # Touch-move rule: once a piece is chosen, the player can't choose another one.
        touched = constants.TOUCH_MOVE_MESSAGE.format(type(piece).__name__.lower(), start)
        message = touched

        while True:
            refresh(board, turn, message, hints)
            end = ask(constants.CHOOSE_DESTINATION_PROMPT)

            try:
                if board.move_piece(piece, end):
                    break

                message = touched + "\n" + constants.ILLEGAL_MOVE_ERROR.format(start, end)
            except ValueError as error:
                message = touched + "\n" + str(error)

        if board.can_promote(piece):
            ask_promotion(board, piece, turn)

        turn = other_color(turn)
        message = ""

        if game_is_over(board, turn):
            return


def main() -> None:
    try:
        play()
    except (KeyboardInterrupt, QuitGame):
        print()


if __name__ == "__main__":
    main()
