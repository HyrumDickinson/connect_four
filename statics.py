'''
contains statics
statics are mostly board functions, kept separate from Board to keep Board lightweight
'''

import numpy as np
from board import Board
from heuristic import heuristic
from board_functions import (
    next_moves,
    current_player,
    drop_piece_into_column,
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


# TODO rework minimax
def minimax(board: Board, depth: int, original_depth: int, alpha: int, beta: int) -> Board:
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
