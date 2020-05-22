from enum import Enum


class MoveTypeEnum(Enum):
    regular_move = 0
    capture = 1
    illegal_move = 2


class TeamEnum(Enum):
    white = 1
    black = -1

class GameStatusEnum(Enum):
    game_continues = "game continues"
    white_wins = "first"
    black_wins = "second"
    tie_game = "tie game"
    incomplete_game = "incomplete game"
    illegal_move = 'illegal move'


ROW_INDEX = 1
COLUMN_INDEX = 0
