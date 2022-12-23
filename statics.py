'''
contains statics
'''

from abort_me import Game

def matchup(
    player_1: str = 'human',
    player_2: str = 'human',
    depth_1: int = 5,
    depth_2: int = 5,
    player_1_name: str = 'player_1',
    player_2_name: str = 'player_2',
    rounds: int = 10,
    verbose: bool = False
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
        match = Game()
        result = Game.match.play(
            player_1=player_1,
            player_2=player_2,
            depth_1=depth_1,
            depth_2=depth_2,
            player_1_name=player_1_name,
            player_2_name=player_2_name,
            print_game=verbose
        )
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
    print(f'{player_1_name} {player_1_score}-{draw_count}-{player_2_score} {player_2_name}')
