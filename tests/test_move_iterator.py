import unittest

from checkersmove import CheckersMove
from move_iterators import create_move_iterator_from_list_of_lists, create_move_iterator_from_move_file


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
        move_iterator = create_move_iterator_from_move_file('games/white.txt')
        self.assertEqual(next(move_iterator), CheckersMove([1, 2, 0, 3]))
        self.assertEqual(next(move_iterator), CheckersMove([4, 5, 3, 4]))