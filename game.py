'''
game class
'''

import numpy as np

class Game:
    '''
    tic tac toe game
    '''

    # SETUP

    def __init__(self):
        # each player is assigned a number: 1 or -1
        # 0 means that no player has been assigned the value
        # Player_1 goes first
        self.turn = 1 # whose turn is it?
            # 1   -> player 1
            # -1  -> player -1
        self.result = 0 # what is the result of the game?
            # 0   -> undecided
            # 1   -> player 1 win
            # -1  -> player -1 win
            # 3   -> draw
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
        self.last_move = 7 # what column was the most recent piece placed in?
            # must be between 0 and 6, inclusive
        self.number_of_moves = 0

    # behold the setters and getters
    def get_turn(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        return self.turn
    def set_turn(self, set_turn):
        '''
        _summary_

        Args:
            set_turn (_type_): _description_
        '''
        self.turn = set_turn
    def get_result(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        return self.result
    def set_result(self, set_result):
        '''
        _summary_

        Args:
            set_result (_type_): _description_
        '''
        self.result = set_result
    def get_board(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        return self.board
    def set_board(self, array):
        '''
        _summary_

        Args:
            array (_type_): _description_
        '''
        self.board = np.array(array)
    def reset_game(self):
        '''
        _summary_
        '''
        self.turn = 1
        self.result = 0
        self.board = np.zeros(42, int)
        self.heuristic = 0
    def select_space(self, i):
        '''
        _summary_

        Args:
            i (_type_): _description_

        Returns:
            _type_: _description_
        '''
        assert (-1 < i < 7), 'columns are numbered 0-6'
        assert (self.board[i] == 0), 'this column is full'
        j = 0
        while self.board[((j + 1) * 7) + i] == 0:
            j += 1
            if j == 5:
                break
        return (j * 7) + i # this is the space
        # set space by index
    def set_space(self, space, value):
        '''
        _summary_

        Args:
            space (_type_): _description_
            value (_type_): _description_
        '''
        assert (-1 < space < 42), 'space is out of bounds'
        self.board[space] = value
        # set_space and select_space for look_ahead function
    def set_select_space_for_la(self, i):
        '''
        _summary_

        Args:
            i (_type_): _description_
        '''
        j = 0
        while self.board[((j + 1) * 7) + i] == 0:
            j += 1
            if j == 5:
                break
        self.board[(j * 7) + i] = self.turn
        # set space by column
    def set_space_i(self, i, value):
        '''
        _summary_

        Args:
            i (_type_): _description_
            value (_type_): _description_
        '''
        self.set_space(self.select_space(i), value)
        # set space by coordinates
    def set_space_i_j(self, i, j, value):# set space by coordinates
        '''
        _summary_

        Args:
            i (_type_): _description_
            j (_type_): _description_
            value (_type_): _description_
        '''
        assert (-1 < i < 7), 'i is out of bounds'
        assert (-1 < j < 6), 'j is out of bounds'
        self.board[(j * 7) + i] = value
        self.print_board()
    def space_to_string(self, i, j):
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
    def get_heuristic(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        return self.heuristic
    def set_heuristic(self, set_heuristic):
        '''
        _summary_

        Args:
            set_heuristic (_type_): _description_
        '''
        self.heuristic = set_heuristic

    # print functions in case I need them later
    # printing the board is a bit complicated
    def print_turn(self):
        '''
        _summary_
        '''
        print(self.turn)
    def print_result(self):
        '''
        _summary_
        '''
        print(self.result)
    def print_board(self):
        '''
        _summary_
        '''
        print(' C0  C1  C2  C3  C4  C5  C6')
        for j in range(6):
            for i in range(7):
                print(self.space_to_string(i, j), end=' ')
            print('\n')
    def print_board_string(self):
        '''
        _summary_
        '''
        print(self.board)

    # GAMEPLAY

    # vital function that returns validity of piece placement on space
    def can_place(self, space):
        '''
        _summary_

        Args:
            space (_type_): _description_

        Returns:
            _type_: _description_
        '''
        assert (-1 < space < 42), 'space does not exist; choose between 0-41'
        if not self.board[space] == 0:
            return False
        elif 34 < space < 42:
            return True
        elif self.board[space + 7] == 0:
            return False
        else:
            return True

    # vital function that returns an array of
    # all squares where (can_place == True)
    def get_valid_moves(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        valid_moves = []
        for i in range(42):
            if self.can_place(i):
                valid_moves.append(i)
        return valid_moves

    # debugging function that prints a visual display of the board
    # and all legal moves
    def display_valid_moves(self):
        '''
        _summary_
        '''
        valid_moves = self.copy_self()
        # for j in range(6):
        #     for i in range(7):
        #         if self.can_place(i):
        #             valid_moves[(j * 7) + i] = 5
        valid_moves.print_board()


    # vital function that updates self.result. This function works!
    def update_result(self):
        '''
        _summary_
        '''
        for j in range(6):
            for i in range(7):
                # check horizontal wins
                if ((i < 4)
                and (self.board[(j * 7) + i] != 0)
                and        (
                     self.board[(j * 7) + i]
                  == self.board[(j * 7) + i + 1]
                  == self.board[(j * 7) + i + 2]
                  == self.board[(j * 7) + i + 3]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return
                # check downwards diagonal wins
                if ((i < 4) and (j < 3)
                and (self.board[(j * 7) + i] != 0)
                and        (
                     self.board[(j * 7) + i]
                  == self.board[((j + 1) * 7) + i + 1]
                  == self.board[((j + 2) * 7) + i + 2]
                  == self.board[((j + 3) * 7) + i + 3]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return
                # check upwards diagonal wins
                if ((i < 4) and (j > 2)
                and (self.board[(j * 7) + i] != 0)
                and        (
                     self.board[(j * 7) + i]
                  == self.board[((j - 1) * 7) + i + 1]
                  == self.board[((j - 2) * 7) + i + 2]
                  == self.board[((j - 3) * 7) + i + 3]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return
                # check vertical wins
                if ((j < 3)
                and (self.board[(j * 7) + i] != 0)
                and        (
                     self.board[(j * 7) + i]
                  == self.board[((j + 1) * 7) + i]
                  == self.board[((j + 2) * 7) + i]
                  == self.board[((j + 3) * 7) + i]
                            )
                ):
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

    # vital function that explains result status
    def display_result(self):
        '''
        _summary_
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

    # debugging function that prints why you can't place on space
    def why_cant_place(self, space):
        '''
        _summary_

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


        # make this an independent class?

    def update_heuristic(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''

        self.heuristic = 0
        # player 1 will earn positive points
        # player 2 will earn negative points

        for j in range(6):
            for i in range(7):

            # Wins

                # check horizontal wins
                if ((i < 4)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[(j * 7) + i + 1]
                  == self.board[(j * 7) + i + 2]
                  == self.board[(j * 7) + i + 3]
                           )
                ):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

                # check downwards diagonal wins
                if ((i < 4) and (j < 3)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j + 1) * 7) + i + 1]
                  == self.board[((j + 2) * 7) + i + 2]
                  == self.board[((j + 3) * 7) + i + 3]
                           )
                ):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

                # check upwards diagonal wins
                if ((i < 4) and (j > 2)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j - 1) * 7) + i + 1]
                  == self.board[((j - 2) * 7) + i + 2]
                  == self.board[((j - 3) * 7) + i + 3]
                           )
                ):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

                # check vertical wins
                if ((j < 3)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j + 1) * 7) + i]
                  == self.board[((j + 2) * 7) + i]
                  == self.board[((j + 3) * 7) + i]
                           )
                ):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return

            # Verticals

                # two vertical with an empty space on top
                if ((1 < j < 6)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j - 1) * 7)+ i]
                           )
                and (self.board[((j - 2) * 7) + i] == 0)
                ):
                    if self.board[(j * 7) + i] == self.turn:
                        self.heuristic += self.turn
                    else:
                        self.heuristic -= self.turn

                # three vertical with an empty space on top
                if ((2 < j < 6)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j - 1) * 7)+ i]
                  == self.board[((j - 2) * 7)+ i]
                           )
                and (self.board[((j - 3) * 7) + i] == 0)
                ):
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
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 2])
                                   )
                        # 1011
                        or        (
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
                             and      (
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
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 2])
                         and (0
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1001
                        or        (
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
                    else: # if (self.board[(j * 7) + i] == 0):
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
                            or        (
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
                            and       (
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
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0
                          == self.board[((j - 2) * 7) + i + 2])
                                   )
                        # 1011
                        or        (
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
                             and      (
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
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 2) * 7) + i + 2])
                         and (0
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 3) * 7) + i + 3])
                                   )
                        # 1001
                        or        (
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
                    else: # if (self.board[(j * 7) + i] == 0):
                        if self.board[((j - 1) * 7) + i + 1] != 0:
                            # 0111
                            if ( self.board[((j - 1) * 7) + i + 1]
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
                            or        (
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
                        else: # if (self.board[((j - 1) * 7) + i + 1] == 0):
                            # 0011
                            if ((self.board[((j - 2) * 7) + i + 2] != 0)
                            and       (
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
                        or        (
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
                             and       (
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
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 2) * 7) + i + 2])
                         and (0
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1001
                        or        (
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
                            or        (
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
                        else: # if (self.board[((j + 1) * 7) + i + 1] == 0):
                            # 0011
                            if (
                                (self.board[((j + 2) * 7) + i + 2] != 0)
                            and       (
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
            print ('heuristic: infinity')
        elif self.heuristic == -100000:
            print ('heuristic: -infinity')
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

    def get_next_moves(self): # isinstance(game, Game())
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        next_moves = [
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self()
        ]
        for i in range(7):
            if next_moves[i].board[i] == 0: # if space to make a move,
                next_moves[i].go_for_la(i)     # makes a move
            else:
                next_moves[i] = 9
        return next_moves

    def get_best_move(self, depth): # isinstance(game, Game())
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        if depth == 0 or self.result != 0:
            return
        if depth == 1:
            self.look_ahead()
        next_moves = [
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self()
        ]
        for i in range(7):
            if next_moves[i].board[i] == 0: # if space to make a move,
                next_moves[i].go_for_la(i)     # makes a move
            else:
                next_moves[i] = 9
        for i in range(7):
            if isinstance(next_moves[i], Game):
                self.get_best_move(depth - 1) # next_moves[i]

    def minimax(self, depth, original_depth, alpha, beta):
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
            next_moves = [
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self()
            ]
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0: # if space to make a move,
                    next_moves[i].go_for_la(i)     # makes a move
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
            next_moves = [
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self()
            ]
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0: # if space to make a move,
                    next_moves[i].go_for_la(i)     # makes a move
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

    def pre_alpha_beta(self, depth, original_depth):
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
            next_moves = [
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self()
            ]
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0: # if space to make a move,
                    next_moves[i].go_for_la(i)     # makes a move
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
            next_moves = [
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self(),
                self.copy_self()
            ]
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0: # if space to make a move,
                    next_moves[i].go_for_la(i)     # makes a move
                    move = next_moves[i].pre_alpha_beta(depth - 1, original_depth)
                    if move.heuristic < min_eval:
                        min_eval = move.heuristic
                        best_move = move
                        best_column = i
            if depth == original_depth:
                return best_column
            else:
                return best_move

        # looks one move ahead and chooses the best move based on heuristic
    def look_ahead(self): # isinstance(self, Game())
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        assert (self.result == 0), 'cannot calculate future moves on a finished game'
        # possible_moves is a 7-index array of games,
        # each index representing the board state if
        # a move is made in the column with the
        # same i-number as the array index
        possible_moves = [
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self()
        ]
        # sets start to correspond to something valid
        # creates an initial best, which will be updated
        # each time it is compared with another move
        # plays move where move plays are valid,
        # marks columns where plays are not valid
        for i in range(7):
            if possible_moves[i].board[i] == 0: # if space to make a move,
                possible_moves[i].go_for_la(i)     # makes a move
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

    # checks to see if both players have made at least one move
    # if not, returns True
    def is_first_turn(self):
        '''
        _summary_

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

    # plays a random non-side move for a first turn
    def play_first_turn(self):
        '''
        _summary_
        '''
        self.go_u(np.random.randint(1,5))

    # plays two random non-side moves. designed to start games where both sides
    # are played by robots
    def play_first_turns(self):
        '''
        _summary_
        '''
        self.go_u(np.random.randint(1,5))
        self.go_u(np.random.randint(1,5))

    def dispaly_info(self):
        '''
        _summary_
        '''
        self.display_result()
        self.print_board()
        self.display_heuristic()

    # human plays one turn; computer displays result and information about game
    def go_u(self, i):
        '''
        _summary_

        Args:
            i (_type_): _description_
        '''
        assert (self.result == 0), "this game is over! you can't place pieces anymore."
        self.set_space(self.select_space(i), self.turn)
        if self.turn == -1:
            self.number_of_moves += 1
        self.turn = np.negative(self.turn)
        # print(' ')
        # self.update_heuristic()
        # self.display_heuristic()
        # self.print_board()
        self.update_result()
        # self.display_result()
        # print(' ')

    # computer plays the pre-alpha-beta minimax recommended turn
    def go_pre_ab(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        if self.is_first_turn():
            self.play_first_turn()
        else:
            self.go_u(self.pre_alpha_beta(depth, depth))

    # plays one turn for look_ahead function
    def go_for_la(self, i):
        '''
        _summary_

        Args:
            i (_type_): _description_
        '''
        self.set_select_space_for_la(i)
        self.turn = np.negative(self.turn)
        self.update_result()
        self.update_heuristic()

    # computer plays the minimax-recommended turn
    def go_minimax(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        assert (depth > 0), 'minimax cannot search to a depth less than one'
        if self.is_first_turn():
            self.play_first_turn()
        else:
            self.go_u(self.minimax(depth, depth, -np.inf, np.inf))

    # computer plays minimax-recommended turn for turns number of turns, switching between sides
    def go_minimaxx_x(self, depth, turns):
        '''
        _summary_

        Args:
            depth (_type_): _description_
            turns (_type_): _description_
        '''
        for _ in range(turns):
            if self.result != 0:
                self.reset_game()
                break
            if self.is_first_turn():
                self.play_first_turn()
            else:
                self.go_minimax(depth)

    # computer plays the heuristic-recommended turn
    def go_heuristic(self):
        '''
        _summary_
        '''
        if self.is_first_turn():
            self.play_first_turn()
        else:
            self.go_u(self.look_ahead())

    # computer plays heuristic-recommended turn for turns number of turns, switching between sides
    def go_heuristicx_x(self, turns):
        '''
        _summary_

        Args:
            turns (_type_): _description_
        '''
        for _ in range(turns):
            if self.result != 0:
                self.reset_game()
                break
            if self.is_first_turn():
                self.play_first_turn()
            else:
                self.go_heuristic()

    # computer plays a random turn
    def go_random(self):
        '''
        _summary_
        '''
        column = np.random.randint(0, 6)
        while self.board[column] != 0:
            column = np.random.randint(0, 6)
        self.go_u(column)

    # computer plays random turn for turns number of turns, switching between sides
    def go_randomx_x(self, turns):
        '''
        _summary_

        Args:
            turns (_type_): _description_
        '''
        for _ in range(turns):
            if self.result != 0:
                self.reset_game()
                break
            self.go_random()

    # human plays a move
    def go_human(self):
        '''
        _summary_
        '''
        print('input an integer between 0 and 6, inclusive')
        column = int(input('which column do you choose to place your piece in? '))
        while not(column == 0
                    or column == 1
                    or column == 2
                    or column == 3
                    or column == 4
                    or column == 5
                    or column == 6):
            column = int(input('that was not an integer between 0 and 6. try again: '))
        self.go_u(column)


    # human plays a game versus a computer opponent
    def play_game(self):
        '''
        _summary_
        '''
        is_human_first = np.random.choice([True, False])
        if is_human_first:
            print('You are player 1')
        else:
            print('You are player 2')
        print(' ')
        print('input an integer between 0 and 3, inclusive')
        level = int(input('which strength AI do you choose to play against? '))
        while not (
            level == 0
            or level == 1
            or level == 2
            or level == 3
            or level == 4
            or level == 5
            or level == 6
        ):
            level = int(input('that was not an integer between 0 and 6. try again: '))
        self.print_board()
        if is_human_first:
            self.go_human()
            self.play_first_turn()
            self.go_human()
        else:
            self.play_first_turn()
            self.go_human()
        if level == 0:
            while self.result == 0:
                self.go_random()
                if self.result != 0:
                    self.reset_game()
                    return
                self.go_human()
        else:
            while self.result == 0:
                self.go_minimax(level)
                if self.result != 0:
                    self.reset_game()
                    return
                self.go_human()

    # preAB plays a game against itself
    def pre_abvs_pre_ab(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_pre_ab(depth)
        self.reset_game()

    # preAB plays a game against Minimax
    def pre_abvs_minimax(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_pre_ab(depth)
            if self.result != 0:
                break
            self.go_minimax(depth)
        self.reset_game()

    # Minimax plays a game against preAB
    def minimax_vs_pre_ab(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_minimax(depth)
            if self.result != 0:
                break
            self.go_pre_ab(depth)
        self.reset_game()

    # single function for all computer vs computer matchups
    def comp_matchup(self, player_1_level, player_2_level):
        '''
        _summary_

        Args:
            player_1_level (_type_): _description_
            player_2_level (_type_): _description_

        Returns:
            _type_: _description_
        '''
        self.reset_game()
        assert ((-1 < player_1_level < 7)
            and (-1 < player_2_level < 7)), 'AI levels go from zero to six'
        self.play_first_turns()
        if player_1_level == 0 and player_2_level == 0:
            while self.result == 0:
                self.go_random()
        elif player_1_level == 0 and player_2_level != 0:
            while self.result == 0:
                self.go_random()
                if self.result != 0:
                    break
                self.go_minimax(player_2_level)
        elif player_1_level != 0 and player_2_level == 0:
            while self.result == 0:
                self.go_minimax(player_1_level)
                if self.result != 0:
                    break
                self.go_random()
        else:
            while self.result == 0:
                self.go_minimax(player_1_level)
                if self.result != 0:
                    break
                self.go_minimax(player_2_level)
        # if (self.result == 1):
        #     print('The level ' + str(player_1_level) + ' player, who went \
        #     first, beat the level ' + str(player_2_level) + ' player in ' \
        #     + str(self.number_of_moves) + ' moves.')
        # else:
        #     print('The level ' + str(player_2_level) + ' player, who went \
        #     second, beat the level ' + str(player_1_level) + ' player in '\
        #     + str(self.number_of_moves) + ' moves.')
        return self.result

    # plays games of a specified computer vs computer matchup and returns each
    # player's win percentage
    def comp_matchup_ultra(self, player_1_level, player_2_level, number_of_games):
        '''
        _summary_

        Args:
            player_1_level (_type_): _description_
            player_2_level (_type_): _description_
            number_of_games (_type_): _description_
        '''
        win_index = np.zeros(number_of_games, int)
        win_percentage = 0
        draw_percentage = 0
        for i in range(number_of_games):
            win_index[i] = self.comp_matchup(player_1_level, player_2_level)
            if win_index[i] == 1:
                win_percentage += 1
            elif win_index[i] == 3:
                draw_percentage += 1
            print('game ' + str(i) + '     result: ' + str(win_index[i]))
        win_percentage = int(win_percentage) * (100 / int(number_of_games))
        draw_percentage = int(draw_percentage) * (100 / int(number_of_games))
        print('In ' + str(number_of_games) + ' games, the level ' \
              + str(player_1_level) + ' player, who went first, \
              beat the level ' + str(player_2_level) + ' player ' \
              + str(win_percentage) + '% of the time. ' + str(draw_percentage) \
              + '% of the games were draws.')

    # Minimax plays a game against Minimax
    def minimax_vs_minimax(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_minimax(depth)
        self.reset_game()

    # Minimax plays a game against Minimax with different search depth
    def minimax_vs_minimax_2(self, depth1, depth2):
        '''
        _summary_

        Args:
            depth1 (_type_): _description_
            depth2 (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_minimax(depth1)
            if self.result != 0:
                break
            self.go_minimax(depth2)
        self.reset_game()

    # Minimax plays a game against Heuristic
    def minimax_vs_heuristic(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_minimax(depth)
            if self.result != 0:
                break
            self.go_heuristic()
        self.reset_game()

    # Minimax plays a game against Random
    def minimax_vs_random(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_minimax(depth)
            if self.result != 0:
                break
            self.go_random()
        self.reset_game()

    # Heuristic plays a game against Minimax
    def heuristic_vs_minimax(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_heuristic()
            if self.result != 0:
                break
            self.go_minimax(depth)
        self.reset_game()

    # Heuristic plays a game against Heuristic
    def heuristic_vs_heuristic(self):
        '''
        _summary_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_heuristic()
        self.reset_game()

    # Heuristic plays a game against Random
    def heuristic_vs_random(self):
        '''
        _summary_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_heuristic()
            if self.result != 0:
                break
            self.go_random()
        self.reset_game()

    # Random plays a game against Minimax
    def random_vs_minimax(self, depth):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_random()
            if self.result != 0:
                break
            self.go_minimax(depth)
        self.reset_game()

    # Random plays a game against Heuristic
    def random_vs_heuristic(self):
        '''
        _summary_
        '''
        self.play_first_turns()
        while self.result == 0:
            self.go_random()
            if self.result != 0:
                break
            self.go_heuristic()
        self.reset_game()

    # Random plays a game against Random
    def random_vs_random(self):
        '''
        _summary_
        '''
        while self.result == 0:
            self.go_random()
        self.reset_game()
