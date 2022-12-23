'''
contains duo class (two players)
'''

from player import player

class duo:
    '''
    duo class
    '''
    def __init__(self, player_1_strategy: str, player_2_strategy: str):
        self.player_1 = player(player_1_strategy, True)
        self.player_2 = player(player_2_strategy, False)
