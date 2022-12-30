'''
contains board class
'''
import numpy as np


class Board:
    '''
    the board is a 7 x 6, seven being the horizontal length
    the indicies begin in the top left corner, and run horizontally
    to the right, like you would read a sentence, so,
    mapping the array to the board squares:


               0  1  2  3  4  5  6


        0      0  1  2  3  4  5  6
        1      7  8  9  10 11 12 13
        2      14 15 16 17 18 19 20
        3      21 22 23 24 25 26 27
        4      28 29 30 31 32 33 34
        5      35 36 37 38 39 40 41


    '''

    def __init__(self, board='new'):

        assert (board == 'new' or isinstance(board, np.ndarray))

        if board == 'new':
            self.spaces = np.zeros(42, int)
        else:
            self.spaces = board
