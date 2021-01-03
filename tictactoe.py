"""Compares tic-tac-toe strategies by having them compete

Mainly designed for Reinforcement Learning techniques
designed using state value functions or action-state
value functions.
"""
import argparse

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
        "--nb_plays",
        type=str,
        default="1000",
        dest="nb",
        help="Number of games to run",
    )

    args = parser.parse_args()

    print(args)
