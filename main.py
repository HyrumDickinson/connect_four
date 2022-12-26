'''
minimal main launcher
'''

from game import Game

if __name__ == '__main__':
    game = Game('human', 'random')
    game.play()
