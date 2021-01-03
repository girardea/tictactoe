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

import tqdm

# Project modules
from players import Strategy, Dummy, SmartStart, Human
from utils import display, test_finish


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

    elif args.action == "board":
        print("Playing all possible player combinations...")
        from itertools import product

        import pandas as pd

        # Compute list of players
        ll_players = ["dummy", "smart_start"]
        nb_players = len(ll_players)

        # Divide plays in half
        half_nb = args.nb // 2

        # Retain scores
        df_scores = pd.DataFrame(index=ll_players, columns=ll_players, data=0)

        # Run every combination of players
        # Display progress bar
        with tqdm.tqdm(total=nb_players ** 2 - nb_players) as pbar:
            for p1_name, p2_name in product(ll_players, ll_players):
                # Do not play against one-self
                if p1_name == p2_name:
                    continue

                # Display
                pbar.update(1)

                # Load players
                p1, p2 = load(p1_name), load(p2_name)

                # Play nb times
                results_x = []
                for i in range(args.nb - half_nb):
                    results_x.append(play(p1, p2))

                results_o = []
                for i in range(half_nb):
                    results_o.append(play(p2, p1))

                wins_p1 = results_x.count("x") + results_o.count("o")
                wins_p2 = results_x.count("o") + results_o.count("x")
                score_p1 = (wins_p1 - wins_p2) / args.nb

                df_scores.loc[p1_name, p2_name] = score_p1
                df_scores.loc[p2_name, p1_name] = -score_p1

        print("Finished!")
        print("Displaying normalized scores...")

        print(df_scores)
