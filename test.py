'''
minimal main launcher
'''

from game import Game

if __name__ == '__main__':

    # Game('random', 'random').play(10)
    # Game('random', 'human').play()
    # Game('human', 'human').play()
    # Game('random', 'minimax').play()
    # Game('heuristic', 'random').play(99)
    # Game('random', 'heuristic').play(99)
    # Game('heuristic', 'heuristic').play(99)
    # Game('heuristic', 'minimax').play()
    # Game('minimax', 'heuristic').play()
    game = Game('minimax', 'minimax')
    game.player_1.depth = 1
    game.player_2.depth = 3
    game.play(10)

    # Game('random', 'random').play(9)
    # Game('random', 'human').play(9)
    # Game('human', 'human').play(9)
    # Game('random', 'minimax').play(9)
    # Game('heuristic', 'random').play(9)
    # Game('heuristic', 'heuristic').play(9)
    # Game('heuristic', 'minimax').play(9)
    # Game('minimax', 'heuristic').play(9)
    # Game('minimax', 'minimax').play(9)
