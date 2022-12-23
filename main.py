'''
minimal main launcher
'''

from abort_me import Game

if __name__ == '__main__':
    tictactoe = Game()
    tictactoe.play_game('human', 'random')
