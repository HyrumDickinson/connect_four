'''
contains matchup function
'''

from game import Game
from statics import print_board


def matchup(
    game: Game,
    rounds: int = 10
):
    '''
    match up two players for a set of games

    Args:
        game (Game): _description_
        rounds (int, optional): _description_. Defaults to 10.
    '''

    # play matches
    matches = []
    for _ in range(rounds):
        game.reset()
        game.play()
        matches.append(game.result)
        print_board(game.board)

    # analyze results
    player_1_score = 0
    player_2_score = 0
    draw_count = 0
    for match in matches:
        assert match in (1, -1, 3)
        if match == 1:
            player_1_score += 1
        if match == -1:
            player_2_score += 1
        if match == 3:
            draw_count += 1

    print(f'{game.player_1.name} {player_1_score}-{draw_count}-{player_2_score} {game.player_2.name}')
