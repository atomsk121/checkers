import unittest

from board import CheckerBoardFactory, CheckerBoardPresets
from checkers_enums import TeamEnum
from checkers_game import CheckersGame
from checkersmove import CheckersMove, IllegalMoveException
from tests.board_presets_for_tests import CheckerBoardTestPresets


class TestCheckerMove(unittest.TestCase):
    def test_str_coordinate(self):
        self.assertRaises(ValueError, CheckersMove, ['a', 2, 3, 4])
        self.assertRaises(ValueError, CheckersMove, [2, 'a', 3, 4])
        self.assertRaises(ValueError, CheckersMove, [2, 3, 'a', 4])
        self.assertRaises(ValueError, CheckersMove, [2, 3, 4, 'a'])

    def test_too_many_arguments(self):
        self.assertRaises(IllegalMoveException, CheckersMove, [1, 2, 3, 4, 5])

    def test_too_little_arguments(self):
        self.assertRaises(IllegalMoveException, CheckersMove, [3, 4, 5])

    def test_check_if_there_is_a_piece_to_capture(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.multi_capture_test_board_8_by_8)
        test_game = CheckersGame(test_board)
        self.assertTrue(test_game.check_if_there_is_a_piece_to_capture(CheckersMove([0, 0, 2, 2]), team=TeamEnum.white))
        self.assertFalse(
            test_game.check_if_there_is_a_piece_to_capture(CheckersMove([0, 0, 2, 2]), team=TeamEnum.black))
        test_game.board.set_up_pieces([(1, 2), (3, 4)], [(2, 3)])
        self.assertTrue(test_game.check_if_there_is_a_piece_to_capture(CheckersMove([1, 2, 3, 4]), team=TeamEnum.white))
        self.assertFalse(test_game.check_if_there_is_a_piece_to_capture(CheckersMove([3, 3, 5, 5]), TeamEnum.black))
        self.assertFalse(test_game.check_if_there_is_a_piece_to_capture(CheckersMove([3, 3, 2, 2]), TeamEnum.black))
        test_game.check_if_there_is_a_piece_to_capture(CheckersMove([0, 0, 2, 2]), team=TeamEnum.white)

    def test_verify_move_is_valid(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([1, 0, 0, 1]),
                          TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([0, 1, 2, 3]),
                          TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([0, 1, 2, 3]),
                          TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([0, 1, 2, 3]),
                          TeamEnum.black)
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([1, 2, 0, 3]),
                          TeamEnum.black)
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([1, 2, -1, 4]),
                          TeamEnum.white)
        test_game.board.remove_piece((4, 5))
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([1, 2, 4, 5]),
                          TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game.verify_move_is_valid, CheckersMove([7, 2, 5, 3]),
                          TeamEnum.white)
        test_game.verify_move_is_valid(CheckersMove([1, 2, 0, 3]), TeamEnum.white)
        test_game.verify_move_is_valid(CheckersMove([3, 2, 2, 3]), TeamEnum.white)
        test_game.verify_move_is_valid(CheckersMove([3, 2, 4, 3]), TeamEnum.white)
        test_game2 = CheckersGame(
            CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.multi_capture_test_board_8_by_8))
        test_game2.verify_move_is_valid(CheckersMove([0, 0, 2, 2]), TeamEnum.white)
        test_game2.board.set_up_pieces([(5, 6)], [(4, 5)])
        self.assertRaises(IllegalMoveException, test_game2.verify_move_is_valid, CheckersMove([5, 6, 6, 5]),
                          TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game2.verify_move_is_valid, CheckersMove([5, 6, 3, 4]),
                          TeamEnum.white)

if __name__ == '__main__':
    unittest.main()
