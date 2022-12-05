'''
minimal main launcher
'''

from game import Game

if __name__ == '__main__':
    tictactoe = Game()
    tictactoe.play_game('human', 'random')
