'''
contains matchup function
'''

from game import Game\

def matchup(
    game: Game,
    rounds: int = 10
):
    '''
    match up two players for a set of games

    Args:
        player_1 (str, optional): _description_. Defaults to 'human'.
        player_2 (str, optional): _description_. Defaults to 'human'.
        depth_1 (int, optional): _description_. Defaults to 5.
        depth_2 (int, optional): _description_. Defaults to 5.
        rounds (int, optional): _description_. Defaults to 10.
    '''

    # play matches
    matches = []
    for _ in range(rounds):
        match = game.copy
        result = match.play()
        matches.append(result)

    # analyze results
    player_1_score = 0
    player_2_score = 0
    draw_count = 0
    for match in matches:
        if match == 1:
            player_1_score += 1
        elif match == -1:
            player_2_score += 1
        elif match == 3:
            draw_count += 1
        else:
            raise Exception('invalid match result')
    print(f'{game.player_1.name} {player_1_score}-{draw_count}-{player_2_score} {game.player_2.name}')