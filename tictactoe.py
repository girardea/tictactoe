"""Compares tic-tac-toe strategies by having them compete

Mainly designed for Reinforcement Learning techniques
designed using state value functions or action-state
value functions.

Tic-tac-toe board is characterized by strings like so:

    ---------

or:

    x---o----

or:

    --xo--ox-

where the board is read from the upper-left corner
to the lower-right corner.
"""
import argparse

# Project modules
from utils import display, possible_move, test_finish


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


def play(p1: Strategy, p2: Strategy, verbose: bool = False) -> str:
    """Runs a game of tic-tac-toe

    Player 1 always plays the "x" mark.
    """

    # Initial state
    s = "-" * 9

    i = 0

    while "-" in s:
        i += 1

        if verbose:
            print(f"*** Set {i} ***")
            display(s)

        # Player 1
        s = p1.action(s, my_mark="x")

        # test win
        win = test_finish(s)
        if win:
            if verbose:
                print(win, "wins!")
            return win

        if verbose:
            display(s)

        # Player 2
        s = p2.action(s, my_mark="o")

        # test win
        win = test_finish(s)
        if win:
            if verbose:
                print(win, "wins!")
            return win

    return


def load(player_name: str):
    """Returns a Strategy instance based on the name
    given as an input
    """
    if player_name == "dummy":
        return Dummy()
    elif player_name == "smart_start":
        return SmartStart()
    elif player_name == "me":
        return Human()
    else:
        raise NotImplementedError(f"Could not find {player_name} player.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compares tic-tac-toe strategies by having them compete",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("action", help="Action may be: play, play_all, board")

    parser.add_argument(
        "--player1",
        type=str,
        default="dummy",
        dest="player1",
        help="Name of the first player",
    )

    parser.add_argument(
        "--player2",
        type=str,
        default="dummy",
        dest="player2",
        help="Name of the second player",
    )

    parser.add_argument(
        "-n",
        "--nb_plays",
        type=int,
        default=1000,
        dest="nb",
        help="Number of games to run",
    )

    args = parser.parse_args()

    if args.action == "play":
        # Load player 1
        p1 = load(args.player1)

        # Load player 2
        p2 = load(args.player2)

        # Run (divide plays in half)
        half_nb = args.nb // 2

        results_x = []
        for i in range(args.nb - half_nb):
            results_x.append(play(p1, p2))

        results_o = []
        for i in range(half_nb):
            results_o.append(play(p2, p1))

        # Display results
        def prettify_name(s: str):
            """Displays player names in a nicer way"""
            return s.replace("_", " ").title()

        p1_name, p2_name = prettify_name(args.player1), prettify_name(args.player2)
        print(f"{p1_name} and {p2_name} played {args.nb} games.")
        print(f"{p1_name} won {results_x.count('x') + results_o.count('o')} times.")
        print(f"{p2_name} won {results_x.count('o') + results_o.count('x')} times.")
        print(f"There where {(results_x + results_o).count('-')} draws.")