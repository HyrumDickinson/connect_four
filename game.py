'''
contains game class
'''

import random
import numpy as np
from board import Board
from player import Player
from heuristic import heuristic
from statics import minimax
from board_functions import (
    reset_board,
    next_moves,
    print_board,
    drop_piece_into_column,
    current_player,
)


class Game:
    '''
    game class
    '''
    def __init__(
        self,
        player_1: str = 'human',
        player_2: str = 'human',
        depth_1: int = 5,
        depth_2: int = 5
    ):

        self.player_1 = Player(player_1, True)
        self.player_2 = Player(player_2, False)

        self.player_1.depth = depth_1
        self.player_2.depth = depth_2

        # each player is assigned a number: 1 or -1
        # 0 means that no player has been assigned the value
        # Player_1 goes first

        # whose turn is it?
        # 1   -> player 1
        # -1  -> player -1
        self.turn = 1

        # what is the result of the game?
        # 0   -> undecided
        # 1   -> player 1 win
        # -1  -> player -1 win
        # 3   -> draw
        self.result = 0

        self.move_count = 0
        self.board = Board()

    def play(self, rounds: int = 1) -> None:
        '''
        play the game
        '''
        # play matches
        matches = []
        for _ in range(rounds):

            # reset()
            self.reset()

            # play game
            while heuristic(self.board) not in (np.inf, -np.inf):
                self.play_turn()

            print_board(self.board)
            print(f'terminal heuristic eval: {heuristic(self.board)}')

            # display result
            if self.result == 1:
                print(f"{self.player_1.name} beat {self.player_2.name} in {self.move_count} moves")
            if self.result == -1:
                print(f"{self.player_2.name} beat {self.player_1.name} in {self.move_count} moves")
            if self.result == 0:
                print(f"{self.player_1.name} drew with {self.player_2.name} after {self.move_count} moves")

            matches.append(self.result)

        # analyze results
        player_1_score = 0
        player_2_score = 0
        draw_count = 0
        for match in matches:
            assert match in (1, -1, 3)
            if match == 1:
                player_1_score += 1
            if match == -1:
                player_2_score += 1
            if match == 3:
                draw_count += 1

        print(f'{self.player_1.name} {player_1_score}-{draw_count}-{player_2_score} {self.player_2.name}')

    def play_turn(self) -> None:
        '''
        play a turn in tictactoe

        Args:
            player (str, optional): _description_. Defaults to 'human'.
            turns (int, optional): _description_. Defaults to 1.
            depth (int, optional): _description_. Defaults to 4.
        '''

        if self.turn == 1:
            player = self.player_1
            self.move_count += 1
        else:
            player = self.player_2

        depth = player.depth

        if self.result != 0:
            self.reset()
            return

        if player.strategy == 'human':

            user_input = input(f'\n{player.name}: input a column (between 0 and 6)')

            try:
                column = int(user_input)
            except ValueError:
                column = 8

            while column not in range(7) or self.board.spaces[column] != 0:
                user_input = input('that was not an integer between 0 and 6 or that column is full. try again: ')
                try:
                    column = int(user_input)
                except ValueError:
                    column = 8
            drop_piece_into_column(self.board, column)

        if player.strategy == 'random':
            column = np.random.randint(0, 7)
            while self.board.spaces[column] != 0:
                column = np.random.randint(0, 7)
            drop_piece_into_column(self.board, column)

        if player.strategy == 'heuristic':
            drop_piece_into_column(self.board, self.__look_ahead())

        if player.strategy == 'minimax':
            assert (depth > 0), 'minimax cannot search to a depth less than one'
            drop_piece_into_column(self.board, minimax(self.board, depth, depth, -np.inf, np.inf))

        # update turn
        assert self.turn in (-1, 1)
        self.turn = np.negative(self.turn)

        self.__update_result()

    def reset(self) -> None:
        '''
        reset the game
        '''
        self.turn = 1
        self.result = 0
        self.move_count = 0
        reset_board(self.board)

    def __look_ahead(self) -> int:
        '''
        looks one move ahead and chooses the best move based on heuristic

        Returns:
            int: _description_
        '''

        assert (self.result == 0), 'cannot calculate future moves on a finished game'
        # possible_moves is a 7-index array of games,
        # each index representing the board state if
        # a move is made in the column with the
        # same i-number as the array index
        possible_moves = next_moves(self.board)
        assert isinstance(possible_moves, dict)
        # sets start to correspond to something valid
        # creates an initial best, which will be updated
        # each time it is compared with another move
        # plays move where move plays are valid,
        # marks columns where plays are not valid

        best_heuristic = current_player(self.board) * -np.inf
        best_columns = []
        for column in possible_moves:
            if heuristic(possible_moves[column]) * current_player(self.board) > best_heuristic * current_player(self.board):
                best_heuristic = heuristic(possible_moves[column])
                # overwrite best_column to be set only containing best move
                best_columns = [column]
            elif heuristic(possible_moves[column]) * current_player(self.board) == best_heuristic * current_player(self.board):
                # if move equally good as current best move
                # add move to set of equally best moves
                best_columns.append(column)

        # best_move, the position, exists for comparison against other positions
        # best_column, the column, exists to be returned
        # after all comparisons are completed
        print(f'best_columns are {best_columns}')
        assert isinstance(best_columns, list)
        best_column = random.choice(best_columns)
        print(f'best_column (randomly chosen) is {best_column}')
        return best_column

    def __update_result(self) -> None:
        '''
        vital function that updates self.result. This function works!
        '''
        for row in range(6):
            for column in range(7):

                # check horizontal wins
                if (column < 4
                    and (self.board.spaces[(row * 7) + column] != 0)
                    and (
                        self.board.spaces[(row * 7) + column]
                        == self.board.spaces[(row * 7) + column + 1]
                        == self.board.spaces[(row * 7) + column + 2]
                        == self.board.spaces[(row * 7) + column + 3])):
                    self.result = self.board.spaces[(row * 7) + column]
                    return

                # check downwards diagonal wins
                if (column < 4 and row < 3
                    and (self.board.spaces[(row * 7) + column] != 0)
                    and (
                        self.board.spaces[(row * 7) + column]
                        == self.board.spaces[((row + 1) * 7) + column + 1]
                        == self.board.spaces[((row + 2) * 7) + column + 2]
                        == self.board.spaces[((row + 3) * 7) + column + 3])):
                    self.result = self.board.spaces[(row * 7) + column]
                    return

                # check upwards diagonal wins
                if (column < 4 and row > 2
                    and (self.board.spaces[(row * 7) + column] != 0)
                    and (
                        self.board.spaces[(row * 7) + column]
                        == self.board.spaces[((row - 1) * 7) + column + 1]
                        == self.board.spaces[((row - 2) * 7) + column + 2]
                        == self.board.spaces[((row - 3) * 7) + column + 3])):
                    self.result = self.board.spaces[(row * 7) + column]
                    return

                # check vertical wins
                if (row < 3
                    and (self.board.spaces[(row * 7) + column] != 0)
                    and (
                        self.board.spaces[(row * 7) + column]
                        == self.board.spaces[((row + 1) * 7) + column]
                        == self.board.spaces[((row + 2) * 7) + column]
                        == self.board.spaces[((row + 3) * 7) + column])):
                    self.result = self.board.spaces[(row * 7) + column]
                    return

        # if no wins are found, self.result is set to 0.
        # This could be useful if I decide to integrate move takebacks

        # check draw (i.e. is the board full)
        for row in range(6):
            for column in range(7):
                if self.board.spaces[(row * 7) + column] == 0:
                    return
        self.result = 3
