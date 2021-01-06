"""All tic-tac-toe strategies are placed here.
"""
# Low-level modules
from typing import Dict

# Project modules
from utils import display, possible_move


class Strategy(object):
    """All playing strategies should derive from this"""

    def action(self, s: str, my_mark: str = "x") -> str:
        """Returns my best action on the board situation
        defined by s
        """
        raise NotImplementedError


class Dummy(Strategy):
    """Plays at random"""

    def action(self, s: str, my_mark: str = "x") -> str:
        """Plays one random move and returns new state"""
        import numpy as np
        import re

        # There should be at least one possible move
        assert "-" in s

        # Get all possible moves
        possible_moves = [m.start() for m in re.finditer("-", s)]

        # Choose one position at random
        move = np.random.choice(possible_moves)

        return s[:move] + my_mark + s[move + 1 :]


class SmartStart(Strategy):
    """Plays at random but has a smarter first move"""

    def action(self, s: str, my_mark: str = "x") -> str:
        """Plays one random move and returns new state,
        except for very first move where it plays at center mark.
        """
        import numpy as np
        import re

        # There should be at least one possible move
        assert "-" in s

        # Play center if very first move
        if not any([mark == my_mark for mark in s]) and s[4] == "-":
            move = 4
        else:
            # Get all possible moves
            possible_moves = [m.start() for m in re.finditer("-", s)]

            # Choose one position at random
            move = np.random.choice(possible_moves)

        return s[:move] + my_mark + s[move + 1 :]


class Human(Strategy):
    """Asks you to play!"""

    def action(self, s: str, my_mark: str = "x") -> str:
        """Asks you to play."""
        # display board (for human to decide)
        display(s)

        # Ask for action and check its feasibility
        move = -1
        while not possible_move(s, move):
            move = input(
                f'Où placer "{my_mark}" ?'
                " (de 1 en haut à gauche à 9 en bas à droite) :"
            )
            move = int(move) - 1

        return s[:move] + my_mark + s[move + 1 :]


class QStrategy(Strategy):
    """Implements a state-action value based strategy"""

    def __init__(self, Q: Dict):
        """Needs the Q-function to work (see README.md)"""
        self.Q = Q

    def action(self, s: str, my_mark: str = "x") -> str:
        """Finds best action."""
        if my_mark == "o":
            # switch "x" and "o"
            s = s.replace("x", "y").replace("o", "x").replace("y", "o")

        # find best action (be aware it could be unfeasible)
        try:
            d = self.Q["data"][s]
        except KeyError:
            # if no info for this state, use random
            return Dummy().action(s, my_mark)

        no_feasible_move = True
        move = -1
        for move in sorted(d, key=d.get, reverse=True):
            # convert from str to int (and to base 0 instead of base 1)
            move = int(move) - 1

            # check feasibility
            if possible_move(s, move):
                no_feasible_move = False
                break

        assert not no_feasible_move, f"Could not find a feasible move for board {s}"

        return s[:move] + my_mark + s[move + 1 :]
