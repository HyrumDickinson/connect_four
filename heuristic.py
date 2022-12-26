'''
contains heuristic functions
gives a rating of position based only on current location of pieces (no looking ahead)
'''
import numpy as np
from board import Board
from statics import current_player, can_place, print_board

# INTELLIGENCE
# to do:

# heuristic function -> rates positions
# minimax function -> searches all possible moves to specified depth
#                     applies heuristic function
#                     works backward to create best position,
#                     assuming opponent perfect play
# alpha-beta function -> I'll have to re-read up on this


def heuristic(board: Board) -> int:
    '''
    returns heuristic evaluation of position
    the larger the number, the better the position for player 1
    the smaller the number, the better the position for player -1

    Returns:
        _type_: _description_
    '''

    score = 0
    # player 1 will earn positive points
    # player 2 will earn negative points

    # Wins

    for j in range(6):
        for i in range(7):
            score += space_heuristic(board, i, j)

            if score in (np.inf, -np.inf):
                return score
    print_board(board)
    print(f'heuristic eval: {score}')
    return score


def space_heuristic(board: Board, i: int, j: int) -> int:
    '''
    _summary_

    Args:
        board (Board): _description_
        i (int): _description_
        j (int): _description_

    Returns:
        _type_: _description_
    '''

    score = 0

    # check horizontal wins
    if (
        i < 4 and
        board.spaces[(j * 7) + i] != 0 and
        (board.spaces[(j * 7) + i]
            == board.spaces[(j * 7) + i + 1]
            == board.spaces[(j * 7) + i + 2]
            == board.spaces[(j * 7) + i + 3])
    ):
        return np.inf * board.spaces[(j * 7) + i]

    # check downwards diagonal wins
    if (i < 4 and j < 3
        and (board.spaces[(j * 7) + i] != 0)
        and (
            board.spaces[(j * 7) + i]
            == board.spaces[((j + 1) * 7) + i + 1]
            == board.spaces[((j + 2) * 7) + i + 2]
            == board.spaces[((j + 3) * 7) + i + 3])
    ):
        return np.inf * board.spaces[(j * 7) + i]

    # check upwards diagonal wins
    if (i < 4 and j > 2
        and (board.spaces[(j * 7) + i] != 0)
        and (
            board.spaces[(j * 7) + i]
            == board.spaces[((j - 1) * 7) + i + 1]
            == board.spaces[((j - 2) * 7) + i + 2]
            == board.spaces[((j - 3) * 7) + i + 3])
    ):
        return np.inf * board.spaces[(j * 7) + i]

    # check vertical wins
    if (j < 3
        and (board.spaces[(j * 7) + i] != 0)
        and (
            board.spaces[(j * 7) + i]
            == board.spaces[((j + 1) * 7) + i]
            == board.spaces[((j + 2) * 7) + i]
            == board.spaces[((j + 3) * 7) + i])
    ):
        return np.inf * board.spaces[(j * 7) + i]

    # Verticals

    # two vertical with an empty space on top
    if (1 < j < 6
        and (board.spaces[(j * 7) + i] != 0)
        and (
            board.spaces[(j * 7) + i]
            == board.spaces[((j - 1) * 7) + i])
        and (board.spaces[((j - 2) * 7) + i] == 0)):
            score += current_player(board)

    # three vertical with an empty space on top
    if (2 < j < 6
        and (board.spaces[(j * 7) + i] != 0)
        and (board.spaces[(j * 7) + i]
            == board.spaces[((j - 1) * 7) + i]
            == board.spaces[((j - 2) * 7) + i])
        and (board.spaces[((j - 3) * 7) + i] == 0)):
        if (board.spaces[(j * 7) + i] == current_player(board)
        and can_place(board, ((j - 3) * 7) + i)
        ):
            score += 1000 * current_player(board)
        else:
            score += 7 * current_player(board)

    # Horizontals and diagonals

    # horizontals
    if i < 4:
        if board.spaces[(j * 7) + i] != 0:
            if (
            # 1110
                        (
                (board.spaces[(j * 7) + i]
                == board.spaces[(j * 7) + i + 1]
                == board.spaces[(j * 7) + i + 2])
                and (0
                == board.spaces[(j * 7) + i + 3])
                        )
            # 1101
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[(j * 7) + i + 1]
                == board.spaces[(j * 7) + i + 3])
                and (0
                == board.spaces[(j * 7) + i + 2])
                        )
            # 1011
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[(j * 7) + i + 2]
                == board.spaces[(j * 7) + i + 3])
                and (0
                == board.spaces[(j * 7) + i + 1])
                        )
            ):

                # each configuration will have one empty space, so
                # only one of the following IF's OR conditions can
                # be true. the others will be checking already
                # filled spaceswhat those spaces are will depend on
                # which OR in the previous IF condition was true

                if ((board.spaces[(j * 7) + i] == current_player(board))
                    and (
                        can_place(board, (j * 7) + i + 1)
                    or can_place(board, (j * 7) + i + 2)
                    or can_place(board, (j * 7) + i + 3)
                            )
                ):
                    score += 1000 * current_player(board)
                else:
                    score += 7 * current_player(board)
            if (
            # 1100
                        (
                (board.spaces[(j * 7) + i]
                == board.spaces[(j * 7) + i + 1])
                and (0
                == board.spaces[(j * 7) + i + 2]
                == board.spaces[(j * 7) + i + 3])
                        )
            # 1010
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[(j * 7) + i + 2])
                and (0
                == board.spaces[(j * 7) + i + 1]
               == board.spaces[(j * 7) + i + 3])
                        )
            # 1001
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[(j * 7) + i + 3])
                and (0
                == board.spaces[(j * 7) + i + 1]
                == board.spaces[(j * 7) + i + 2])
                        )
            ):
                if board.spaces[(j * 7) + i] == current_player(board):
                    score += current_player(board)
                else:
                    score -= current_player(board)
        else:
            if board.spaces[(j * 7) + i + 1] != 0:
                # 0111
                if (board.spaces[(j * 7) + i + 1]
                    == board.spaces[(j * 7) + i + 2]
                    == board.spaces[(j * 7) + i + 3]
                ):
                    if ((board.spaces[(j * 7) + i + 1] == current_player(board))
                    and (can_place(board, (j * 7) + i))
                    ):
                        score += 1000 * current_player(board)
                    elif (board.spaces[(j * 7) + i + 1] == current_player(board)
                    # and not can_place(board, the empty space)
                    ):
                        score += 7 * current_player(board)
                    else:
                    # if the player who isn't about to make a move
                    # has the advantago_us formation
                        score -= 7 * current_player(board)
                if (
                # 0110
                            (
                    (board.spaces[(j * 7) + i + 1]
                    == board.spaces[(j * 7) + i + 2])
                    and (0
                    == board.spaces[(j * 7) + i + 3])
                            )
                # 0101
                or (
                    (board.spaces[(j * 7) + i + 1]
                    == board.spaces[(j * 7) + i + 3])
                    and (0
                    == board.spaces[(j * 7) + i + 2])
                            )
                ):
                    if board.spaces[(j * 7) + i + 1] == current_player(board):
                        score += current_player(board)
                    else:
                        score -= current_player(board)
            else:
                # 0011
                if ((board.spaces[(j * 7) + i + 2] != 0)
                and (
                        board.spaces[(j * 7) + i + 2]
                    == board.spaces[(j * 7) + i + 3]
                            )
                ):
                    if board.spaces[(j * 7) + i + 2] == current_player(board):
                        score += current_player(board)
                    else:
                        score -= current_player(board)

    # upwards diagonals
    if i < 4 and j > 2:
        if board.spaces[(j * 7) + i] != 0:
            if (
            # 1110
                        (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j - 1) * 7) + i + 1]
                == board.spaces[((j - 2) * 7) + i + 2])
                and (0
                == board.spaces[((j - 3) * 7) + i + 3])
                        )
            # 1101
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j - 1) * 7) + i + 1]
                == board.spaces[((j - 3) * 7) + i + 3])
                and (0
                == board.spaces[((j - 2) * 7) + i + 2])
                        )
            # 1011
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j - 2) * 7) + i + 2]
                == board.spaces[((j - 3) * 7) + i + 3])
                and (0
                == board.spaces[((j - 1) * 7) + i + 1])
                        )
            ):
                # each scenario will have an empty space, so only
                # 1 of the following IF's OR conditions can be true
                # the others will be checking already-filled spaces
                # what those spaces are will depend on which OR in
                # the previous IF condition was true
                if ((board.spaces[(j * 7) + i] == current_player(board))
                    and (
                        can_place(board, ((j - 3) * 7) + i + 3)
                    or can_place(board, ((j - 2) * 7) + i + 2)
                    or can_place(board, ((j - 1) * 7) + i + 1)
                            )
                ):
                    score += 1000 * current_player(board)
                elif (board.spaces[(j * 7) + i] == current_player(board)
                # and not can_place(board, the empty space)
                ):
                    score += 7 * current_player(board)
                else:
                # if the player who isn't about to make a move has
                # the advantago_us formation
                    score -= 7 * current_player(board)
            if (
            # 1100
                        (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j - 1) * 7) + i + 1])
                and (0
                == board.spaces[((j - 2) * 7) + i + 2]
                == board.spaces[((j - 3) * 7) + i + 3])
                        )
            # 1010
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j - 2) * 7) + i + 2])
                and (0
                == board.spaces[((j - 1) * 7) + i + 1]
                == board.spaces[((j - 3) * 7) + i + 3])
                        )
            # 1001
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j - 3) * 7) + i + 3])
                and (0
                == board.spaces[((j - 1) * 7) + i + 1]
                == board.spaces[((j - 2) * 7) + i + 2])
                        )
            ):
                if board.spaces[(j * 7) + i] == current_player(board):
                    score += current_player(board)
                else:
                    score -= current_player(board)
        else:
            if board.spaces[((j - 1) * 7) + i + 1] != 0:
                # 0111
                if (board.spaces[((j - 1) * 7) + i + 1]
                    == board.spaces[((j - 2) * 7) + i + 2]
                    == board.spaces[((j - 3) * 7) + i + 3]
                ):
                    if ((board.spaces[((j - 1) * 7) + i + 1] == current_player(board))
                        and (can_place(board, (j * 7) + i))
                    ):
                        score += 1000 * current_player(board)
                    elif (board.spaces[((j - 1) * 7) + i + 1] == current_player(board)
                        # and not can_place(board, the empty space)
                    ):
                        score += 7 * current_player(board)
                    else:
                        # if the player who isn't about to make a move
                        # has the advantago_us formation
                        score -= 7 * current_player(board)
                if (
                    # 0110
                        (
                            (
                                board.spaces[((j - 1) * 7) + i + 1]
                            == board.spaces[((j - 2) * 7) + i + 2]
                        )
                        and (0
                        == board.spaces[((j - 3) * 7) + i + 3])
                    )
                    # 0101
                    or (
                        (board.spaces[((j - 1) * 7) + i + 1]
                        == board.spaces[((j - 3) * 7) + i + 3])
                        and (0
                        == board.spaces[((j - 2) * 7) + i + 2])
                    )
                ):
                    score += current_player(board)

            else:
                # 0011
                if ((board.spaces[((j - 2) * 7) + i + 2] != 0)
                and (
                        board.spaces[((j - 2) * 7) + i + 2]
                    == board.spaces[((j - 3) * 7) + i + 3]
                            )
                ):
                    score += current_player(board)

    # downwards diagonals
    if i < 4 and j < 3:
        if board.spaces[(j * 7) + i] != 0:
            if (
            # 1110
                        (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j + 1) * 7) + i + 1]
                == board.spaces[((j + 2) * 7) + i + 2])
                and (0
                == board.spaces[((j + 3) * 7) + i + 3])
                        )
            # 1101
            or        (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j + 1) * 7) + i + 1]
                == board.spaces[((j + 3) * 7) + i + 3])
                and (0
                == board.spaces[((j + 2) * 7) + i + 2])
                        )
            # 1011
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j + 2) * 7) + i + 2]
                == board.spaces[((j + 3) * 7) + i + 3])
                and (0
                == board.spaces[((j + 1) * 7) + i + 1])
                        )
            ):
                # each configuration will have one empty space, so only
                # one of the following IF's OR conditions can be true
                # the others will be checking already-filled spaces
                # what those spaces are will depend on which OR in
                # the previous IF condition was true
                if ((board.spaces[(j * 7) + i] == current_player(board))
                    and (
                        can_place(board, ((j + 3) * 7) + i + 3)
                    or can_place(board, ((j + 2) * 7) + i + 2)
                    or can_place(board, ((j + 1) * 7) + i + 1)
                            )
                ):
                    score += 1000 * current_player(board)
                elif (board.spaces[(j * 7) + i] == current_player(board)
                # and not can_place(board, the empty space)
                ):
                    score += 7 * current_player(board)
                else:
                # if the player who isn't about to make a move has
                # the advantago_us formation
                    score -= 7 * current_player(board)
            if (
            # 1100
                        (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j + 1) * 7) + i + 1])
                and (0
                == board.spaces[((j + 2) * 7) + i + 2]
                == board.spaces[((j + 3) * 7) + i + 3])
                        )
            # 1010
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j + 2) * 7) + i + 2])
                and (0
                == board.spaces[((j + 1) * 7) + i + 1]
                == board.spaces[((j + 3) * 7) + i + 3])
                        )
            # 1001
            or (
                (board.spaces[(j * 7) + i]
                == board.spaces[((j + 3) * 7) + i + 3])
                and (0
                == board.spaces[((j + 1) * 7) + i + 1]
                == board.spaces[((j + 2) * 7) + i + 2])
                        )
            ):
                score += current_player(board)
        else:
            if board.spaces[((j + 1) * 7) + i + 1] != 0:
                # 0111
                if (board.spaces[((j + 1) * 7) + i + 1]
                    == board.spaces[((j + 2) * 7) + i + 2]
                    == board.spaces[((j + 3) * 7) + i + 3]
                ):
                    if ((board.spaces[((j + 1) * 7) + i + 1] == current_player(board))
                    and (can_place(board, (j * 7) + i))
                    ):
                        score += (1000 * current_player(board))
                    else:
                        score += 7 * current_player(board)
                if (
                # 0110
                            (
                    (board.spaces[((j + 1) * 7) + i + 1]
                    == board.spaces[((j + 2) * 7) + i + 2])
                and (board.spaces[((j + 3) * 7) + i + 3])
                            )
                # 0101
                or (
                    (board.spaces[((j + 1) * 7) + i + 1]
                    == board.spaces[((j + 3) * 7) + i + 3])
                and (0
                    == board.spaces[((j + 2) * 7) + i + 2])
                            )
                ):
                    score += current_player(board)

            else:
                # 0011
                if (
                    (board.spaces[((j + 2) * 7) + i + 2] != 0)
                and (
                        board.spaces[((j + 2) * 7) + i + 2]
                    == board.spaces[((j + 3) * 7) + i + 3]
                            )
                ):
                    score += current_player(board)

    return score
