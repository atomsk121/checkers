from typing import Type, Iterator, Tuple, Dict, List

from checkersmove import CheckersMove, IllegalMoveException
from board import Board, BoardException, CheckerBoard
from checkers_enums import MoveTypeEnum, TeamEnum, GameStatusEnum, COLUMN_INDEX, ROW_INDEX
from move_loader import create_move_iterator_from_list_of_lists


class CheckersGame:
    FIRST_TURN = TeamEnum.white
    SECOND_TURN = TeamEnum.black

    def __init__(self, board: CheckerBoard):
        self.board = board #TODO CHECK IF PRESET BOARD HAS PIECES THAT CAN BE CAPTURED
        self.game_status = GameStatusEnum.game_continues
        self.current_team = self.FIRST_TURN
        self.other_team = self.SECOND_TURN
        self.possible_capture_moves: Dict[TeamEnum, List[CheckersMove]] = {TeamEnum.white: [], TeamEnum.black: []}
        self.multiple_capture_possibilities = []

    def switch_team_turn(self):
        if self.current_team == TeamEnum.white:
            self.current_team = TeamEnum.black
            self.other_team = TeamEnum.white
        else:
            self.current_team = TeamEnum.white
            self.other_team = TeamEnum.black

    @property
    def game_status(self):
        return self._game_status

    @game_status.setter
    def game_status(self, status: GameStatusEnum):
        self._game_status = status

    def is_move_inside_board(self, move: CheckersMove) -> bool:
        # todo check dimensions
        if not (0 < move.source[0] < self.board.height) or not (0 < move.source[1] < self.board.length):
            return False
        if not (0 < move.target[0] < self.board.height) or not (0 < move.target[1] < self.board.length):
            return False
        return True

    def find_move_type(self, move: CheckersMove) -> MoveTypeEnum:
        if abs(move.source[1] - move.target[1]) == 1:
            return MoveTypeEnum.regular_move
        if abs(move.source[1] - move.target[1]) == 2:
            return MoveTypeEnum.capture

    @staticmethod
    def check_move_is_diagonal(move: CheckersMove):
        return abs(move.source[1] - move.target[1]) == abs(move.source[0] - move.target[0])

    def check_if_target_is_empty(self, move: CheckersMove) -> bool:
        if self.board[move.target] is not None:
            return False
        return True

    def check_if_source_is_correct_color(self, move: CheckersMove, team: TeamEnum) -> bool:
        return self.board[move.source] and self.board[move.source].team is team


    @staticmethod
    def check_correct_move_direction(move: CheckersMove, team: TeamEnum):
        return (move.target[ROW_INDEX] - move.source[ROW_INDEX]) * team.value > 0

    @staticmethod
    def verify_move_distance_is_valid(move: CheckersMove):
        return abs(move.target[ROW_INDEX] - move.source[ROW_INDEX]) <= 2

    @staticmethod
    def get_coordinates_for_piece_to_capture(move: CheckersMove, team: TeamEnum):
        coordinates = move.source[ROW_INDEX] + team.value, \
                      int((move.target[COLUMN_INDEX] + move.source[COLUMN_INDEX]) / 2)

        return coordinates

    def check_if_there_is_a_piece_to_capture(self, move, team: TeamEnum):
        coordinates = self.get_coordinates_for_piece_to_capture(move, team)
        if not self.board[coordinates[ROW_INDEX], coordinates[COLUMN_INDEX]] or \
                self.board[coordinates[ROW_INDEX], coordinates[COLUMN_INDEX]] == team:
            return False
        return True

    def check_if_move_is_valid(self, move: CheckersMove, team: TeamEnum = None):
        if team is None:
            team = self.current_team
        # if self.is_move_inside_board(move):
        #     raise IllegalMoveException()
        # if not self.check_if_target_is_empty(move):
        #     raise IllegalMoveException()
        if not self.check_if_source_is_correct_color(move, team):
            raise IllegalMoveException()
        if not self.check_move_is_diagonal(move):
            raise IllegalMoveException()
        if not self.check_correct_move_direction(move, team):
            raise IllegalMoveException()
        if not self.verify_move_distance_is_valid(move):
            raise IllegalMoveException()
        if self.find_move_type(move) == MoveTypeEnum.capture:
            if not self.check_if_there_is_a_piece_to_capture(move, team):
                raise IllegalMoveException()

    def find_possible_capture_moves_as_a_result_of_removed_piece(self, coordinates: Tuple[int, int]):
        for team in [TeamEnum.white, TeamEnum.black]:
            raw_move_list = [[coordinates[COLUMN_INDEX] + 2,
                              coordinates[ROW_INDEX] - 2 * team.value,
                              coordinates[COLUMN_INDEX] - 2,
                              coordinates[ROW_INDEX],
                              ],
                             [coordinates[COLUMN_INDEX] - 2,
                              coordinates[ROW_INDEX] - 2 * team.value,
                              coordinates[COLUMN_INDEX] + 2,
                              coordinates[ROW_INDEX],
                              ]
                             ]
            for potential_move in create_move_iterator_from_list_of_lists(raw_move_list):
                if self.verify_legal_capture(potential_move, team):
                    self.possible_capture_moves[team].append(potential_move)

    def find_possible_capture_moves_as_a_result_of_placed_piece_for_other_team(self, move: CheckersMove):
        raw_move_list = [[move.target[COLUMN_INDEX] + 1,
                          move.target[ROW_INDEX] + self.current_team.value,
                          move.target[COLUMN_INDEX] - 1,
                          move.source[ROW_INDEX],
                          ],
                         [move.target[COLUMN_INDEX] - 1,
                          move.target[ROW_INDEX] + self.current_team.value,
                          move.target[COLUMN_INDEX] + 1,
                          move.source[ROW_INDEX],
                          ],
                         ]
        for potential_move in create_move_iterator_from_list_of_lists(raw_move_list):
            if self.verify_legal_capture(potential_move, self.other_team):
                self.possible_capture_moves[self.other_team].append(potential_move)

    def add_multi_capture_moves_as_a_result_of_placed_piece_for_current_team(self, move: CheckersMove):
        raw_move_list = [[move.target[COLUMN_INDEX],
                          move.target[ROW_INDEX],
                          move.target[COLUMN_INDEX] + 2,
                          move.target[ROW_INDEX] + 2,
                          ],
                         [move.target[COLUMN_INDEX],
                          move.target[ROW_INDEX],
                          move.target[COLUMN_INDEX] - 2,
                          move.target[ROW_INDEX] + self.current_team.value * 2,
                          ],
                         ]
        for potential_move in create_move_iterator_from_list_of_lists(raw_move_list):
            if self.verify_legal_capture(potential_move, self.current_team):
                if self.find_move_type(move) == MoveTypeEnum.capture:
                    self.multiple_capture_possibilities.append(potential_move)
                self.possible_capture_moves[self.current_team].append(potential_move)

    def verify_legal_capture(self, move: CheckersMove, team: TeamEnum):
        try:
            self.check_if_move_is_valid(move, team)
            return True
        except IllegalMoveException:
            return False

    def add_all_possible_captures_as_result_of_move(self, move: CheckersMove):
        self.add_multi_capture_moves_as_a_result_of_placed_piece_for_current_team(move)
        self.find_possible_capture_moves_as_a_result_of_placed_piece_for_other_team(move)
        self.find_possible_capture_moves_as_a_result_of_removed_piece(move.source)
        if self.find_move_type(move) == MoveTypeEnum.capture:
            self.find_possible_capture_moves_as_a_result_of_removed_piece(
                self.get_coordinates_for_piece_to_capture(move, self.current_team)
            )

    def check_if_move_is_one_of_available_captures(self, move: CheckersMove):
        if self.multiple_capture_possibilities and move not in self.multiple_capture_possibilities:
            raise IllegalMoveException('Multiple Capture Available')
        elif self.possible_capture_moves[self.current_team] and move not in self.possible_capture_moves[self.current_team]:
            raise IllegalMoveException('Capture available')

    def remove_illegal_moves_from_immediate_and_possible_capture_moves(self):
        for move in self.multiple_capture_possibilities:
            if not self.verify_legal_capture(move, self.current_team):
                self.multiple_capture_possibilities.remove(move)
        for team, move_set in self.possible_capture_moves.items():
            for move in move_set:
                if not self.verify_legal_capture(move, team):
                    move_set.remove(move)

    def make_move(self, move: CheckersMove):
        self.check_if_move_is_valid(move)
        self.check_if_move_is_one_of_available_captures(move)
        try:
            if self.find_move_type(move) == MoveTypeEnum.regular_move:
                self.board.move_piece(move.source, move.target)
            elif self.find_move_type(move) == MoveTypeEnum.capture:
                self.board.capture_piece(move.source, move.target,
                                         self.get_coordinates_for_piece_to_capture(move, self.current_team))
            else:
                raise IllegalMoveException('Unknown move type')
        except BoardException:
            raise IllegalMoveException()
        self.add_all_possible_captures_as_result_of_move(move)
        self.remove_illegal_moves_from_immediate_and_possible_capture_moves()
        if not self.multiple_capture_possibilities:
            self.switch_team_turn()

    def check_if_piece_can_move_regularly(self, coordinates: Tuple[int, int]) -> bool:
        team = self.board[coordinates[ROW_INDEX], coordinates[COLUMN_INDEX]].team
        possible_moves = [[coordinates[COLUMN_INDEX], coordinates[ROW_INDEX], coordinates]]

    def end_game(self):
        pass


if __name__ == '__main__':
    print(len(Board(8, 8).board[0]))
