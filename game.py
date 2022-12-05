'''
contains game class
'''

import numpy as np


class Game:
    '''
    tictactoe game
    '''

    # SETUP

    def __init__(self):
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

        # the board is a 7 x 6, seven being the horizontal length
        # the indicies begin in the top left corner, and run horizontally
        # to the right, like you would read a sentence, so,
        # mapping the array to the board squares:
        #
        #
        #            0i 1i 2i 3i 4i 5i 6i
        #
        #
        #     0j     0  1  2  3  4  5  6
        #     1j     7  8  9  10 11 12 13
        #     2j     14 15 16 17 18 19 20
        #     3j     21 22 23 24 25 26 27
        #     4j     28 29 30 31 32 33 34
        #     5j     35 36 37 38 39 40 41
        #
        #

        self.board = np.zeros(42, int)
        self.heuristic = 0
        # what column was the most recent piece placed in?
        # must be between 0 and 6, inclusive
        self.last_move = 7
        self.number_of_moves = 0

    def reset_game(self):
        '''
        reset the game
        '''
        self.print_board()
        self.turn = 1
        self.result = 0
        self.board = np.zeros(42, int)
        self.heuristic = 0

    def select_space(self, i: int) -> int:
        '''
        select space to play

        Args:
            i (int): column

        Returns:
            int: column to place piece in
        '''
        assert (-1 < i < 7), 'columns are numbered 0-6'
        assert (self.board[i] == 0), 'this column is full'
        j = 0
        while self.board[((j + 1) * 7) + i] == 0:
            j += 1
            if j == 5:
                break
        return (j * 7) + i

    def set_space(self, space: int, value):
        '''
        set space by index
d
        Args:
            space (int): _description_
            value (_type_): _description_
        '''
        assert (-1 < space < 42), 'space is out of bounds'
        self.board[space] = value

    def set_select_space_for_la(self, i: int):
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

    def set_space_i(self, i: int, value):
        '''
        set space by column

        Args:
            i (int): column
            value (_type_): _description_
        '''
        self.set_space(self.select_space(i), value)

    def set_space_i_j(self, i: int, j: int, value):
        '''
        set space by coordinates

        Args:
            i (int): column
            j (int): row
            value (_type_): _description_
        '''
        assert (-1 < i < 7), 'i is out of bounds'
        assert (-1 < j < 6), 'j is out of bounds'
        self.board[(j * 7) + i] = value
        self.print_board()

    def space_to_string(self, i: int, j: int):
        '''
        _summary_

        Args:
            i (_type_): _description_
            j (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if self.board[(j * 7) + i] == 0:
            return ' 0 '
        if self.board[(j * 7) + i] == 1:
            return ' 1 '
        if self.board[(j * 7) + i] == -1:
            return '-1 '

    def print_board(self):
        '''
        provide visual printout of board
        '''
        print('\n')
        for j in range(6):
            for i in range(7):
                print(self.space_to_string(i, j), end=' ')
            print('\n')

    # GAMEPLAY

    def can_place(self, space: int) -> bool:
        '''
        check if legal move can be made at space

        Args:
            space (int): location of space

        Returns:
            bool: True if space is legal move option
        '''
        assert (-1 < space < 42), 'space does not exist; choose between 0-41'
        if not self.board[space] == 0:
            return False
        if 34 < space < 42:
            return True
        if self.board[space + 7] == 0:
            return False
        return True

    def get_valid_moves(self) -> list:
        '''
        returns list of all squares where can_place is True

        Returns:
            list: valid move options
        '''
        valid_moves = []
        for i in range(42):
            if self.can_place(i):
                valid_moves.append(i)
        return valid_moves

    def display_valid_moves(self):
        '''
        print visual display of the board and all legal moves
        '''
        valid_moves = self.copy_self()
        # for j in range(6):
        #     for i in range(7):
        #         if self.can_place(i):
        #             valid_moves[(j * 7) + i] = 5
        valid_moves.print_board()

    def update_result(self):
        '''
        vital function that updates self.result. This function works!
        '''
        for j in range(6):
            for i in range(7):
                # check horizontal wins
                if (i < 4
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[(j * 7) + i + 1]
                        == self.board[(j * 7) + i + 2]
                        == self.board[(j * 7) + i + 3])):
                    self.result = self.board[(j * 7) + i]
                    return
                # check downwards diagonal wins
                if (i < 4 and j < 3
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j + 1) * 7) + i + 1]
                        == self.board[((j + 2) * 7) + i + 2]
                        == self.board[((j + 3) * 7) + i + 3])):
                    self.result = self.board[(j * 7) + i]
                    return
                # check upwards diagonal wins
                if (i < 4 and j > 2
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j - 1) * 7) + i + 1]
                        == self.board[((j - 2) * 7) + i + 2]
                        == self.board[((j - 3) * 7) + i + 3])):
                    self.result = self.board[(j * 7) + i]
                    return
                # check vertical wins
                if (j < 3
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j + 1) * 7) + i]
                        == self.board[((j + 2) * 7) + i]
                        == self.board[((j + 3) * 7) + i])):
                    self.result = self.board[(j * 7) + i]
                    return
        # if no wins are found, self.result = 0is set to 0.
        # This could be useful if I decide to integrate move takebacks

        # check draw (i.e. is the board full)
        for j in range(6):
            for i in range(7):
                if self.board[(j * 7) + i] == 0:
                    return
        self.result = 3

    def display_result(self):
        '''
        vital function that explains result status
        '''
        if self.result == 1:
            print('Player 1 wins!')
        elif self.result == -1:
            print('Player -1 wins!')
        elif self.result == 3:
            print('This game is a draw!')
        elif self.result == 0:
            print('This game remains in progress')
        else:
            print('error: result has been set to an invalid value')

    def why_cant_place(self, space: int):
        '''
        debugging function that prints why you can't place on space

        Args:
            space (_type_): _description_
        '''
        if self.can_place(space):
            print('you can place here!')
        else:
            if space != 0:
                print('this space is occupied')
            if space + 7 == 0:
                print('this space lies above an empty space; piece will drop')

    # INTELLIGENCE
    # to do:
        # heuristic function -> rates positions
        # minimax function -> searches all possible moves to specified depth
        #                     applies heuristic function
        #                     works backward to create best position,
        #                     assuming opponent perfect play
        # alpha-beta function -> I'll have to re-read up on this

    def update_heuristic(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''

        self.heuristic = 0
        # player 1 will earn positive points
        # player 2 will earn negative points

        # Wins

        for j in range(6):
            for i in range(7):

                # check horizontal wins
                if (i < 4
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[(j * 7) + i + 1]
                        == self.board[(j * 7) + i + 2]
                        == self.board[(j * 7) + i + 3])):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

                # check downwards diagonal wins
                if (i < 4 and j < 3
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j + 1) * 7) + i + 1]
                        == self.board[((j + 2) * 7) + i + 2]
                        == self.board[((j + 3) * 7) + i + 3])):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

                # check upwards diagonal wins
                if (i < 4 and j > 2
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j - 1) * 7) + i + 1]
                        == self.board[((j - 2) * 7) + i + 2]
                        == self.board[((j - 3) * 7) + i + 3])):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

                # check vertical wins
                if ((j < 3)
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j + 1) * 7) + i]
                        == self.board[((j + 2) * 7) + i]
                        == self.board[((j + 3) * 7) + i])):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

            # Verticals

                # two vertical with an empty space on top
                if (1 < j < 6
                    and (self.board[(j * 7) + i] != 0)
                    and (
                        self.board[(j * 7) + i]
                        == self.board[((j - 1) * 7) + i])
                    and (self.board[((j - 2) * 7) + i] == 0)):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic += self.turn
                    else:
                        self.heuristic -= self.turn

                # three vertical with an empty space on top
                if (2 < j < 6
                    and (self.board[(j * 7) + i] != 0)
                    and (self.board[(j * 7) + i]
                        == self.board[((j - 1) * 7) + i]
                        == self.board[((j - 2) * 7) + i])
                    and (self.board[((j - 3) * 7) + i] == 0)):
                    if (self.board[(j * 7) + i] == self.turn
                    and self.can_place(((j - 3) * 7) + i)
                    ):
                        self.heuristic += 1000 * self.turn
                    elif (self.board[(j * 7) + i] == self.turn
                    # and not self.can_place(the empty space)
                    ):
                        self.heuristic += 7 * self.turn
                    else:
                    # if the player who isn't about to make a move has the
                    # advantago_us formation
                        self.heuristic -= 7 * self.turn

            # Horizontals and diagonals

                # horizontals
                if i < 4:
                    if self.board[(j * 7) + i] != 0:
                        if (
                        # 1110
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 2])
                         and (0
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1101
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 2])
                                   )
                        # 1011
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 2]
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 1])
                                   )
                        ):
                            # each configuration will have one empty space, so
                            # only one of the following IF's OR conditions can
                            # be true. the others will be checking already
                            # filled spaceswhat those spaces are will depend on
                            # which OR in the previous IF condition was true
                            if ((self.board[(j * 7) + i] == self.turn)
                             and (
                                 self.can_place((j * 7) + i + 1)
                              or self.can_place((j * 7) + i + 2)
                              or self.can_place((j * 7) + i + 3)
                                       )
                            ):
                                self.heuristic += 1000 * self.turn
                            elif (self.board[(j * 7) + i] == self.turn
                            # and not self.can_place(the empty space)
                            ):
                                self.heuristic += 7 * self.turn
                            else:
                            # if the player who isn't about to make a move has
                            # the advantago_us formation
                                self.heuristic -= 7 * self.turn
                        if (
                        # 1100
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 1])
                         and (0
                          == self.board[(j * 7) + i + 2]
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1010
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 2])
                         and (0
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1001
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 2])
                                   )
                        ):
                            if self.board[(j * 7) + i] == self.turn:
                                self.heuristic += self.turn
                            else:
                                self.heuristic -= self.turn
                    else:
                        if self.board[(j * 7) + i + 1] != 0:
                            # 0111
                            if (self.board[(j * 7) + i + 1]
                             == self.board[(j * 7) + i + 2]
                             == self.board[(j * 7) + i + 3]
                            ):
                                if ((self.board[(j * 7) + i + 1] == self.turn)
                                and (self.can_place((j * 7) + i))
                                ):
                                    self.heuristic += 1000 * self.turn
                                elif (self.board[(j * 7) + i + 1] == self.turn
                                # and not self.can_place(the empty space)
                                ):
                                    self.heuristic += 7 * self.turn
                                else:
                                # if the player who isn't about to make a move
                                # has the advantago_us formation
                                    self.heuristic -= 7 * self.turn
                            if (
                            # 0110
                                      (
                                (self.board[(j * 7) + i + 1]
                              == self.board[(j * 7) + i + 2])
                             and (0
                              == self.board[(j * 7) + i + 3])
                                       )
                            # 0101
                            or (
                                (self.board[(j * 7) + i + 1]
                              == self.board[(j * 7) + i + 3])
                             and (0
                              == self.board[(j * 7) + i + 2])
                                       )
                            ):
                                if self.board[(j * 7) + i + 1] == self.turn:
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                        else:
                            # 0011
                            if ((self.board[(j * 7) + i + 2] != 0)
                            and (
                                 self.board[(j * 7) + i + 2]
                              == self.board[(j * 7) + i + 3]
                                       )
                            ):
                                if self.board[(j * 7) + i + 2] == self.turn:
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn

                # upwards diagonals
                if i < 4 and j > 2:
                    if self.board[(j * 7) + i] != 0:
                        if (
                        # 1110
                                   (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 2) * 7) + i + 2])
                         and (0
                          == self.board[((j - 3) * 7) + i + 3])
                                    )
                        # 1101
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0
                          == self.board[((j - 2) * 7) + i + 2])
                                   )
                        # 1011
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 2) * 7) + i + 2]
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0
                          == self.board[((j - 1) * 7) + i + 1])
                                   )
                        ):
                            # each scenario will have an empty space, so only
                            # 1 of the following IF's OR conditions can be true
                            # the others will be checking already-filled spaces
                            # what those spaces are will depend on which OR in
                            # the previous IF condition was true
                            if ((self.board[(j * 7) + i] == self.turn)
                             and (
                                 self.can_place(((j - 3) * 7) + i + 3)
                              or self.can_place(((j - 2) * 7) + i + 2)
                              or self.can_place(((j - 1) * 7) + i + 1)
                                      )
                            ):
                                self.heuristic += 1000 * self.turn
                            elif (self.board[(j * 7) + i] == self.turn
                            # and not self.can_place(the empty space)
                            ):
                                self.heuristic += 7 * self.turn
                            else:
                            # if the player who isn't about to make a move has
                            # the advantago_us formation
                                self.heuristic -= 7 * self.turn
                        if (
                        # 1100
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 1) * 7) + i + 1])
                         and (0
                          == self.board[((j - 2) * 7) + i + 2]
                          == self.board[((j - 3) * 7) + i + 3])
                                   )
                        # 1010
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 2) * 7) + i + 2])
                         and (0
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 3) * 7) + i + 3])
                                   )
                        # 1001
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 2) * 7) + i + 2])
                                   )
                        ):
                            if self.board[(j * 7) + i] == self.turn:
                                self.heuristic += self.turn
                            else:
                                self.heuristic -= self.turn
                    else:
                        if self.board[((j - 1) * 7) + i + 1] != 0:
                            # 0111
                            if (self.board[((j - 1) * 7) + i + 1]
                              == self.board[((j - 2) * 7) + i + 2]
                              == self.board[((j - 3) * 7) + i + 3]
                            ):
                                if ((self.board[((j - 1) * 7) + i + 1] == self.turn)
                                and (self.can_place((j * 7) + i))
                                ):
                                    self.heuristic += 1000 * self.turn
                                elif (self.board[((j - 1) * 7) + i + 1] == self.turn
                                # and not self.can_place(the empty space)
                                ):
                                    self.heuristic += 7 * self.turn
                                else:
                                # if the player who isn't about to make a move
                                # has the advantago_us formation
                                    self.heuristic -= 7 * self.turn
                            if (
                            # 0110
                                      (
                                (self.board[((j - 1) * 7) + i + 1]
                              == self.board[((j - 2) * 7) + i + 2])
                             and (0
                              == self.board[((j - 3) * 7) + i + 3])
                                       )
                            # 0101
                            or (
                                (self.board[((j - 1) * 7) + i + 1]
                              == self.board[((j - 3) * 7) + i + 3])
                             and (0
                              == self.board[((j - 2) * 7) + i + 2])
                                       )
                            ):
                                if self.board[((j - 1) * 7) + i + 1] == self.turn:
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                        else:
                            # 0011
                            if ((self.board[((j - 2) * 7) + i + 2] != 0)
                            and (
                                 self.board[((j - 2) * 7) + i + 2]
                              == self.board[((j - 3) * 7) + i + 3]
                                       )
                            ):
                                if self.board[((j - 2) * 7) + i + 2] == self.turn:
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn

                # downwards diagonals
                if i < 4 and j < 3:
                    if self.board[(j * 7) + i] != 0:
                        if (
                        # 1110
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 2) * 7) + i + 2])
                         and (0
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1101
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 3) * 7) + i + 3])
                         and (0
                          == self.board[((j + 2) * 7) + i + 2])
                                   )
                        # 1011
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 2) * 7) + i + 2]
                          == self.board[((j + 3) * 7) + i + 3])
                         and (0
                          == self.board[((j + 1) * 7) + i + 1])
                                   )
                        ):
                            # each configuration will have one empty space, so only
                            # one of the following IF's OR conditions can be true
                            # the others will be checking already-filled spaces
                            # what those spaces are will depend on which OR in
                            # the previous IF condition was true
                            if ((self.board[(j * 7) + i] == self.turn)
                             and (
                                 self.can_place(((j + 3) * 7) + i + 3)
                              or self.can_place(((j + 2) * 7) + i + 2)
                              or self.can_place(((j + 1) * 7) + i + 1)
                                        )
                            ):
                                self.heuristic += 1000 * self.turn
                            elif (self.board[(j * 7) + i] == self.turn
                            # and not self.can_place(the empty space)
                            ):
                                self.heuristic += 7 * self.turn
                            else:
                            # if the player who isn't about to make a move has
                            # the advantago_us formation
                                self.heuristic -= 7 * self.turn
                        if (
                        # 1100
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 1) * 7) + i + 1])
                         and (0
                          == self.board[((j + 2) * 7) + i + 2]
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1010
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 2) * 7) + i + 2])
                         and (0
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1001
                        or (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 3) * 7) + i + 3])
                         and (0
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 2) * 7) + i + 2])
                                   )
                        ):
                            if self.board[(j * 7) + i] == self.turn:
                                self.heuristic += self.turn
                            else:
                                self.heuristic -= self.turn
                    else:
                        if self.board[((j + 1) * 7) + i + 1] != 0:
                            # 0111
                            if (self.board[((j + 1) * 7) + i + 1]
                             == self.board[((j + 2) * 7) + i + 2]
                             == self.board[((j + 3) * 7) + i + 3]
                            ):
                                if ((self.board[((j + 1) * 7) + i + 1] == self.turn)
                                and (self.can_place((j * 7) + i))
                                ):
                                    self.heuristic += (1000 * self.turn)
                                elif (self.board[((j + 1) * 7) + i + 1] == self.turn
                                # and not self.can_place(the empty space)
                                ):
                                    self.heuristic += 7 * self.turn
                                else:
                                # if the player who isn't about to make a move
                                # has the advantago_us formation
                                    self.heuristic -= 7 * self.turn
                            if (
                            # 0110
                                      (
                                (self.board[((j + 1) * 7) + i + 1]
                              == self.board[((j + 2) * 7) + i + 2])
                            and (self.board[((j + 3) * 7) + i + 3])
                                       )
                            # 0101
                            or (
                                (self.board[((j + 1) * 7) + i + 1]
                              == self.board[((j + 3) * 7) + i + 3])
                            and (0
                              == self.board[((j + 2) * 7) + i + 2])
                                       )
                            ):
                                if self.board[((j + 1) * 7) + i + 1] == self.turn:
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                        else:
                            # 0011
                            if (
                                (self.board[((j + 2) * 7) + i + 2] != 0)
                            and (
                                 self.board[((j + 2) * 7) + i + 2]
                              == self.board[((j + 3) * 7) + i + 3]
                                       )
                            ):
                                if self.board[((j + 2) * 7) + i + 2] == self.turn:
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn

        # returns heuristic evaluation of position
        # the larger the number, the better the position for player 1
        # the smaller the number, the better the position for player -1
        return self.heuristic

    def display_heuristic(self):
        '''
        _summary_
        '''
        if self.heuristic == 100000:
            print('heuristic: infinity')
        elif self.heuristic == -100000:
            print('heuristic: -infinity')
        else:
            print('heuristic: ' + str(self.heuristic))

    def copy_self(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        copy = Game()
        copy.board = np.array([i for i in self.board])
        copy.turn = self.turn
        copy.result = self.result
        copy.heuristic = self.heuristic
        return copy

    def get_next_moves(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        next_moves = self.next_moves()
        for i in range(7):
            # if space to make a move, # makes a move
            if next_moves[i].board[i] == 0:
                next_moves[i].go_for_la(i)
            else:
                next_moves[i] = 9
        return next_moves

    def next_moves(self):
        return [
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self()
        ]

    def get_best_move(self, depth: int):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        if depth == 0 or self.result != 0:
            return
        if depth == 1:
            self.look_ahead()
        next_moves = self.next_moves()
        for i in range(7):
            # if space to make a move, makes a move
            if next_moves[i].board[i] == 0:
                next_moves[i].go_for_la(i)
            else:
                next_moves[i] = 9
        for i in range(7):
            if isinstance(next_moves[i], Game):
                self.get_best_move(depth - 1)

    def minimax(self, depth: int, original_depth: int, alpha, beta):
        '''
        _summary_

        Args:
            depth (_type_): _description_
            original_depth (_type_): _description_
            alpha (_type_): _description_
            beta (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if ((depth == 0) or (self.result != 0)):
            return self
        if self.turn == 1:
            max_eval = -np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].minimax(depth - 1, original_depth, alpha, beta)
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
            else:
                return best_move
        else:
            min_eval = np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].minimax(depth - 1, original_depth, alpha, beta)
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
            else:
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
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].pre_alpha_beta(depth - 1, original_depth)
                    # max() can't run on all potential moves at once because
                    # the number of potential moves will very depending on
                    # whether one or more columns are full
                    if move.heuristic > max_eval:
                        max_eval = move.heuristic
                        best_move = move
                        best_column = i
            if depth == original_depth:
                return best_column
            else:
                return best_move
        else:
            min_eval = np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].pre_alpha_beta(depth - 1, original_depth)
                    if move.heuristic < min_eval:
                        min_eval = move.heuristic
                        best_move = move
                        best_column = i
            if depth == original_depth:
                return best_column
            else:
                return best_move

    def look_ahead(self):
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
        possible_moves = self.next_moves()
        # sets start to correspond to something valid
        # creates an initial best, which will be updated
        # each time it is compared with another move
        # plays move where move plays are valid,
        # marks columns where plays are not valid
        for i in range(7):
            if possible_moves[i].board[i] == 0:
                possible_moves[i].go_for_la(i)
                if self.turn == 1:
                    best_heuristic = -np.inf
                    if possible_moves[i].heuristic > best_heuristic:
                        best_heuristic = possible_moves[i]
                        best_column = i
                else:
                    best_heuristic = np.inf
                    if possible_moves[i].heuristic < best_heuristic:
                        best_heuristic = possible_moves[i]
                        best_column = i
        # best_move, the position, exists for comparison against other positions
        # best_column, the column, exists to be returned
        # after all comparisons are completed
        return best_column

    def is_first_turn(self):
        '''
        checks to see if both players have made at least one move
        if not, returns True

        Returns:
            _type_: _description_
        '''
        one_move = False
        two_moves = False
        for i in range(42):
            if self.board[i] != 0:
                if not one_move:
                    two_moves = True
                else:
                    one_move = True
        return not two_moves

    def play_first_turn(self):
        '''
        plays a random non-side move for a first turn
        '''
        self.go_u(np.random.randint(1, 5))

    def play_first_turns(self):
        '''
        plays two random non-side moves. designed to start games where both sides
        are played by robots
        '''
        self.go_u(np.random.randint(1, 5))
        self.go_u(np.random.randint(1, 5))

    def display_info(self):
        '''
        _summary_
        '''
        self.display_result()
        self.print_board()
        self.display_heuristic()

    # instanceof go

    def go_u(self, i: int, verbose=True):
        '''
        human plays one turn; computer displays result and information about game

        Args:
            i (_type_): _description_
        '''
        assert (self.result == 0), "this game is over! you can't place pieces anymore."
        self.set_space(self.select_space(i), self.turn)
        if self.turn == -1:
            self.number_of_moves += 1
        self.turn = np.negative(self.turn)
        if verbose:
            self.print_board()
        self.update_result()

    def go_pre_ab(self, depth: int):
        '''
        computer plays the pre-alpha-beta minimax recommended turn

        Args:
            depth (_type_): _description_
        '''
        if self.is_first_turn():
            self.play_first_turn()
        else:
            self.go_u(self.pre_alpha_beta(depth, depth))

    def go_for_la(self, i: int):
        '''
        plays one turn for look_ahead function

        Args:
            i (_type_): _description_
        '''
        self.set_select_space_for_la(i)
        self.turn = np.negative(self.turn)
        self.update_result()
        self.update_heuristic()

    def play_turn(
        self,
        player: str = 'human',
        turns: int = 1,
        depth: int = 4,
        print_turn: bool = True
    ):
        '''
        play a turn in tictactoe

        Args:
            player (str, optional): _description_. Defaults to 'human'.
            turns (int, optional): _description_. Defaults to 1.
            depth (int, optional): _description_. Defaults to 4.
        '''
        if player == 'human':
            print('input an integer between 0 and 6, inclusive')
            column = int(input('which column do you choose to place your piece in? '))
            while column not in (0, 1, 2, 3, 4, 5, 6):
                column = int(input('that was not an integer between 0 and 6. try again: '))
            self.go_u(column, verbose=print_turn)
        elif player == 'random':
            for _ in range(turns):
                if self.result != 0:
                    self.reset_game()
                    break
                column = np.random.randint(0, 6)
                while self.board[column] != 0:
                    column = np.random.randint(0, 6)
                self.go_u(column, verbose=print_turn)
        elif player == 'heuristic':
            for _ in range(turns):
                if self.result != 0:
                    self.reset_game()
                    break
                if self.is_first_turn():
                    self.play_first_turn()
                else:
                    if self.is_first_turn():
                        self.play_first_turn()
                    else:
                        self.go_u(self.look_ahead(), verbose=print_turn)
        elif player == 'minimax':
            for _ in range(turns):
                if self.result != 0:
                    self.reset_game()
                    break
                if self.is_first_turn():
                    self.play_first_turn()
                else:
                    assert (depth > 0), 'minimax cannot search to a depth less than one'
                    if self.is_first_turn():
                        self.play_first_turn()
                    else:
                        self.go_u(self.minimax(depth, depth, -np.inf, np.inf), verbose=print_turn)

    # instanceof matchup

    def play_game(
        self,
        player_1: str = 'human',
        player_2: str = 'human',
        depth_1: int = 5,
        depth_2: int = 5,
        player_1_name: str = 'player_1',
        player_2_name: str = 'player_2',
        print_game: bool = True,
        verbose: bool = False
    ):
        '''
        play a game of tictactoe

        Args:
            player_1 (str, optional): player 1 type. Defaults to 'minimax'.
            player_2 (str, optional): player 2 type. Defaults to 'minimax'.
            depth_1 (int, optional): player 1 search depth. Defaults to 5.
            depth_2 (int, optional): player 2 search depth. Defaults to 5.
        '''

        # setup
        self.reset_game()
        self.play_first_turns()

        # play game
        while self.result == 0:
            self.play_turn(player=player_1, depth=depth_1, print_turn=verbose)
            if self.result != 0:
                break
            self.play_turn(player=player_2, depth=depth_2, print_turn=verbose)

        # print result
        if print_game:
            if self.result == 1:
                print(f"{player_1_name} beat {player_2_name} in {self.number_of_moves} moves")
            elif self.result == -1:
                print(f"{player_2_name} beat {player_1_name} in {self.number_of_moves} moves")
            elif self.result == 0:
                print(f"{player_1_name} drew with {player_2_name} after {self.number_of_moves} moves")

        print(self.result)
        return self.result
