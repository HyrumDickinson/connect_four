'''
contains statics
statics are mostly board functions, kept separate from Board to keep Board lightweight
'''

import numpy as np
from board import Board


# plays one turn for lookAhead function
def go_for_la(board: Board, i: int) -> Board:
    set_select_space_for_la(board, i)

def get_next_moves(board: Board) -> list[Board]:
    '''
    _summary_

    Returns:
        list[Board]: _description_
    '''

    moves = next_moves(board)
    for i in range(7):
        # if space to make a move, # makes a move
        if moves[i].spaces[i] == 0:
            moves[i].go_for_la(i)
        else:
            moves[i] = 9
    return moves


def get_best_move(board: Board, depth: int) -> None:
    '''
    _summary_

    Args:
        depth (_type_): _description_
    '''

    if depth == 0:
        return
    if depth == 1:
        board.look_ahead()

    moves = next_moves(board)

    for i, move in enumerate(moves):
        # if space to make a move, makes a move
        if move.board[i] == 0:
            move.go_for_la(i)
        else:
            move = 9

    for i, move in enumerate(moves):
        if isinstance(move, Board):
            get_best_move(board, depth - 1)


def print_space(board: Board, column: int, row: int) -> str:
    '''
    convert a space to a string (for display)

    Args:
        column (int): _description_
        row (int): _description_

    Returns:
        str: _description_
    '''

    assert board.spaces[(row * 7) + column] in (-1, 0, 1)

    if board.spaces[(row * 7) + column] == 1:
        return ' X '
    if board.spaces[(row * 7) + column] == -1:
        return ' O '
    return ' * '


def print_board(board: Board) -> None:
    '''
    provide visual printout of board
    '''
    print('\n')
    for row in range(6):
        for column in range(7):
            print(print_space(board, column, row), end=' ')
        print('\n')


def set_select_space_for_la(board: Board, i: int):
    '''
    set_space and select_space for look_ahead function

    Args:
        i (int): _description_
    '''

    j = 0
    while board.spaces[((j + 1) * 7) + i] == 0:
        j += 1
        if j == 5:
            break
    board.spaces[(j * 7) + i] = current_player(board)


def reset_board(board: Board) -> None:
    '''
    _summary_
    '''
    board.spaces = np.zeros(42, int)


def get_valid_moves(board: Board) -> list[int]:
    '''
    returns list of all squares where can_place is True

    Returns:
        list: valid move options
    '''
    valid_moves = []
    for i in range(42):
        if can_place(board, i):
            valid_moves.append(i)
    return valid_moves


def can_place(board: Board, space: int) -> bool:
    '''
    check if legal move can be made at space

    Args:
        space (int): location of space

    Returns:
        bool: True if space is legal move option
    '''
    assert (-1 < space < 42), 'space does not exist; choose between 0-41'
    if not board.spaces[space] == 0:
        return False
    if 34 < space < 42:
        return True
    if board.spaces[space + 7] == 0:
        return False
    return True


def select_space(board: Board, column: int) -> int:
    '''
    select space to play

    Args:
        column (int): column

    Returns:
        int: space to place piece in
    '''
    assert (-1 < column < 7), 'columns are numbered 0-6'
    assert (board.spaces[column] == 0), 'this column is full'
    row = 0
    while board.spaces[((row + 1) * 7) + column] == 0:
        row += 1
        if row == 5:
            break
    return (row * 7) + column


def set_space(board: Board, space: int, value: int) -> None:
    '''
    set space by index

    Args:
        space (int): _description_
        value (int): _description_
    '''
    assert (-1 < space < 42), 'space out of bounds'
    board.spaces[space] = value


def set_space_by_column(board: Board, i: int, value) -> None:
    '''
    set space by column

    Args:
        i (int): column
        value (_type_): _description_
    '''
    set_space(board, select_space(board, i), value)


def set_space_by_coordinates(board: Board, column: int, row: int, value: int) -> None:
    '''
    set space by coordinates

    Args:
        column (int): column
        row (int): row
        value (int): _description_
    '''
    assert (-1 < column < 7), 'i is out of bounds'
    assert (-1 < row < 6), 'j is out of bounds'
    board.spaces[(row * 7) + column] = value


def current_player(board: Board) -> int:
    '''
    compute whose turn it is based on the existing turn
    '''
    turn_sum = 0
    for space in board.spaces:
        turn_sum += space
    assert turn_sum in (1, 0)
    if turn_sum == 0:
        return -1
    return turn_sum


def next_moves(board: Board) -> list[Board]:
    '''
    _summary_

    Returns:
        _type_: _description_
    '''
    return [
        copy_board(board),
        copy_board(board),
        copy_board(board),
        copy_board(board),
        copy_board(board),
        copy_board(board),
        copy_board(board),
    ]


def copy_board(board: Board) -> Board:
    '''
    _summary_

    Returns:
        _type_: _description_
    '''
    board_copy = Board()
    board_copy.spaces = np.array([list(board.spaces)])
    return board_copy


def minimax(board: Board, depth: int, original_depth: int, alpha, beta):
    '''
    this should create boards and analyze them

    Args:
        depth (int): _description_
        original_depth (int): _description_
        alpha (_type_): _description_
        beta (_type_): _description_

    Returns:
        _type_: _description_
    '''
    if depth == 0:
        return board

    moves = next_moves(board)
    best_move = Board()

    if current_player(board) == 1:
        max_eval = -np.inf
        for i in range(7):
            if moves[i].board[i] == 0:
                moves[i].go_for_la(i)
                move = moves[i].minimax(depth - 1, original_depth, alpha, beta)
                # max() can't run on all potential moves at once because
                # the number of potential moves will very depending on
                # whether one or more columns are full
                if move.heuristic > max_eval:
                    max_eval = move.heuristic
                    best_move = move
                    best_column = i
                if move.heuristic > alpha:
                    alpha = move.heuristic
                    if beta <= alpha:
                        break
    else:
        min_eval = np.inf
        for i in range(7):
            if moves[i].board[i] == 0:
                moves[i].go_for_la(i)
                move = moves[i].minimax(depth - 1, original_depth, alpha, beta)
                if move.heuristic < min_eval:
                    min_eval = move.heuristic
                    best_move = move
                    best_column = i
                if move.heuristic < beta:
                    beta = move.heuristic
                    if beta <= alpha:
                        break

    if depth == original_depth:
        return best_column
    return best_move


def pre_alpha_beta(board: Board, depth: int, original_depth: int):
    '''
    _summary_

    Args:
        depth (_type_): _description_
        original_depth (_type_): _description_

    Returns:
        _type_: _description_
    '''
    if depth == 0:
        return board

    moves = next_moves(board)
    best_move = Board()

    if current_player(board) == 1:
        max_eval = -np.inf
        for i in range(7):
            if moves[i].board[i] == 0:
                moves[i].go_for_la(i)
                move = moves[i].pre_alpha_beta(depth - 1, original_depth)
                # max() can't run on all potential moves at once because
                # the number of potential moves will very depending on
                # whether one or more columns are full
                if move.heuristic > max_eval:
                    max_eval = move.heuristic
                    best_move = move
                    best_column = i
    else:
        min_eval = np.inf
        for i in range(7):
            if moves[i].board[i] == 0:
                moves[i].go_for_la(i)
                move = moves[i].pre_alpha_beta(depth - 1, original_depth)
                if move.heuristic < min_eval:
                    min_eval = move.heuristic
                    best_move = move
                    best_column = i

    if depth == original_depth:
        return best_column
    return best_move
