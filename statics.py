'''
contains statics
statics are mostly board functions, kept separate from Board to keep Board lightweight
'''

import random
import numpy as np
from board import Board
from heuristic import heuristic
from board_functions import (
    next_moves,
    current_player,
    drop_piece_into_column,
    print_board,
    copy_board,
)


def get_best_move(board: Board, depth: int) -> None:
    '''
    _summary_

    Args:
        depth (int): _description_
    '''

    if depth == 0:
        return
    if depth == 1:
        board.look_ahead()

    boards = next_moves(board)

    for i, move in enumerate(boards):
        # if space to make a move, makes a move
        if move.spaces[i] == 0:
            drop_piece_into_column(move, i)
        else:
            move = 9

    for i, move in enumerate(boards):
        if isinstance(move, Board):
            get_best_move(board, depth - 1)


def minimax(
    board: Board,
    depth: int = 1,
    original_depth: int = 1,
    alpha: float = -np.inf,
    beta: float = np.inf
):
    '''
    looks one move ahead and returns best move based on heuristic if depth == 1
    else returns heuristic of chosen best move

    Returns:
        int: _description_
    '''

    assert depth > 0, 'searching too far'

    possible_moves = next_moves(board)
    assert isinstance(possible_moves, dict)  # dict[int: Board]
    player = current_player(board)
    best_heuristic = player * -np.inf
    best_columns = []

    for column in possible_moves:

        # recursion or direct heuristic
        if depth == 1:
            score = heuristic(possible_moves[column])
            print(f'heuristic eval: {player} on column {column} for {score}')
        else:
            minimax_tuple = minimax(
                board=possible_moves[column],
                depth=depth - 1,
                original_depth=original_depth,
                alpha=alpha,
                beta=beta
            )
            score = minimax_tuple[1]
            print(f'minimax eval: {player} on column {column} for {score}')

        # overwrite best_column to be set only containing best move
        if score * player > best_heuristic * player:
            best_heuristic = score
            best_columns = [column]

        # if move equally good as current best move
        # add move to set of equally best moves
        elif score * player == best_heuristic * player:
            best_columns.append(column)

    print(f'best_columns are {best_columns} at depth {original_depth - depth}')
    assert isinstance(best_columns, list)
    assert len(best_columns) > 0, 'cannot make move on full board'
    best_column = random.choice(best_columns)
    print(f'best_column (randomly chosen) is {best_column} for {player} for eval of {best_heuristic}')
    if original_depth - depth == 0:
        print('\n')
        printable_copy = copy_board(board)
        drop_piece_into_column(printable_copy, best_column)
        print_board(printable_copy)
    return best_column, best_heuristic


def minimaxx(board: Board, depth: int, original_depth: int, alpha: int, beta: int) -> Board:
    '''
    this should create boards and analyze them

    Args:
        depth (int): _description_
        original_depth (int): _description_
        alpha (int): _description_
        beta (int): _description_

    Returns:
        _type_: _description_
    '''
    if depth == 0:
        return board

    moves = next_moves(board)
    best_move = Board()

    if current_player(board) == 1:
        max_eval = np.inf * current_player(board)
        for mov in moves:

            if mov.spaces[i] == 0:
                drop_piece_into_column(mov, i)
                move = minimax(mov, depth - 1, original_depth, alpha, beta)
                # max() can't run on all potential moves at once because
                # the number of potential moves will very depending on
                # whether one or more columns are full
                if heuristic(move) > max_eval:
                    max_eval = heuristic(move)
                    best_move = move
                    best_column = i
                if heuristic(move) > alpha:
                    alpha = heuristic(move)
                    if beta <= alpha:
                        break
    else:
        min_eval = np.inf * current_player(board)
        for i, mov in enumerate(moves):
            if mov.spaces[i] == 0:
                drop_piece_into_column(mov, i)
                move = minimax(mov, depth - 1, original_depth, alpha, beta)
                if heuristic(move) < min_eval:
                    min_eval = heuristic(move)
                    best_move = move
                    best_column = i
                if heuristic(move) < beta:
                    beta = heuristic(move)
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
            if moves[i].spaces[i] == 0:
                drop_piece_into_column(moves[i], i)
                move = pre_alpha_beta(moves[i], depth - 1, original_depth)
                # max() can't run on all potential moves at once because
                # the number of potential moves will very depending on
                # whether one or more columns are full
                if heuristic(move) > max_eval:
                    max_eval = heuristic(move)
                    best_move = move
                    best_column = i
    else:
        min_eval = np.inf
        for i in range(7):
            if moves[i].spaces[i] == 0:
                drop_piece_into_column(moves[i], i)
                move = pre_alpha_beta(moves[i], depth - 1, original_depth)
                if heuristic(move) < min_eval:
                    min_eval = heuristic(move)
                    best_move = move
                    best_column = i

    if depth == original_depth:
        return best_column
    return best_move
