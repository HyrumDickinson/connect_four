'''
contains heuristic functions
gives a rating of position based only on current location of pieces (no looking ahead)
'''
import numpy as np
from board import Board
from board_functions import current_player, can_place, print_board

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
    for row in range(6):
        for column in range(7):
            score += space_heuristic(board, column, row)
            if score in (np.inf, -np.inf):
                return score
    print_board(board)
    print(f'heuristic eval: {score}')
    return score


def space_heuristic(board: Board, column: int, row: int) -> int:
    '''
    _summary_

    Args:
        board (Board): _description_
        column (int): _description_
        row (int): _description_

    Returns:
        _type_: _description_
    '''

    score = 0

    # check horizontal wins
    if (
        column < 4 and
        board.spaces[(row * 7) + column] != 0 and
        (board.spaces[(row * 7) + column]
            == board.spaces[(row * 7) + column + 1]
            == board.spaces[(row * 7) + column + 2]
            == board.spaces[(row * 7) + column + 3])
    ):
        return np.inf * board.spaces[(row * 7) + column]

    # check downwards diagonal wins
    if (
        column < 4 and row < 3
        and (board.spaces[(row * 7) + column] != 0)
        and (
            board.spaces[(row * 7) + column]
            == board.spaces[((row + 1) * 7) + column + 1]
            == board.spaces[((row + 2) * 7) + column + 2]
            == board.spaces[((row + 3) * 7) + column + 3])
    ):
        return np.inf * board.spaces[(row * 7) + column]

    # check upwards diagonal wins
    if (
        column < 4 and row > 2
        and (board.spaces[(row * 7) + column] != 0)
        and (
            board.spaces[(row * 7) + column]
            == board.spaces[((row - 1) * 7) + column + 1]
            == board.spaces[((row - 2) * 7) + column + 2]
            == board.spaces[((row - 3) * 7) + column + 3])
    ):
        return np.inf * board.spaces[(row * 7) + column]

    # check vertical wins
    if (
        row < 3
        and (board.spaces[(row * 7) + column] != 0)
        and (
            board.spaces[(row * 7) + column]
            == board.spaces[((row + 1) * 7) + column]
            == board.spaces[((row + 2) * 7) + column]
            == board.spaces[((row + 3) * 7) + column])
    ):
        return np.inf * board.spaces[(row * 7) + column]

    # Verticals

    # two vertical with an empty space on top
    if (
        1 < row < 6
        and (board.spaces[(row * 7) + column] != 0)
        and (
            board.spaces[(row * 7) + column]
            == board.spaces[((row - 1) * 7) + column])
        and (board.spaces[((row - 2) * 7) + column] == 0)
    ):
        score += current_player(board)

    # three vertical with an empty space on top
    if (
        2 < row < 6
        and (board.spaces[(row * 7) + column] != 0)
        and (
            board.spaces[(row * 7) + column]
            == board.spaces[((row - 1) * 7) + column]
            == board.spaces[((row - 2) * 7) + column])
        and (board.spaces[((row - 3) * 7) + column] == 0)
    ):
        if (
            board.spaces[(row * 7) + column] == current_player(board)
            and can_place(board, ((row - 3) * 7) + column)
        ):
            score += 1000 * current_player(board)
        else:
            score += 7 * current_player(board)

    # Horizontals and diagonals

    # horizontals
    if column < 4:
        if board.spaces[(row * 7) + column] != 0:
            if (
                    # 1110
                    (
                    (
                        board.spaces[(row * 7) + column]
                        == board.spaces[(row * 7) + column + 1]
                        == board.spaces[(row * 7) + column + 2])
                    and (
                        0 == board.spaces[(row * 7) + column + 3])
                )
                    # 1101
                or (
                    (
                        board.spaces[(row * 7) + column]
                        == board.spaces[(row * 7) + column + 1]
                        == board.spaces[(row * 7) + column + 3])
                    and (
                        0 == board.spaces[(row * 7) + column + 2])
                )
                    # 1011
                or (
                    (
                        board.spaces[(row * 7) + column]
                        == board.spaces[(row * 7) + column + 2]
                        == board.spaces[(row * 7) + column + 3])
                    and (
                        0 == board.spaces[(row * 7) + column + 1])
                )
            ):

                # each configuration will have one empty space, so
                # only one of the following IF's OR conditions can
                # be true. the others will be checking already
                # filled spaceswhat those spaces are will depend on
                # which OR in the previous IF condition was true

                if (
                    (board.spaces[(row * 7) + column] == current_player(board))
                    and (
                        can_place(board, (row * 7) + column + 1)
                        or can_place(board, (row * 7) + column + 2)
                        or can_place(board, (row * 7) + column + 3)
                    )
                ):
                    score += 1000 * current_player(board)
                else:
                    score += 7 * current_player(board)
            if (
                # 1100
                (
                    (
                        board.spaces[(row * 7) + column]
                        == board.spaces[(row * 7) + column + 1])
                    and (
                        0 == board.spaces[(row * 7) + column + 2]
                        == board.spaces[(row * 7) + column + 3])
                )
                # 1010
                or (
                    (
                        board.spaces[(row * 7) + column]
                        == board.spaces[(row * 7) + column + 2])
                    and (
                        0 == board.spaces[(row * 7) + column + 1]
                        == board.spaces[(row * 7) + column + 3])
                )
                # 1001
                or (
                    (
                        board.spaces[(row * 7) + column]
                        == board.spaces[(row * 7) + column + 3])
                    and (
                        0 == board.spaces[(row * 7) + column + 1]
                        == board.spaces[(row * 7) + column + 2])
                )
            ):
                if board.spaces[(row * 7) + column] == current_player(board):
                    score += current_player(board)
                else:
                    score -= current_player(board)
        else:
            if board.spaces[(row * 7) + column + 1] != 0:
                # 0111
                if (
                    board.spaces[(row * 7) + column + 1]
                    == board.spaces[(row * 7) + column + 2]
                    == board.spaces[(row * 7) + column + 3]
                ):
                    if (
                        (board.spaces[(row * 7) + column + 1] == current_player(board))
                        and (can_place(board, (row * 7) + column))
                    ):
                        score += 1000 * current_player(board)
                    elif (
                        board.spaces[(row * 7) + column + 1] == current_player(board)
                    ):
                        score += 7 * current_player(board)
                    else:
                        score -= 7 * current_player(board)
                if (
                    # 0110
                            (
                    (board.spaces[(row * 7) + column + 1]
                    == board.spaces[(row * 7) + column + 2])
                    and (0
                    == board.spaces[(row * 7) + column + 3])
                            )
                # 0101
                or (
                    (board.spaces[(row * 7) + column + 1]
                    == board.spaces[(row * 7) + column + 3])
                    and (0
                    == board.spaces[(row * 7) + column + 2])
                            )
                ):
                    if board.spaces[(row * 7) + column + 1] == current_player(board):
                        score += current_player(board)
                    else:
                        score -= current_player(board)
            else:
                # 0011
                if ((board.spaces[(row * 7) + column + 2] != 0)
                and (
                        board.spaces[(row * 7) + column + 2]
                    == board.spaces[(row * 7) + column + 3]
                            )
                ):
                    if board.spaces[(row * 7) + column + 2] == current_player(board):
                        score += current_player(board)
                    else:
                        score -= current_player(board)

    # upwards diagonals
    if column < 4 and row > 2:
        if board.spaces[(row * 7) + column] != 0:
            if (
            # 1110
                    (
                    (board.spaces[(row * 7) + column]
                    == board.spaces[((row - 1) * 7) + column + 1]
                    == board.spaces[((row - 2) * 7) + column + 2])
                    and (0 == board.spaces[((row - 3) * 7) + column + 3])
                )
                # 1101
                or (
                    (board.spaces[(row * 7) + column]
                    == board.spaces[((row - 1) * 7) + column + 1]
                    == board.spaces[((row - 3) * 7) + column + 3])
                    and (0 == board.spaces[((row - 2) * 7) + column + 2])
                )
                # 1011
                or (
                    (board.spaces[(row * 7) + column]
                    == board.spaces[((row - 2) * 7) + column + 2]
                    == board.spaces[((row - 3) * 7) + column + 3])
                    and (0 == board.spaces[((row - 1) * 7) + column + 1])
                )
            ):
                # each scenario will have an empty space, so only
                # 1 of the following IF's OR conditions can be true
                # the others will be checking already-filled spaces
                # what those spaces are will depend on which OR in
                # the previous IF condition was true
                if (
                    (board.spaces[(row * 7) + column] == current_player(board))
                    and (
                        can_place(board, ((row - 3) * 7) + column + 3)
                        or can_place(board, ((row - 2) * 7) + column + 2)
                        or can_place(board, ((row - 1) * 7) + column + 1)
                    )
                ):
                    score += 1000 * current_player(board)
                elif (
                    board.spaces[(row * 7) + column] == current_player(board)
                ):
                    score += 7 * current_player(board)
                else:
                    score -= 7 * current_player(board)
                if (
                    # 1100
                        (
                        (board.spaces[(row * 7) + column]
                        == board.spaces[((row - 1) * 7) + column + 1])
                        and (0
                        == board.spaces[((row - 2) * 7) + column + 2]
                        == board.spaces[((row - 3) * 7) + column + 3])
                    )
                    # 1010
                    or (
                        (board.spaces[(row * 7) + column]
                        == board.spaces[((row - 2) * 7) + column + 2])
                        and (0
                        == board.spaces[((row - 1) * 7) + column + 1]
                        == board.spaces[((row - 3) * 7) + column + 3])
                    )
                    # 1001
                    or (
                        (board.spaces[(row * 7) + column]
                        == board.spaces[((row - 3) * 7) + column + 3])
                        and (0
                        == board.spaces[((row - 1) * 7) + column + 1]
                        == board.spaces[((row - 2) * 7) + column + 2])
                    )
                ):
                    if board.spaces[(row * 7) + column] == current_player(board):
                        score += current_player(board)
                    else:
                        score -= current_player(board)
        else:
            if board.spaces[((row - 1) * 7) + column + 1] != 0:
                # 0111
                if (board.spaces[((row - 1) * 7) + column + 1]
                    == board.spaces[((row - 2) * 7) + column + 2]
                    == board.spaces[((row - 3) * 7) + column + 3]
                ):
                    if (
                        (board.spaces[((row - 1) * 7) + column + 1] == current_player(board))
                        and (can_place(board, (row * 7) + column))
                    ):
                        score += 1000 * current_player(board)
                    elif (board.spaces[((row - 1) * 7) + column + 1] == current_player(board)
                    ):
                        score += 7 * current_player(board)
                    else:
                        score -= 7 * current_player(board)
                if (
                    # 0110
                        (
                            (
                                board.spaces[((row - 1) * 7) + column + 1]
                            == board.spaces[((row - 2) * 7) + column + 2]
                        )
                        and (0 == board.spaces[((row - 3) * 7) + column + 3])
                    )
                    # 0101
                    or (
                        (board.spaces[((row - 1) * 7) + column + 1]
                        == board.spaces[((row - 3) * 7) + column + 3])
                        and (0 == board.spaces[((row - 2) * 7) + column + 2])
                    )
                ):
                    score += current_player(board)

            else:
                # 0011
                if ((board.spaces[((row - 2) * 7) + column + 2] != 0)
                and (
                        board.spaces[((row - 2) * 7) + column + 2]
                    == board.spaces[((row - 3) * 7) + column + 3]
                )
                ):
                    score += current_player(board)

    # downwards diagonals
    if column < 4 and row < 3:
        if board.spaces[(row * 7) + column] != 0:
            if (
            # 1110
                        (
                (board.spaces[(row * 7) + column]
                == board.spaces[((row + 1) * 7) + column + 1]
                == board.spaces[((row + 2) * 7) + column + 2])
                and (0
                == board.spaces[((row + 3) * 7) + column + 3])
                        )
            # 1101
            or (
                (
                board.spaces[(row * 7) + column]
                == board.spaces[((row + 1) * 7) + column + 1]
                == board.spaces[((row + 3) * 7) + column + 3])
                and (0
                == board.spaces[((row + 2) * 7) + column + 2])
                )
            # 1011
            or (
                (
                    board.spaces[(row * 7) + column]
                    == board.spaces[((row + 2) * 7) + column + 2]
                    == board.spaces[((row + 3) * 7) + column + 3])
                and (
                    0
                    == board.spaces[((row + 1) * 7) + column + 1])
                )
            ):
                # each configuration will have one empty space, so only
                # one of the following IF's OR conditions can be true
                # the others will be checking already-filled spaces
                # what those spaces are will depend on which OR in
                # the previous IF condition was true
                if (
                    (board.spaces[(row * 7) + column] == current_player(board))
                    and (
                        can_place(board, ((row + 3) * 7) + column + 3)
                        or can_place(board, ((row + 2) * 7) + column + 2)
                        or can_place(board, ((row + 1) * 7) + column + 1)
                            )
                ):
                    score += 1000 * current_player(board)
                elif (
                    board.spaces[(row * 7) + column] == current_player(board)
                ):
                    score += 7 * current_player(board)
                else:
                    score -= 7 * current_player(board)
            if (
                # 1100
                (
                (
                    board.spaces[(row * 7) + column]
                    == board.spaces[((row + 1) * 7) + column + 1])
                and (
                    0
                    == board.spaces[((row + 2) * 7) + column + 2]
                    == board.spaces[((row + 3) * 7) + column + 3])
                )
            # 1010
            or (
                (
                    board.spaces[(row * 7) + column]
                    == board.spaces[((row + 2) * 7) + column + 2])
                and (
                    0
                    == board.spaces[((row + 1) * 7) + column + 1]
                    == board.spaces[((row + 3) * 7) + column + 3])
                )
            # 1001
            or (
                (
                    board.spaces[(row * 7) + column]
                    == board.spaces[((row + 3) * 7) + column + 3])
                and (
                    0
                    == board.spaces[((row + 1) * 7) + column + 1]
                    == board.spaces[((row + 2) * 7) + column + 2])
                )
            ):
                score += current_player(board)
        else:
            if board.spaces[((row + 1) * 7) + column + 1] != 0:
                # 0111
                if (
                    board.spaces[((row + 1) * 7) + column + 1]
                    == board.spaces[((row + 2) * 7) + column + 2]
                    == board.spaces[((row + 3) * 7) + column + 3]
                ):
                    if (
                        (board.spaces[((row + 1) * 7) + column + 1] == current_player(board))
                        and (can_place(board, (row * 7) + column))
                    ):
                        score += (1000 * current_player(board))
                    else:
                        score += 7 * current_player(board)
                if (
                    # 0110
                        (
                            (
                            board.spaces[((row + 1) * 7) + column + 1]
                            == board.spaces[((row + 2) * 7) + column + 2])
                            and (board.spaces[((row + 3) * 7) + column + 3]
                        )
                    )
                    # 0101
                or (
                        (
                        board.spaces[((row + 1) * 7) + column + 1]
                        == board.spaces[((row + 3) * 7) + column + 3]
                    )
                and (
                    0
                    == board.spaces[((row + 2) * 7) + column + 2])
                            )
                ):
                    score += current_player(board)

            else:
                # 0011
                if (
                    (board.spaces[((row + 2) * 7) + column + 2] != 0)
                    and (
                        board.spaces[((row + 2) * 7) + column + 2]
                        == board.spaces[((row + 3) * 7) + column + 3]
                    )
                ):
                    score += current_player(board)

    return score
