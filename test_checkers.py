import unittest

from checkers_game import CheckersGame
from checkersmove import CheckersMove, IllegalMoveException
from move_loader import create_move_iterator_from_list_of_lists, create_move_iterator_from_move_file
from board import Board, MissingGamePieceException, BoardTileOccupiedException, \
    OutOfBoardException, CheckerBoardPresets, CheckerBoardFactory
from checkers_enums import TeamEnum
from game_pieces import CheckersGamePiece


class TestBoardInitialization(unittest.TestCase):
    def test_board_size(self):
        test_board = Board(8, 8)
        self.assertEqual((len(test_board.board)), 8)
        for row in test_board.board:
            self.assertEqual((len(row)), 8)


class TestBoardMoves(unittest.TestCase):
    def test_move_piece(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        source = (1, 0)
        target = (1, 1)
        self.assertIsInstance(test_board[source], CheckersGamePiece)
        self.assertEqual(test_board[source].team, TeamEnum.white)
        self.assertIsNone(test_board[(target)], CheckersGamePiece)
        test_board.move_piece(source, target)
        self.assertIsInstance(test_board[target], CheckersGamePiece)
        self.assertEqual(test_board[target].team, TeamEnum.white)
        self.assertIsNone(test_board[source], CheckersGamePiece)

    def test_move_piece_with_bad_source(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        source = (1, 1)
        target = (1, 0)
        self.assertRaises(MissingGamePieceException, test_board.move_piece, source, target)

    def test_move_piece_with_occupied_target(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        source = (1, 0)
        target = (3, 0)
        self.assertRaises(BoardTileOccupiedException, test_board.move_piece, source, target)

    def test_move_piece_to_outside_the_board(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        source = (1, 0)
        for target in [(8, 0), (-1, 0), (0, 8), (0, -1), (0, 11)]:
            self.assertRaises(OutOfBoardException, test_board.move_piece, source, target)

    def test_capture_piece(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        source = (1, 0)
        target = (1, 1)
        captured_piece = (0, 7)
        self.assertIsInstance(test_board[source], CheckersGamePiece)
        self.assertEqual(test_board[source].team, TeamEnum.white)
        self.assertIsInstance(test_board[captured_piece], CheckersGamePiece)
        self.assertEqual(test_board[captured_piece].team, TeamEnum.black)
        self.assertIsNone(test_board[target], CheckersGamePiece)
        test_board.capture_piece(source, target, captured_piece)
        self.assertIsInstance(test_board[target], CheckersGamePiece)
        self.assertEqual(test_board[target].team, TeamEnum.white)
        self.assertIsNone(test_board[source], CheckersGamePiece)
        self.assertIsNone(test_board[captured_piece], CheckersGamePiece)

    def test_no_piece_to_capture(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        source = (1, 0)
        target = (1, 1)
        captured_piece = (0, 4)
        self.assertIsInstance(test_board[source], CheckersGamePiece)
        self.assertEqual(test_board[source].team, TeamEnum.white)
        self.assertIsNone(test_board[(target)], CheckersGamePiece)
        self.assertRaises(MissingGamePieceException, test_board.capture_piece, source, target, captured_piece)


class TestCheckersMoves(unittest.TestCase):
    def test_valid_game_movement(self):
        pass

    def test_ignore_capture_move(self):
        list_of_setup_moves = [[1, 2, 2, 3],
                               [0, 5, 1, 4],
                               ]
        illegal_move = [2, 3, 3, 4]
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for move in create_move_iterator_from_list_of_lists(list_of_setup_moves):
            test_game.make_move(move)
        self.assertRaises(IllegalMoveException,test_game.make_move, CheckersMove(illegal_move))

    def test_multi_capture(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.multi_capture_test_board_8_by_8))
        move_list = [[0,0,2,2],
                     [2,2,4,4]
                     ]
        for move in create_move_iterator_from_list_of_lists(move_list):
            test_game.make_move(move)
        self.assertIsNone(test_game.board[0, 0])
        self.assertIsNone(test_game.board[1, 1])
        self.assertIsNone(test_game.board[3, 3])
        self.assertIsInstance(test_game.board[4, 4], CheckersGamePiece)



class TestMoveLoader(unittest.TestCase):
    def test_load_moves_from_list(self):
        list_of_moves = [[1, 2, 2, 3],
                         [0, 5, 1, 4],
                         [2, 3, 0, 5],
                         ]
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for move in create_move_iterator_from_list_of_lists(list_of_moves):
            test_game.make_move(move)

class TestGames(unittest.TestCase):
    def test_move_iterator_from_path(self):
        #TODO Make smaller test
        move_iterator = create_move_iterator_from_move_file('white.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        # try:
        for move in move_iterator:
            test_game.make_move(move)
        # except IllegalMoveException:
        #     print(move)
        self.assertEqual(test_game.end_game().value, 'first')

    def test_white_wins_game(self):
        move_iterator = create_move_iterator_from_move_file('white.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        # try:
        for move in move_iterator:
            test_game.make_move(move)
        # except IllegalMoveException:
        #     print(move)
        self.assertEqual(test_game.end_game().value, 'first')

    def test_black_wins_game(self):
        move_iterator = create_move_iterator_from_move_file('black.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        # try:
        for ind, move in enumerate(move_iterator):
            test_game.make_move(move)
        # except IllegalMoveException:
        #     print(move)
        self.assertEqual(test_game.end_game().value, 'second')

    def test_tie(self):
        #TODO Test better tie game?
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.simple_tie_test_board))
        self.assertEqual(test_game.end_game().value, 'tie game')

    def test_incomplete_game(self):
        #TODO Better incomplete test
        move_iterator = create_move_iterator_from_move_file('incomplete.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        # try:
        for ind, move in enumerate(move_iterator):
            test_game.make_move(move)
        # except IllegalMoveException:
        #     print(move)
        self.assertEqual(test_game.end_game().value, 'Incomplete game')

if __name__ == '__main__':
    unittest.main()
