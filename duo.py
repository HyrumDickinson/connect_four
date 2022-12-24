'''
contains duo class (two players)
'''

from player import Player


class Duo:
    '''
    duo class
    '''
    def __init__(self, player_1_strategy: str, player_2_strategy: str):
        self.player_1 = Player(player_1_strategy, True)
        self.player_2 = Player(player_2_strategy, False)
