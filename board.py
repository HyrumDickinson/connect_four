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

import numpy as np


class Board:
    '''
    board class
    '''

    def __init__(self, board):

        assert (board == 'new' or isinstance(board, np.array))

        if board == 'new':
            self.board = np.zeros(42, int)
        else:
            self.board = board

    def reset(self):
        self.board = np.zeros(42, int)

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

    def set_space_by_column(self, i: int, value):
        '''
        set space by column

        Args:
            i (int): column
            value (_type_): _description_
        '''
        self.set_space(self.select_space(i), value)

    def set_space_by_coordinates(self, i: int, j: int, value):
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
            return ' X '
        if self.board[(j * 7) + i] == -1:
            return ' 0 '

    def print(self):
        '''
        provide visual printout of board
        '''
        print('\n')
        for j in range(6):
            for i in range(7):
                print(self.space_to_string(i, j), end=' ')
            print('\n')
