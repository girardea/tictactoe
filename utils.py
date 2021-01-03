"""Some tic-tac-toe low-level functions like
displaying the board or testing whether game is finished.
"""


def display(s: str) -> None:
    """Nicely display tic-tac-toe state"""
    assert len(s) == 9
    assert all([c in ["-", "x", "o"] for c in s])

    print("\n".join([s[:3], s[3:6], s[6:9]]))


def test_finish(s: str) -> str:
    """Returns None if game isnot finished,
    x if x wins, o if o wins, - if draw.
    """

    for symbol in ["x", "o"]:
        # Horizontal wins
        if all([c == symbol for c in s[:3]]):
            return symbol
        if all([c == symbol for c in s[3:6]]):
            return symbol
        if all([c == symbol for c in s[6:]]):
            return symbol

        # Vertical wins
        if all([c == symbol for c in s[::3]]):
            return symbol
        if all([c == symbol for c in s[1::3]]):
            return symbol
        if all([c == symbol for c in s[2::3]]):
            return symbol

        # Diagonal wins
        if all([c == symbol for c in s[::4]]):
            return symbol
        if all([c == symbol for c in s[2:7:2]]):
            return symbol

    # If no win but no possible move, game is finished with a draw
    if not ("-" in s):
        return "-"

    return


def possible_move(s: str, move: int) -> bool:
    """Returns True if move is possible, False otherwise"""
    return (move >= 0) & (move <= 8) & (s[move] == "-")
