import unittest

from board import Board, CheckerBoardFactory, CheckerBoardPresets, MissingGamePieceException, \
    BoardTileOccupiedException, OutOfBoardException, BoardPresetDataclass
from checkers_enums import TeamEnum
from checkersmove import CheckersMove
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
        self.assertIsNone(test_board[target], CheckersGamePiece)
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
        self.assertIsNone(test_board[target], CheckersGamePiece)
        self.assertRaises(MissingGamePieceException, test_board.capture_piece, source, target, captured_piece)

    def test_board_dimensions(self):
        test_board = CheckerBoardFactory.build_board_from_preset(BoardPresetDataclass(8, 100, [(0, 0)], []))
        test_board.move_piece(CheckersMove([0, 0, 2, 2]).source, CheckersMove([0, 0, 2, 2]).target)
        test_board.move_piece(CheckersMove([2, 2, 4, 11]).source, CheckersMove([2, 2, 4, 11]).target)
        self.assertRaises(OutOfBoardException, test_board.move_piece, CheckersMove([4, 11, 11, 11]).source,
                          CheckersMove([4, 11, 11, 11]).target)

if __name__ == '__main__':
    unittest.main()
