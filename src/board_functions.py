"""
statics that are actually board methods
but separate because I want to create Boards en masse
so these are separated to keep the Board class lightweight
"""

import numpy as np
from src.board import Board


def drop_piece_into_column(board: Board, column: int):
    """
    set_space and select_space for look_ahead function

    Args:
        column (int): _description_
        :param column:
        :param board:
    """

    assert isinstance(column, int), f'column should be int but is {type(column)}'
    assert isinstance(board, Board), f'board should be Board but is {type(board)}'
    assert -1 < column < 7, f'columns are numbered 0-6, {column} is out of bounds'
    assert board.spaces[column] == 0, f'column {column} is full'
    row = 0

    # look at next space
    # if empty
    # move to it and look at next space
    # once the next space is not empty
    # place piece on current space

    while board.spaces[((row + 1) * 7) + column] == 0:
        row += 1
        if row == 5:
            # if after updating current row is bottom row
            # stop looking and place piece on current row
            break

    board.spaces[(row * 7) + column] = current_player(board)


def current_player(board: Board) -> int:
    """
    compute whose turn it is based on the existing turn
    """

    turn_sum = 0
    for space in board.spaces:
        turn_sum += space
    assert turn_sum in (1, 0), f'turn sum is {turn_sum}'

    if turn_sum == 0:
        return 1
    return -1


def next_moves(board: Board) -> dict[int: Board]:
    """
    _summary_

    Returns:
        dict[int: Board]: column mapped Board after move is made in that column
    """

    possible_moves = {}

    # look at all columns
    # if top space of column is empty, simulate a possible future move
    # by placing current player's piece in that column
    for column in range(7):
        if board.spaces[column] == 0:
            assert board.spaces[column] == 0
            possible_move = copy_board(board)
            drop_piece_into_column(possible_move, column)
            possible_moves[column] = possible_move
    return possible_moves


def copy_board(board: Board) -> Board:
    """
    copy the board

    Returns:
        Board: _description_
    """

    board_copy = Board()
    board_copy.spaces = np.array(list(board.spaces))
    return board_copy


def print_board(board: Board) -> None:
    """
    provide visual printout of board
    """

    print('\n')
    for row in range(6):
        for column in range(7):
            print(print_space(board, column, row), end=' ')
        print('\n')


def print_space(board: Board, column: int, row: int) -> str:
    """
    convert a space to a string (for display)

    Args:
        column (int): _description_
        row (int): _description_

    Returns:
        str: _description_
        :param row:
        :param column:
        :param board:
    """

    assert board.spaces[(row * 7) + column] in (-1, 0, 1)

    if board.spaces[(row * 7) + column] == 1:
        return ' X '
    if board.spaces[(row * 7) + column] == -1:
        return ' O '
    return ' * '


def can_place(board: Board, space: int) -> bool:
    """
    check if legal move can be made at space

    Args:
        space (int): location of space

    Returns:
        bool: True if space is legal move option
        :param space:
        :param board:
    """

    assert (-1 < space < 42), 'space does not exist; choose between 0-41'
    if not board.spaces[space] == 0:
        return False
    if 34 < space < 42:
        return True
    if board.spaces[space + 7] == 0:
        return False
    return True


def reset_board(board: Board) -> None:
    """
    reset the board
    """
    board.spaces = np.zeros(42, int)


def get_valid_moves(board: Board) -> list[int]:
    """
    returns list of all squares where can_place is True

    Returns:
        list: valid move options
    """
    valid_moves = []
    for i in range(42):
        if can_place(board, i):
            valid_moves.append(i)
    return valid_moves
