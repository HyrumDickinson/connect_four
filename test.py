'''
minimal main launcher
'''

from game import Game
from matchup import matchup

if __name__ == '__main__':
    game = Game('random', 'random')
    matchup(game)
    game = Game('random', 'human')
    game.play()
    # game.play_matchup('random', 'minimax')
    # game.play_matchup('heuristic', 'random')
    # game.play_matchup('heuristic', 'heuristic')
    # game.play_matchup('heuristic', 'minimax')
    # game.play_matchup('minimax', 'heuristic')
    # game.play_matchup('minimax', 'minimax')
