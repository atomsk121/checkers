import argparse
import os

from board import CheckerBoardFactory, CheckerBoardPresets
from checkers_game import CheckersGame
from move_iterators import create_move_iterator_from_move_file


def main():
    parser = argparse.ArgumentParser(description='Please enter file path for game')
    parser.add_argument('path', type=str)
    args = parser.parse_args()
    move_iterator = create_move_iterator_from_move_file(args.path)
    game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
    game_result = game.run_game(move_iterator)
    print(f'{os.path.basename(args.path)} - {game_result}')


if __name__ == '__main__':
    main()