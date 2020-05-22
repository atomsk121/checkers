import unittest

from checkers_game import CheckersGame
from checkersmove import CheckersMove, IllegalMoveException
from move_iterators import create_move_iterator_from_list_of_lists, create_move_iterator_from_move_file
from board import CheckerBoardPresets, CheckerBoardFactory, BoardPresetDataclass
from checkers_enums import TeamEnum
from game_pieces import CheckersGamePiece
from tests.board_presets_for_tests import CheckerBoardTestPresets


class TestRegularMoves(unittest.TestCase):
    def test_valid_move(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        test_game.make_move(CheckersMove([1, 2, 2, 3]))
        self.assertIsInstance(test_game.board[2, 3], CheckersGamePiece)
        self.assertEqual(test_game.board[2, 3].team, TeamEnum.white)
        self.assertIsNone(test_game.board[1, 2])

    def test_cant_move_to_occupied_space_by_other_team(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        move_list = [[1, 2, 2, 3],
                     [2, 5, 3, 4]]
        team_iterator = self.team_iterator()
        for move in create_move_iterator_from_list_of_lists(move_list):
            test_game.make_move(move)
            self.assertIsInstance(test_game.board[move.target], CheckersGamePiece)
            self.assertEqual(test_game.board[move.target].team, next(team_iterator))
            self.assertIsNone(test_game.board[move.source])
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove([2, 3, 3, 4]))

    def test_white_cant_move_backwards(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        move_list = [[1, 2, 2, 3],
                     [2, 5, 3, 4]]
        team_iterator = self.team_iterator()
        for move in create_move_iterator_from_list_of_lists(move_list):
            test_game.make_move(move)
            self.assertIsInstance(test_game.board[move.target], CheckersGamePiece)
            self.assertEqual(test_game.board[move.target].team, next(team_iterator))
            self.assertIsNone(test_game.board[move.source])
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove([2, 3, 1, 2]))

    def test_black_cant_move_backwards(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        move_list = [[1, 2, 2, 3],
                     [2, 5, 3, 4],
                     [2, 3, 1, 4]]
        team_iterator = self.team_iterator()
        for move in create_move_iterator_from_list_of_lists(move_list):
            test_game.make_move(move)
            self.assertIsInstance(test_game.board[move.target], CheckersGamePiece)
            self.assertEqual(test_game.board[move.target].team, next(team_iterator))
            self.assertIsNone(test_game.board[move.source])
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove([3, 4, 2, 5]))

    def test_cant_move_to_occupied_space_by_same_team(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove([1, 0, 0, 1]))

    @staticmethod
    def team_iterator(initial_team: TeamEnum=TeamEnum.white):
        if initial_team is TeamEnum.white:
            yield TeamEnum.white
        while True:
            yield TeamEnum.black
            yield TeamEnum.white


class TestCaptures(unittest.TestCase):
    def test_possible_captures(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.test_capture_board))
        test_game.make_move(CheckersMove([3, 2, 5, 4]))
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.test_capture_board))
        test_game.make_move(CheckersMove([3, 2, 1, 4]))
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.test_capture_board))
        test_game.make_move(CheckersMove([7, 0, 5, 2]))
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.test_capture_board))
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove([0, 1, 1, 2]))

    def test_ignore_capture_move_raises_exception(self):
        list_of_setup_moves = [[1, 2, 2, 3],
                               [0, 5, 1, 4],
                               ]
        illegal_move = [2, 3, 3, 4]
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for move in create_move_iterator_from_list_of_lists(list_of_setup_moves):
            test_game.make_move(move)
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove(illegal_move))

    def test_multi_capture(self):
        test_game = CheckersGame(
            CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.multi_capture_test_board_8_by_8))
        move_list = [[0, 0, 2, 2],
                     [2, 2, 4, 4]
                     ]
        move_iterator = create_move_iterator_from_list_of_lists(move_list)
        test_game.make_move(next(move_iterator))
        self.assertEqual(test_game.current_team, TeamEnum.white)
        test_game.make_move(next(move_iterator))
        self.assertIsNone(test_game.board[0, 0])
        self.assertIsNone(test_game.board[1, 1])
        self.assertIsNone(test_game.board[3, 3])
        self.assertIsInstance(test_game.board[4, 4], CheckersGamePiece)
        self.assertEqual(test_game.current_team, TeamEnum.black)

    def test_multi_capture_not_activated_on_regular_move(self):
        test_board = CheckerBoardFactory.build_board_from_preset(BoardPresetDataclass(8, 8, [(1, 1)], [(3, 3), (5, 5)]))
        test_game = CheckersGame(test_board)
        test_game.make_move(CheckersMove([1, 1, 2, 2]))
        self.assertEqual(test_game.current_team, TeamEnum.black)
        test_game.make_move((CheckersMove([3, 3, 1, 1])))

    def test_multi_capture_possible_with_original_piece_only(self):
        test_board = CheckerBoardFactory.build_board_from_preset(
            BoardPresetDataclass(8, 8, [(2, 2), (6, 4)], [(3, 3), (5, 5)]))
        test_game = CheckersGame(test_board)
        test_game.make_move(CheckersMove([2, 2, 4, 4]))
        self.assertEqual(test_game.current_team, TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game.make_move, CheckersMove([6, 4, 4, 6]))
        test_board2 = CheckerBoardFactory.build_board_from_preset(
            BoardPresetDataclass(8, 8, [(2, 2), (6, 4)], [(3, 3), (5, 5)]))
        test_game2 = CheckersGame(test_board2)
        test_game2.make_move(CheckersMove([2, 2, 4, 4]))
        self.assertEqual(test_game2.current_team, TeamEnum.white)
        test_game2.make_move(CheckersMove([4, 4, 6, 6]))

    def test_extensive_possible_captures(self):
        test_board = CheckerBoardFactory.build_board_from_preset(
            BoardPresetDataclass(8, 8, [(7, 2), (6, 3), (4, 3), (3, 2), (2, 3)], [(5, 4), (4, 5), (5, 6), (6, 5)]))
        test_game = CheckersGame(test_board)
        test_game.switch_team_turn()
        test_game.make_move(CheckersMove([4, 5, 3, 4]))
        self.assertEqual(test_game.current_team, TeamEnum.white)
        white_potential_captures = [[6,3,4,5],
                                    [4, 3, 2, 5],
                                    [2, 3, 4, 5]]
        black_potential_captures = [[3, 4, 1, 2],
                                    [3, 4, 5, 2]]
        for move in create_move_iterator_from_list_of_lists(white_potential_captures):
            self.assertIn(move, test_game.possible_capture_moves[TeamEnum.white])
        for move in create_move_iterator_from_list_of_lists(black_potential_captures):
            self.assertIn(move, test_game.possible_capture_moves[TeamEnum.black])

    def test_potential_capture_added_when_blocking_piece_is_removed(self):
        test_board = CheckerBoardFactory.build_board_from_preset(
            BoardPresetDataclass(8, 8, [(1, 0), (3, 2)], [(2, 1), (2, 3)]))
        test_game = CheckersGame(test_board)
        test_game.switch_team_turn()
        test_game.make_move(CheckersMove([2, 3, 4, 1]))
        self.assertEqual(test_game.current_team, TeamEnum.white)
        self.assertIn(CheckersMove([1, 0, 3, 2]), test_game.possible_capture_moves[TeamEnum.white])


