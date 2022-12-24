'''
minimal main launcher
'''

from game import Game
from matchup import matchup

if __name__ == '__main__':
    connect_four = Game('random', 'random')
    connect_four.play()
    matchup(connect_four)
    # connect_four.play_matchup('random', 'minimax')
    # connect_four.play_matchup('heuristic', 'random')
    # connect_four.play_matchup('heuristic', 'heuristic')
    # connect_four.play_matchup('heuristic', 'minimax')
    # connect_four.play_matchup('minimax', 'heuristic')
    # connect_four.play_matchup('minimax', 'minimax')
