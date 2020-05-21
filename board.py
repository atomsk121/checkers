from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

from game_pieces import CheckersGamePiece
from checkers_enums import TeamEnum, COLUMN_INDEX, ROW_INDEX


class BoardException(Exception):
    pass


class OutOfBoardException(BoardException):
    pass


class BoardTileOccupiedException(BoardException):
    pass


class MissingGamePieceException(BoardException):
    pass


class Board:
    def __init__(self, board_length: int, board_height: int):
        self.length = board_length
        self.height = board_height
        self.board: List[List[Optional[CheckersGamePiece]]] = [[None for _ in range(board_length)] for _ in
                                                               range(board_height)]

    def check_if_coordinates_are_on_board(self, coordinates: Tuple[int, int]):
        if not (0 <= coordinates[COLUMN_INDEX] < self.length and 0 <= coordinates[ROW_INDEX] < self.height):
            raise OutOfBoardException()

    def __getitem__(self, item: tuple):
        return self.board[item[ROW_INDEX]][item[COLUMN_INDEX]]


class CheckerBoard(Board):
    def __init__(self, board_length, board_height):
        super().__init__(board_length, board_height)
        self.active_pieces = {}

    def remove_piece(self, coordinates: Tuple[int, int]):
        self.board[coordinates[ROW_INDEX]][coordinates[COLUMN_INDEX]] = None
        self.active_pieces.pop(coordinates[ROW_INDEX], coordinates[COLUMN_INDEX])

    def verify_game_piece_can_be_moved(self, source: Tuple[int, int], target: Tuple[int, int]):
        self.check_if_coordinates_are_on_board(source)
        self.check_if_coordinates_are_on_board(target)
        if self.board[source[ROW_INDEX]][source[COLUMN_INDEX]] is None:
            raise MissingGamePieceException()
        if self.board[target[ROW_INDEX]][target[COLUMN_INDEX]]:
            raise BoardTileOccupiedException()

    def verify_game_piece_can_be_captured(self, coordinates: Tuple[int, int]):
        if self.board[coordinates[ROW_INDEX]][coordinates[COLUMN_INDEX]] is None:
            raise MissingGamePieceException()

    def move_piece(self, source: Tuple[int, int], target: Tuple[int, int]):
        self.verify_game_piece_can_be_moved(source, target)
        self.board[target[ROW_INDEX]][target[COLUMN_INDEX]] = self.board[source[ROW_INDEX]][source[COLUMN_INDEX]]
        self.active_pieces[target[ROW_INDEX], target[COLUMN_INDEX]] = self.board[source[ROW_INDEX]][source[COLUMN_INDEX]].team
        self.remove_piece(source)

    def capture_piece(self, source: Tuple[int, int], target: Tuple[int, int],
                      captured_piece_coordinates: Tuple[int, int]):
        self.check_if_coordinates_are_on_board(captured_piece_coordinates)
        self.verify_game_piece_can_be_captured(captured_piece_coordinates)
        self.move_piece(source, target)
        self.remove_piece(captured_piece_coordinates)

    def _create_piece(self, coordinates: Tuple[int, int], team: TeamEnum):
        self.check_if_coordinates_are_on_board(coordinates)
        self.board[coordinates[ROW_INDEX]][coordinates[COLUMN_INDEX]] = CheckersGamePiece(team)
        self.active_pieces[coordinates[ROW_INDEX], coordinates[COLUMN_INDEX]] = team

    def set_up_pieces(self, white_coordinates: List[tuple], black_coordinates: List[Tuple]):
        # TODO List Comprension
        for coordinates in white_coordinates:
            self._create_piece(coordinates, TeamEnum.white)
        for coordinates in black_coordinates:
            self._create_piece(coordinates, TeamEnum.black)

    def print_board(self):
        for row in self.board:
            print(row)


@dataclass
class BoardPresetDataclass:
    height: int
    length: int
    white_coordinates: List[Tuple[int, int]]
    black_coordinates: List[Tuple[int, int]]


class CheckerBoardPresets:
    standard_8_by_8 = BoardPresetDataclass(8, 8,
                                           [(1, 0), (3, 0), (5, 0), (7, 0),
                                            (0, 1), (2, 1), (4, 1), (6, 1),
                                            (1, 2), (3, 2), (5, 2), (7, 2)],
                                           [(0, 5), (2, 5), (4, 5), (6, 5),
                                            (1, 6), (3, 6), (5, 6), (7, 6),
                                            (0, 7), (2, 7), (4, 7), (6, 7)])
    multi_capture_test_board_8_by_8 = BoardPresetDataclass(8, 8, [(0, 0)], [(1, 1), (3, 3)])


class CheckerBoardFactory:
    @staticmethod
    def build_board_from_preset(board_preset: BoardPresetDataclass) -> CheckerBoard:
        built_board = CheckerBoard(board_preset.length, board_preset.height)
        built_board.set_up_pieces(board_preset.white_coordinates, board_preset.black_coordinates)
        return built_board
