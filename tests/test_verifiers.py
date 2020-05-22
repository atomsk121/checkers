import unittest

from board import CheckerBoardFactory, BoardPresetDataclass, CheckerBoardPresets
from checkers_enums import MoveTypeEnum, TeamEnum
from checkers_game import CheckersGame
from checkersmove import CheckersMove


class TestVerifiers(unittest.TestCase):
    def test_verify_is_on_board(self):
        test_board = CheckerBoardFactory.build_board_from_preset(BoardPresetDataclass(8, 100, [(0, 0)], []))
        test_game = CheckersGame(test_board)
        self.assertTrue(test_game.is_move_inside_board(CheckersMove([0, 0, 2, 2])))
        self.assertTrue(test_game.is_move_inside_board(CheckersMove([2, 2, 4, 11])))
        self.assertTrue(test_game.is_move_inside_board(CheckersMove([2, 2, 7, 99])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([4, 11, 11, 11])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([8, 100, 11, 11])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([7, 100, 11, 11])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([8, 99, 11, 11])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([-1, 99, 11, 11])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([5, -2, 11, 11])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([5, 5, 8, 100])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([5, 5, 7, 100])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([5, 5, 8, 99])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([5, 5, 5, -1])))
        self.assertFalse(test_game.is_move_inside_board(CheckersMove([5, 5, -5, 55])))

    def test_find_move_type(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        self.assertEqual(test_game.find_move_type(CheckersMove([0, 0, 1, 1])), MoveTypeEnum.regular_move)
        self.assertEqual(test_game.find_move_type(CheckersMove([0, 0, 2, 2])), MoveTypeEnum.capture)
        self.assertEqual(test_game.find_move_type(CheckersMove([0, 0, 4, 2])), MoveTypeEnum.illegal_move)

    def test_verify_move_is_diagonal(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        self.assertTrue(test_game.verify_move_is_diagonal(CheckersMove([0, 0, 1, 1])))
        self.assertTrue(test_game.verify_move_is_diagonal(CheckersMove([0, 0, 2, 2])))
        self.assertFalse(test_game.verify_move_is_diagonal(CheckersMove([0, 0, 4, 2])))
        self.assertTrue(test_game.verify_move_is_diagonal(CheckersMove([1, 1, 0, 0])))
        self.assertTrue(test_game.verify_move_is_diagonal(CheckersMove([2, 2, 0, 0])))
        self.assertFalse(test_game.verify_move_is_diagonal(CheckersMove([4, 2, 0, 0])))

    def test_verify_target_is_empty(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board, skip_scan_for_pieces_that_can_capture=True)
        self.assertTrue(test_game.verify_target_is_empty(CheckersMove([2, 1, 1, 1])))
        self.assertFalse(test_game.verify_target_is_empty(CheckersMove([1, 1, 2, 1])))

    def test_verify_source_is_correct_color(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board, skip_scan_for_pieces_that_can_capture=True)
        self.assertTrue(test_game.verify_source_is_correct_color(CheckersMove([7, 6, 1, 1]), TeamEnum.black))
        self.assertTrue(test_game.verify_source_is_correct_color(CheckersMove([1, 2, 1, 1]), TeamEnum.white))
        self.assertFalse(test_game.verify_source_is_correct_color(CheckersMove([1, 2, 1, 1]), TeamEnum.black))
        self.assertFalse(test_game.verify_source_is_correct_color(CheckersMove([7, 6, 1, 1]), TeamEnum.white))
        self.assertFalse(test_game.verify_source_is_correct_color(CheckersMove([0, 0, 1, 1]), TeamEnum.white))
        self.assertFalse(test_game.verify_source_is_correct_color(CheckersMove([-1, 0, 1, 1]), TeamEnum.black))

    def test_verify_correct_move_direction(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board, skip_scan_for_pieces_that_can_capture=True)
        self.assertTrue(test_game.verify_correct_move_direction(CheckersMove([7, 6, 1, 1]), TeamEnum.black))
        self.assertFalse(test_game.verify_correct_move_direction(CheckersMove([7, 6, 1, 1]), TeamEnum.white))
        self.assertTrue(test_game.verify_correct_move_direction(CheckersMove([1, 2, 2, 1]), TeamEnum.black))
        self.assertFalse(test_game.verify_correct_move_direction(CheckersMove([1, 2, 2, 1]), TeamEnum.white))
        self.assertTrue(test_game.verify_correct_move_direction(CheckersMove([1, 2, 0, 1]), TeamEnum.black))
        self.assertFalse(test_game.verify_correct_move_direction(CheckersMove([1, 2, 0, 1]), TeamEnum.white))
        self.assertTrue(test_game.verify_correct_move_direction(CheckersMove([2, 1, 4, 3]), TeamEnum.white))
        self.assertFalse(test_game.verify_correct_move_direction(CheckersMove([2, 1, 4, 3]), TeamEnum.black))
        self.assertTrue(test_game.verify_correct_move_direction(CheckersMove([2, 3, 0, 1]), TeamEnum.black))
        self.assertFalse(test_game.verify_correct_move_direction(CheckersMove([2, 3, 0, 1]), TeamEnum.white))