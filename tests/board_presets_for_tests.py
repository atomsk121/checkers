from board import BoardPresetDataclass


class CheckerBoardTestPresets:
    multi_capture_test_board_8_by_8 = BoardPresetDataclass(8, 8, [(0, 0)], [(1, 1), (3, 3)])
    simple_tie_test_board = BoardPresetDataclass(8, 8, [(0, 7)], [(1, 0)])
    test_capture_board = BoardPresetDataclass(8, 8, [(3, 2), (0, 1), (7, 0)], [(4, 3), (2, 3), (6, 1)])
