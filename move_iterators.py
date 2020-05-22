from typing import Iterator, List

from checkersmove import CheckersMove, IllegalMoveException


def create_move_iterator_from_move_file(path: str) -> Iterator[CheckersMove]:
    with open(path, 'r') as file:
        for line in file:
            try:
                move = CheckersMove([int(coord) for coord in line.split(',')])
            except ValueError as e:
                raise IllegalMoveException(str(e))
            yield move


def create_move_iterator_from_list_of_lists(list_of_moves: List[List[int]]) -> Iterator[CheckersMove]:
    for move in list_of_moves:
        try:
            move = CheckersMove(move)
        except ValueError as e:
            raise IllegalMoveException(str(e))
        yield move
