"""
contains simple player class
"""


class Player:
    """
    player class
    """

    def __init__(self, strategy: str, my_turn: bool, depth: int = 3):

        assert strategy in (
            'human',
            'random',
            'heuristic',
            'minimax',
        )

        self.strategy = strategy
        self.my_turn = my_turn
        self.depth = depth

        if self.strategy == 'human':
            self.search_depth = 0
        if self.strategy == 'random':
            self.search_depth = 0
        if self.strategy == 'heuristic':
            self.search_depth = 5
        if self.strategy == 'minimax':
            self.search_depth = 5

        # this only runs when player is created
        # when it's player_1's turn
        if self.my_turn:
            self.name = f'{self.strategy}_player_1'
            self.token = 1
        else:
            self.name = f'{self.strategy}_player_2'
            self.token = -1