class TestEndGame(unittest.TestCase):
    def test_tie(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.simple_tie_test_board))
        self.assertEqual(test_game.end_game().value, 'tie game')

    def test_white_wins(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.simple_tie_test_board))
        test_game.board.set_up_pieces([(7, 7)], [])
        self.assertEqual(test_game.end_game().value, 'first')

    def test_black_wins(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.simple_tie_test_board))
        test_game.board.set_up_pieces([], [(7, 7)])
        self.assertEqual(test_game.end_game().value, 'second')

    def test_incomplete_game(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardTestPresets.simple_tie_test_board))
        test_game.board.set_up_pieces([], [(5, 5)])
        test_game.switch_team_turn()
        self.assertEqual(test_game.end_game().value, 'incomplete game')


class TestFullGames(unittest.TestCase):
    def test_white_wins_game(self):
        move_iterator = create_move_iterator_from_move_file('games/white.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for move in move_iterator:
            test_game.make_move(move)
        self.assertEqual(test_game.end_game().value, 'first')

    def test_black_wins_game(self):
        move_iterator = create_move_iterator_from_move_file('games/black.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for ind, move in enumerate(move_iterator):
            test_game.make_move(move)
        self.assertEqual(test_game.end_game().value, 'second')

    def test_incomplete_game(self):
        move_iterator = create_move_iterator_from_move_file('games/incomplete.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for ind, move in enumerate(move_iterator):
            test_game.make_move(move)
        self.assertEqual(test_game.end_game().value, 'incomplete game')

class TestRunGame(unittest.TestCase):
    def test_empty_iterator(self):
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8)
        test_game = CheckersGame(test_board)
        move_iterator = create_move_iterator_from_list_of_lists([])
        print(test_game.run_game(move_iterator))

if __name__ == '__main__':
    unittest.main()
