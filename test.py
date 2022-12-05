'''
minimal main launcher
'''

from game import Game

if __name__ == '__main__':
    tictactoe = Game()
    tictactoe.play_game('random', 'random')
    tictactoe.play_matchup('random', 'random')
    # tictactoe.play_matchup('random', 'minimax')
    # tictactoe.play_matchup('heuristic', 'random')
    # tictactoe.play_matchup('heuristic', 'heuristic')
    # tictactoe.play_matchup('heuristic', 'minimax')
    # tictactoe.play_matchup('minimax', 'heuristic')
    # tictactoe.play_matchup('minimax', 'minimax')