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


def shift(coord: str, dx: int, dy: int) -> str | None:
    """Returns the square dx columns and dy rows away from coord ("e2", 1, 1 gives "f3"), or None if it's off the board."""
    letter, row = coord_to_tuple(coord)
    new_coord = chr(ord(letter) + dx) + str(row + dy)

    return new_coord if is_coord(new_coord) else None
