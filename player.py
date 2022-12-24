'''
contains simple player class
'''


class Player:
    '''
    player class
    '''

    def __init__(self, strategy: str, goes_first: bool):

        assert strategy in (
            'human',
            'random',
            'heuristic',
            'minimax',
        )

        self.strategy = strategy
        self.goes_first = goes_first

        if self.strategy == 'human':
            self.search_depth = 0
        if self.strategy == 'random':
            self.search_depth = 0
        if self.strategy == 'heuristic':
            self.search_depth = 5
        if self.strategy == 'minimax':
            self.search_depth = 5

        if self.goes_first:
            self.name = f'{self.strategy}_player_1'
        self.name = f'{self.strategy}_player_2'
