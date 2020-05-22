from typing import List


class CheckersMove:
    def __init__(self, move: List[int]):
        if len(move) != 4:
            raise IllegalMoveException(f"Can't createa Move: Expected 4 arguments, got{len(move)} arguments instead")
        for coordinate in move:
            int(coordinate)
        self.source = (move[0], move[1])
        self.target = (move[2], move[3])

    def __eq__(self, other):
        return (self.source, self.target) == other

    def __hash__(self):
        return hash(f"source {self.source} target {self.target}")

    def __str__(self):
        return f'{self.source}, {self.target}'



class IllegalMoveException(Exception):
    pass
