'''
contains game class
'''

import numpy as np
from board import Board
from player import Player
from heuristic import heuristic
from statics import (
    pre_alpha_beta,
    minimax,
    next_moves,
    set_select_space_for_la,
    reset_board,
    set_space,
    select_space,
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

    def play(self) -> None:
        '''
        play the game
        '''

        # play game
        while heuristic(self.board) not in (np.inf, -np.inf):
            self.play_turn()

        print(f'terminal heuristic eval: {heuristic(self.board)}')

        # display result
        if self.result == 1:
            print(f"{self.player_1.name} beat {self.player_2.name} in {self.move_count} moves")
        if self.result == -1:
            print(f"{self.player_2.name} beat {self.player_1.name} in {self.move_count} moves")
        if self.result == 0:
            print(f"{self.player_1.name} drew with {self.player_2.name} after {self.move_count} moves")

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
        else:
            player = self.player_2

        depth = player.depth

        if self.result != 0:
            self.reset()
            return

        if player.strategy == 'human':
            print('input an integer between 0 and 6')
            column = int(input('choose an column (between 0 and 6)'))
            while column not in (0, 1, 2, 3, 4, 5, 6):
                column = int(input('that was not an integer between 0 and 6. try again: '))
            self.__go_u(column)

        if player.strategy == 'random':
            column = np.random.randint(0, 7)
            while self.board.spaces[column] != 0:
                column = np.random.randint(0, 7)
            self.__go_u(column)

        if player.strategy == 'heuristic':
            self.__go_u(self.__look_ahead())

        if player.strategy == 'minimax':
            assert (depth > 0), 'minimax cannot search to a depth less than one'
            self.__go_u(minimax(self.board, depth, depth, -np.inf, np.inf))

        # update turn
        assert self.turn in (-1, 1)
        self.turn = np.negative(self.turn)

    def reset(self) -> None:
        '''
        reset the game
        '''
        self.turn = 1
        self.result = 0
        reset_board(self.board)

    def __go_u(self, column: int) -> None:
        '''
        human plays one turn; computer displays result and information about game

        Args:
            column (int): _description_
        '''
        assert (self.result == 0), "this game is over! you can't place pieces anymore."
        set_space(self.board, select_space(self.board, column), self.turn)
        if self.turn == -1:
            self.move_count += 1
        self.__update_result()

    def __go_pre_ab(self, depth: int) -> None:
        '''
        computer plays the pre-alpha-beta minimax recommended turn

        Args:
            depth (_type_): _description_
        '''
        if self.__is_first_turn():
            self.__play_first_turn()
        else:
            self.__go_u(pre_alpha_beta(self.board, depth, depth))

    def __go_for_la(self, i: int) -> None:
        '''
        plays one turn for __look_ahead function

        Args:
            i (_type_): _description_
        '''
        set_select_space_for_la(self.board.spaces, i)
        self.turn = np.negative(self.turn)
        self.__update_result()

    def __play_first_turn(self) -> None:
        '''
        plays a random non-side move for a first turn
        '''
        self.__go_u(np.random.randint(1, 5))

    def __play_first_turns(self) -> None:
        '''
        plays two random non-side moves. designed to start games where both sides
        are played by robots
        '''
        for _ in range(2):
            self.__go_u(np.random.randint(1, 5))

    def __is_first_turn(self) -> bool:
        '''
        checks to see if both players have made at least one move
        if not, returns True

        Returns:
            _type_: _description_
        '''
        one_move = False
        two_moves = False
        for i in range(42):
            if self.board.spaces[i] != 0:
                if not one_move:
                    two_moves = True
                else:
                    one_move = True
        return not two_moves

    def __look_ahead(self) -> int:
        '''
        looks one move ahead and chooses the best move based on heuristic

        Returns:
            _type_: _description_
        '''
        assert (self.result == 0), 'cannot calculate future moves on a finished game'
        # possible_moves is a 7-index array of games,
        # each index representing the board state if
        # a move is made in the column with the
        # same i-number as the array index
        possible_moves = next_moves(self.board)
        # sets start to correspond to something valid
        # creates an initial best, which will be updated
        # each time it is compared with another move
        # plays move where move plays are valid,
        # marks columns where plays are not valid
        for i in range(7):
            if possible_moves[i].board[i] == 0:
                self.__go_for_la(i)
                # possible_moves[i].__go_for_la(i)
                if self.turn == 1:
                    best_heuristic = -np.inf
                    if heuristic(possible_moves[i]) > best_heuristic:
                        best_heuristic = possible_moves[i]
                        best_column = i
                else:
                    best_heuristic = np.inf
                    if heuristic(possible_moves[i]) < best_heuristic:
                        best_heuristic = possible_moves[i]
                        best_column = i
        # best_move, the position, exists for comparison against other positions
        # best_column, the column, exists to be returned
        # after all comparisons are completed
        return best_column

    def __update_result(self) -> None:
        '''
        vital function that updates self.result. This function works!
        '''
        for j in range(6):
            for i in range(7):
                # check horizontal wins
                if (i < 4
                    and (self.board.spaces[(j * 7) + i] != 0)
                    and (
                        self.board.spaces[(j * 7) + i]
                        == self.board.spaces[(j * 7) + i + 1]
                        == self.board.spaces[(j * 7) + i + 2]
                        == self.board.spaces[(j * 7) + i + 3])):
                    self.result = self.board.spaces[(j * 7) + i]
                    return
                # check downwards diagonal wins
                if (i < 4 and j < 3
                    and (self.board.spaces[(j * 7) + i] != 0)
                    and (
                        self.board.spaces[(j * 7) + i]
                        == self.board.spaces[((j + 1) * 7) + i + 1]
                        == self.board.spaces[((j + 2) * 7) + i + 2]
                        == self.board.spaces[((j + 3) * 7) + i + 3])):
                    self.result = self.board.spaces[(j * 7) + i]
                    return
                # check upwards diagonal wins
                if (i < 4 and j > 2
                    and (self.board.spaces[(j * 7) + i] != 0)
                    and (
                        self.board.spaces[(j * 7) + i]
                        == self.board.spaces[((j - 1) * 7) + i + 1]
                        == self.board.spaces[((j - 2) * 7) + i + 2]
                        == self.board.spaces[((j - 3) * 7) + i + 3])):
                    self.result = self.board.spaces[(j * 7) + i]
                    return
                # check vertical wins
                if (j < 3
                    and (self.board.spaces[(j * 7) + i] != 0)
                    and (
                        self.board.spaces[(j * 7) + i]
                        == self.board.spaces[((j + 1) * 7) + i]
                        == self.board.spaces[((j + 2) * 7) + i]
                        == self.board.spaces[((j + 3) * 7) + i])):
                    self.result = self.board.spaces[(j * 7) + i]
                    return

        # if no wins are found, self.result is set to 0.
        # This could be useful if I decide to integrate move takebacks

        # check draw (i.e. is the board full)
        for j in range(6):
            for i in range(7):
                if self.board.spaces[(j * 7) + i] == 0:
                    return
        self.result = 3
