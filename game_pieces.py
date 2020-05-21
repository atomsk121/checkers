from dataclasses import dataclass

from checkers_enums import TeamEnum


@dataclass
class CheckersGamePiece:
    team: TeamEnum