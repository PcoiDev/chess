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

    if message:
        print(message)


def get_hints(board: Board, piece) -> list[str]:
    """Returns the squares the piece can go to, or nothing while its possible_moves isn't written yet."""
    try:
        return piece.possible_moves(board)
    except NotImplementedError:
        return []


def play() -> None:
    """Runs a game: each player in turn chooses a piece, then where it goes, until they type quit."""
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

        # Touch-move rule: once a piece is chosen, the player can't choose another one.
        touched = constants.TOUCH_MOVE_MESSAGE.format(type(piece).__name__.lower(), start)
        hints = get_hints(board, piece)
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

        turn = "black" if turn == "white" else "white"
        message = ""


def main() -> None:
    try:
        play()
    except (KeyboardInterrupt, QuitGame):
        print()


if __name__ == "__main__":
    main()
