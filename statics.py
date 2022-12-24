'''
contains statics
'''

import numpy as np
from board import Board


def get_next_moves(board: Board):
    '''
    _summary_

    Returns:
        _type_: _description_
    '''
    local_next_moves = board.next_moves()
    for i in range(7):
        # if space to make a move, # makes a move
        if local_next_moves[i].board[i] == 0:
            local_next_moves[i].go_for_la(i)
        else:
            local_next_moves[i] = 9
    return local_next_moves


def get_best_move(board: Board, depth: int):
    '''
    _summary_

    Args:
        depth (_type_): _description_
    '''
    if depth == 0 or board.result != 0:
        return
    if depth == 1:
        board.look_ahead()
    local_next_moves = board.local_next_moves()
    for i in range(7):
        # if space to make a move, makes a move
        if local_next_moves[i].board[i] == 0:
            local_next_moves[i].go_for_la(i)
        else:
            local_next_moves[i] = 9
    for i in range(7):
        if isinstance(local_next_moves[i], Game):
            board.get_best_move(depth - 1)


def set_select_space_for_la(board: Board, i: int):
    '''
    set_space and select_space for look_ahead function

    Args:
        i (int): _description_
    '''
    j = 0
    while self.board[((j + 1) * 7) + i] == 0:
        j += 1
        if j == 5:
            break
    self.board[(j * 7) + i] = self.turn


def next_moves(self) -> list[Board]:
    '''
    _summary_

    Returns:
        _type_: _description_
    '''
    return [
        self.copy_self(),
        self.copy_self(),
        self.copy_self(),
        self.copy_self(),
        self.copy_self(),
        self.copy_self(),
        self.copy_self()
    ]


def minimax(self, depth: int, original_depth: int, alpha, beta):
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
    if depth == 0 or self.result != 0:
        return self

    if self.turn == 1:
        max_eval = -np.inf
        local_next_moves = self.local_next_moves()
        best_move = Game()
        for i in range(7):
            if local_next_moves[i].board[i] == 0:
                local_next_moves[i].go_for_la(i)
                move = local_next_moves[i].minimax(depth - 1, original_depth, alpha, beta)
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
        if depth == original_depth:
            return best_column
        return best_move

    min_eval = np.inf
    local_next_moves = self.local_next_moves()
    best_move = Game()
    for i in range(7):
        if local_next_moves[i].board[i] == 0:
            local_next_moves[i].go_for_la(i)
            move = local_next_moves[i].minimax(depth - 1, original_depth, alpha, beta)
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


def pre_alpha_beta(self, depth: int, original_depth: int):
    '''
    _summary_

    Args:
        depth (_type_): _description_
        original_depth (_type_): _description_

    Returns:
        _type_: _description_
    '''
    if ((depth == 0) or (self.result != 0)):
        return self
    if self.turn == 1:
        max_eval = -np.inf
        local_next_moves = self.local_next_moves()
        best_move = Game()
        for i in range(7):
            if local_next_moves[i].board[i] == 0:
                local_next_moves[i].go_for_la(i)
                move = local_next_moves[i].pre_alpha_beta(depth - 1, original_depth)
                # max() can't run on all potential moves at once because
                # the number of potential moves will very depending on
                # whether one or more columns are full
                if move.heuristic > max_eval:
                    max_eval = move.heuristic
                    best_move = move
                    best_column = i
        if depth == original_depth:
            return best_column
        return best_move

    min_eval = np.inf
    local_next_moves = self.local_next_moves()
    best_move = Game()
    for i in range(7):
        if local_next_moves[i].board[i] == 0:
            local_next_moves[i].go_for_la(i)
            move = local_next_moves[i].pre_alpha_beta(depth - 1, original_depth)
            if move.heuristic < min_eval:
                min_eval = move.heuristic
                best_move = move
                best_column = i
    if depth == original_depth:
        return best_column
    return best_move
