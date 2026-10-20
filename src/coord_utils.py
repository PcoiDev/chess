import constants


def is_coord(coord: str) -> bool:
    """Returns True if coord is a valid square on the board (like "e2"), False otherwise."""
    if len(coord) != 2:
        return False

    letter = coord[0]
    digit = coord[1]

    return (ord("a") <= ord(letter) <= ord("h")) and (ord("1") <= ord(digit) <= ord("8"))


def coord_to_tuple(coord: str) -> tuple[str, int]:
    """Splits a square like "e2" into its column and row: ("e", 2)."""
    coord = coord.lower()

    if not is_coord(coord):
        raise ValueError(constants.INVALID_COORD_ERROR.format(coord))

    return coord[0], int(coord[1])

def tuple_to_coord(square: tuple[str, int]) -> str:
    """Joins a column and row like ("e", 2) into a square: "e2"."""
    coord = square[0] + str(square[1])

    if not is_coord(coord):
        raise ValueError(constants.INVALID_COORD_ERROR.format(coord))

    return coord