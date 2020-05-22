from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

from game_pieces import CheckersGamePiece
from checkers_enums import TeamEnum, ROW_INDEX, COLUMN_INDEX


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
        if not (0 <= coordinates[ROW_INDEX] < self.length and 0 <= coordinates[COLUMN_INDEX] < self.height):
            raise OutOfBoardException()

    def __getitem__(self, item: tuple):
        return self.board[item[COLUMN_INDEX]][item[ROW_INDEX]]


class CheckerBoard(Board):
    def __init__(self, board_length, board_height):
        super().__init__(board_length, board_height)
        self.active_pieces = {}

    def remove_piece(self, coordinates: Tuple[int, int]):
        self.board[coordinates[COLUMN_INDEX]][coordinates[ROW_INDEX]] = None
        self.active_pieces.pop((coordinates[COLUMN_INDEX], coordinates[ROW_INDEX]))

    def verify_game_piece_can_be_moved(self, source: Tuple[int, int], target: Tuple[int, int]):
        self.check_if_coordinates_are_on_board(source)
        self.check_if_coordinates_are_on_board(target)
        if self.board[source[COLUMN_INDEX]][source[ROW_INDEX]] is None:
            raise MissingGamePieceException()
        if self.board[target[COLUMN_INDEX]][target[ROW_INDEX]]:
            raise BoardTileOccupiedException()

    def verify_game_piece_can_be_captured(self, coordinates: Tuple[int, int]):
        if self.board[coordinates[COLUMN_INDEX]][coordinates[ROW_INDEX]] is None:
            raise MissingGamePieceException()

    def move_piece(self, source: Tuple[int, int], target: Tuple[int, int]):
        self.verify_game_piece_can_be_moved(source, target)
        self.board[target[COLUMN_INDEX]][target[ROW_INDEX]] = self.board[source[COLUMN_INDEX]][source[ROW_INDEX]]
        self.active_pieces[(target[COLUMN_INDEX], target[ROW_INDEX])] = self.board[source[COLUMN_INDEX]][source[ROW_INDEX]].team
        self.remove_piece(source)

    def capture_piece(self, source: Tuple[int, int], target: Tuple[int, int],
                      captured_piece_coordinates: Tuple[int, int]):
        self.check_if_coordinates_are_on_board(captured_piece_coordinates)
        self.verify_game_piece_can_be_captured(captured_piece_coordinates)
        self.move_piece(source, target)
        self.remove_piece(captured_piece_coordinates)

    def _create_piece(self, coordinates: Tuple[int, int], team: TeamEnum):
        self.check_if_coordinates_are_on_board(coordinates)
        self.board[coordinates[COLUMN_INDEX]][coordinates[ROW_INDEX]] = CheckersGamePiece(team)
        self.active_pieces[(coordinates[COLUMN_INDEX], coordinates[ROW_INDEX])] = team

    def set_up_pieces(self, white_coordinates: List[tuple], black_coordinates: List[Tuple]):
        # TODO List Comprension
        for coordinates in white_coordinates:
            self._create_piece(coordinates, TeamEnum.white)
        for coordinates in black_coordinates:
            self._create_piece(coordinates, TeamEnum.black)

    def __str__(self):
        board_rep = ''
        for i in range(self.length-1,-1,-1):
            for j in range(self.height-1,-1,-1):
                if self[j,i] is None:
                    board_rep += '_'
                else:
                    board_rep += self[j,i].team.name[0]
            board_rep += '\n'
        return board_rep

    @property
    def score(self)-> Dict:
        scores = {TeamEnum.white: 0, TeamEnum.black: 0}
        for team in self.active_pieces.values():
            scores[team] += 1
        return scores


@dataclass
class BoardPresetDataclass:
    height: int
    length: int
    white_coordinates: List[Tuple[int, int]]
    black_coordinates: List[Tuple[int, int]]


class CheckerBoardPresets:
    standard_8_by_8 = BoardPresetDataclass(8, 8,
                                           [(i, j) for i in range(8) for j in range(3) if (i+j)%2 == 1],
                                           [(i, j) for i in range(8) for j in range(5, 8) if (i+j)%2 == 1])
    multi_capture_test_board_8_by_8 = BoardPresetDataclass(8, 8, [(0, 0)], [(1, 1), (3, 3)]) #TODO Move to test directory
    simple_tie_test_board = BoardPresetDataclass(8, 8, [(0, 7)], [(1, 0)]) #TODO Move to test directory


class CheckerBoardFactory:
    @staticmethod
    def build_board_from_preset(board_preset: BoardPresetDataclass) -> CheckerBoard:
        built_board = CheckerBoard(board_preset.length, board_preset.height)
        built_board.set_up_pieces(board_preset.white_coordinates, board_preset.black_coordinates)
        return built_board
