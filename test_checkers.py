import unittest

from checkers_game import CheckersGame
from checkersmove import CheckersMove, IllegalMoveException
from move_loader import create_move_iterator_from_list_of_lists, create_move_iterator_from_move_file
from board import Board, MissingGamePieceException, BoardTileOccupiedException, \
    OutOfBoardException, CheckerBoardPresets, CheckerBoardFactory, BoardPresetDataclass
from checkers_enums import TeamEnum, MoveTypeEnum
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
        self.assertIsNone(test_board[target], CheckersGamePiece)
        self.assertRaises(MissingGamePieceException, test_board.capture_piece, source, target, captured_piece)

    def test_board_dimensions(self):
        test_board = CheckerBoardFactory.build_board_from_preset(BoardPresetDataclass(8, 100, [(0, 0)], []))
        test_board.move_piece(CheckersMove([0, 0, 2, 2]).source, CheckersMove([0, 0, 2, 2]).target)
        test_board.move_piece(CheckersMove([2, 2, 4, 11]).source, CheckersMove([2, 2, 4, 11]).target)
        self.assertRaises(OutOfBoardException, test_board.move_piece, CheckersMove([4, 11, 11, 11]).source,
                          CheckersMove([4, 11, 11, 11]).target)


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
        test_board = CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.multi_capture_test_board_8_by_8)
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
            CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.multi_capture_test_board_8_by_8))
        test_game2.verify_move_is_valid(CheckersMove([0, 0, 2, 2]), TeamEnum.white)
        test_game2.board.set_up_pieces([(5, 6)], [(4, 5)])
        self.assertRaises(IllegalMoveException, test_game2.verify_move_is_valid, CheckersMove([5, 6, 6, 5]),
                          TeamEnum.white)
        self.assertRaises(IllegalMoveException, test_game2.verify_move_is_valid, CheckersMove([5, 6, 3, 4]),
                          TeamEnum.white)


class TestMoveIterator(unittest.TestCase):
    def test_load_moves_from_list(self):
        list_of_moves_to_convert = [[1, 2, 2, 3],
                                    [0, 5, 1, 4],
                                    [2, 3, 0, 5],
                                    ]
        list_of_moves = [CheckersMove([1, 2, 2, 3]),
                         CheckersMove([0, 5, 1, 4]),
                         CheckersMove([2, 3, 0, 5]),
                         ]

        for ind, move in enumerate(create_move_iterator_from_list_of_lists(list_of_moves_to_convert)):
            self.assertEqual(list_of_moves[ind], move)

    def test_move_iterator_from_path(self):
        move_iterator = create_move_iterator_from_move_file('white.txt')
        self.assertEqual(next(move_iterator), CheckersMove([1, 2, 0, 3]))
        self.assertEqual(next(move_iterator), CheckersMove([4, 5, 3, 4]))


class TestCaptures(unittest.TestCase):
    def test_possible_captures(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.test_capture_board))
        test_game.make_move(CheckersMove([3, 2, 5, 4]))
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.test_capture_board))
        test_game.make_move(CheckersMove([3, 2, 1, 4]))
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.test_capture_board))
        test_game.make_move(CheckersMove([7, 0, 5, 2]))
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.test_capture_board))
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
            CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.multi_capture_test_board_8_by_8))
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
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.simple_tie_test_board))
        self.assertEqual(test_game.end_game().value, 'tie game')

    def test_white_wins(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.simple_tie_test_board))
        test_game.board.set_up_pieces([(7, 7)], [])
        self.assertEqual(test_game.end_game().value, 'first')

    def test_black_wins(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.simple_tie_test_board))
        test_game.board.set_up_pieces([], [(7, 7)])
        self.assertEqual(test_game.end_game().value, 'second')

    def test_incomplete_game(self):
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.simple_tie_test_board))
        test_game.board.set_up_pieces([], [(5, 5)])
        test_game.switch_team_turn()
        self.assertEqual(test_game.end_game().value, 'Incomplete game')


class TestFullGames(unittest.TestCase):
    def test_white_wins_game(self):
        move_iterator = create_move_iterator_from_move_file('white.txt')
        test_game = CheckersGame(CheckerBoardFactory.build_board_from_preset(CheckerBoardPresets.standard_8_by_8))
        for move in move_iterator:
            test_game.make_move(move)
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

    def test_incomplete_game(self):
        # TODO Better incomplete test
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
