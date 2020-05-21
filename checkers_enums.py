from enum import Enum


class MoveTypeEnum(Enum):
    regular_move = 0
    capture = 1
    illegal_move = 2


class TeamEnum(Enum):
    white = 1
    black = -1

class GameStatusEnum(Enum):
    game_continues = "game_continues"
    white_wins = "white_wins"
    black_wins = "black_wins"
    tie_game = "tie_game"
    illegal_move = 'illegal_move'


ROW_INDEX = 1
COLUMN_INDEX = 0
