import constants
from board import Board
from render import render_board


def play() -> None:
    """Runs a game: shows the board and asks for moves until the player types quit."""
    board = Board()
    board.setup()

    while True:
        render_board(board)
        answer = input(constants.MOVE_PROMPT).strip().lower()

        if answer == constants.QUIT_COMMAND:
            return

        coords = answer.split()

        if len(coords) != 2:
            print(constants.MOVE_FORMAT_ERROR)
            continue

        start, end = coords

        try:
            piece = board.get_square(start)

            if piece == "":
                print(constants.EMPTY_START_ERROR.format(start))
                continue

            if not board.move_piece(piece, end):
                print(constants.ILLEGAL_MOVE_ERROR.format(start, end))
        except ValueError as error:
            print(error)


def main() -> None:
    try:
        play()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
