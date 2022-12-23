from board import Board

# INTELLIGENCE
# to do:

# heuristic function -> rates positions
# minimax function -> searches all possible moves to specified depth
#                     applies heuristic function
#                     works backward to create best position,
#                     assuming opponent perfect play
# alpha-beta function -> I'll have to re-read up on this


def heuristic(board: Board):
    '''
    _summary_

    Returns:
        _type_: _description_
    '''

    heuristic = 0
    # player 1 will earn positive points
    # player 2 will earn negative points

    # Wins

    for j in range(6):
        for i in range(7):

            # check horizontal wins
            if (i < 4
                and (board[(j * 7) + i] != 0)
                and (
                    board[(j * 7) + i]
                    == board[(j * 7) + i + 1]
                    == board[(j * 7) + i + 2]
                    == board[(j * 7) + i + 3])):
                if board[(j * 7) + i] == turn:
                    heuristic = 100000 * turn
                else:
                    heuristic = -100000 * turn
                return

            # check downwards diagonal wins
            if (i < 4 and j < 3
                and (board[(j * 7) + i] != 0)
                and (
                    board[(j * 7) + i]
                    == board[((j + 1) * 7) + i + 1]
                    == board[((j + 2) * 7) + i + 2]
                    == board[((j + 3) * 7) + i + 3])):
                if board[(j * 7) + i] == turn:
                    heuristic = 100000 * turn
                else:
                    heuristic = -100000 * turn
                return

            # check upwards diagonal wins
            if (i < 4 and j > 2
                and (board[(j * 7) + i] != 0)
                and (
                    board[(j * 7) + i]
                    == board[((j - 1) * 7) + i + 1]
                    == board[((j - 2) * 7) + i + 2]
                    == board[((j - 3) * 7) + i + 3])):
                if board[(j * 7) + i] == turn:
                    heuristic = 100000 * turn
                else:
                    heuristic = -100000 * turn
                return

            # check vertical wins
            if ((j < 3)
                and (board[(j * 7) + i] != 0)
                and (
                    board[(j * 7) + i]
                    == board[((j + 1) * 7) + i]
                    == board[((j + 2) * 7) + i]
                    == board[((j + 3) * 7) + i])):
                if board[(j * 7) + i] == turn:
                    heuristic = 100000 * turn
                else:
                    heuristic = -100000 * turn
                return

        # Verticals

            # two vertical with an empty space on top
            if (1 < j < 6
                and (board[(j * 7) + i] != 0)
                and (
                    board[(j * 7) + i]
                    == board[((j - 1) * 7) + i])
                and (board[((j - 2) * 7) + i] == 0)):
                if board[(j * 7) + i] == turn:
                    heuristic += turn
                else:
                    heuristic -= turn

            # three vertical with an empty space on top
            if (2 < j < 6
                and (board[(j * 7) + i] != 0)
                and (board[(j * 7) + i]
                    == board[((j - 1) * 7) + i]
                    == board[((j - 2) * 7) + i])
                and (board[((j - 3) * 7) + i] == 0)):
                if (board[(j * 7) + i] == turn
                and self.can_place(((j - 3) * 7) + i)
                ):
                    heuristic += 1000 * turn
                elif (board[(j * 7) + i] == turn
                # and not self.can_place(the empty space)
                ):
                    heuristic += 7 * turn
                else:
                # if the player who isn't about to make a move has the
                # advantago_us formation
                    heuristic -= 7 * turn

        # Horizontals and diagonals

            # horizontals
            if i < 4:
                if board[(j * 7) + i] != 0:
                    if (
                    # 1110
                                (
                        (board[(j * 7) + i]
                        == board[(j * 7) + i + 1]
                        == board[(j * 7) + i + 2])
                        and (0
                        == board[(j * 7) + i + 3])
                                )
                    # 1101
                    or (
                        (board[(j * 7) + i]
                        == board[(j * 7) + i + 1]
                        == board[(j * 7) + i + 3])
                        and (0
                        == board[(j * 7) + i + 2])
                                )
                    # 1011
                    or (
                        (board[(j * 7) + i]
                        == board[(j * 7) + i + 2]
                        == board[(j * 7) + i + 3])
                        and (0
                        == board[(j * 7) + i + 1])
                                )
                    ):
                        # each configuration will have one empty space, so
                        # only one of the following IF's OR conditions can
                        # be true. the others will be checking already
                        # filled spaceswhat those spaces are will depend on
                        # which OR in the previous IF condition was true
                        if ((board[(j * 7) + i] == turn)
                            and (
                                self.can_place((j * 7) + i + 1)
                            or self.can_place((j * 7) + i + 2)
                            or self.can_place((j * 7) + i + 3)
                                    )
                        ):
                            heuristic += 1000 * turn
                        elif (board[(j * 7) + i] == turn
                        # and not self.can_place(the empty space)
                        ):
                            heuristic += 7 * turn
                        else:
                        # if the player who isn't about to make a move has
                        # the advantago_us formation
                            heuristic -= 7 * turn
                    if (
                    # 1100
                                (
                        (board[(j * 7) + i]
                        == board[(j * 7) + i + 1])
                        and (0
                        == board[(j * 7) + i + 2]
                        == board[(j * 7) + i + 3])
                                )
                    # 1010
                    or (
                        (board[(j * 7) + i]
                        == board[(j * 7) + i + 2])
                        and (0
                        == board[(j * 7) + i + 1]
                        == board[(j * 7) + i + 3])
                                )
                    # 1001
                    or (
                        (board[(j * 7) + i]
                        == board[(j * 7) + i + 3])
                        and (0
                        == board[(j * 7) + i + 1]
                        == board[(j * 7) + i + 2])
                                )
                    ):
                        if board[(j * 7) + i] == turn:
                            heuristic += turn
                        else:
                            heuristic -= turn
                else:
                    if board[(j * 7) + i + 1] != 0:
                        # 0111
                        if (board[(j * 7) + i + 1]
                            == board[(j * 7) + i + 2]
                            == board[(j * 7) + i + 3]
                        ):
                            if ((board[(j * 7) + i + 1] == turn)
                            and (self.can_place((j * 7) + i))
                            ):
                                heuristic += 1000 * turn
                            elif (board[(j * 7) + i + 1] == turn
                            # and not self.can_place(the empty space)
                            ):
                                heuristic += 7 * turn
                            else:
                            # if the player who isn't about to make a move
                            # has the advantago_us formation
                                heuristic -= 7 * turn
                        if (
                        # 0110
                                    (
                            (board[(j * 7) + i + 1]
                            == board[(j * 7) + i + 2])
                            and (0
                            == board[(j * 7) + i + 3])
                                    )
                        # 0101
                        or (
                            (board[(j * 7) + i + 1]
                            == board[(j * 7) + i + 3])
                            and (0
                            == board[(j * 7) + i + 2])
                                    )
                        ):
                            if board[(j * 7) + i + 1] == turn:
                                heuristic += turn
                            else:
                                heuristic -= turn
                    else:
                        # 0011
                        if ((board[(j * 7) + i + 2] != 0)
                        and (
                                board[(j * 7) + i + 2]
                            == board[(j * 7) + i + 3]
                                    )
                        ):
                            if board[(j * 7) + i + 2] == turn:
                                heuristic += turn
                            else:
                                heuristic -= turn

            # upwards diagonals
            if i < 4 and j > 2:
                if board[(j * 7) + i] != 0:
                    if (
                    # 1110
                                (
                        (board[(j * 7) + i]
                        == board[((j - 1) * 7) + i + 1]
                        == board[((j - 2) * 7) + i + 2])
                        and (0
                        == board[((j - 3) * 7) + i + 3])
                                )
                    # 1101
                    or (
                        (board[(j * 7) + i]
                        == board[((j - 1) * 7) + i + 1]
                        == board[((j - 3) * 7) + i + 3])
                        and (0
                        == board[((j - 2) * 7) + i + 2])
                                )
                    # 1011
                    or (
                        (board[(j * 7) + i]
                        == board[((j - 2) * 7) + i + 2]
                        == board[((j - 3) * 7) + i + 3])
                        and (0
                        == board[((j - 1) * 7) + i + 1])
                                )
                    ):
                        # each scenario will have an empty space, so only
                        # 1 of the following IF's OR conditions can be true
                        # the others will be checking already-filled spaces
                        # what those spaces are will depend on which OR in
                        # the previous IF condition was true
                        if ((board[(j * 7) + i] == turn)
                            and (
                                self.can_place(((j - 3) * 7) + i + 3)
                            or self.can_place(((j - 2) * 7) + i + 2)
                            or self.can_place(((j - 1) * 7) + i + 1)
                                    )
                        ):
                            heuristic += 1000 * turn
                        elif (board[(j * 7) + i] == turn
                        # and not self.can_place(the empty space)
                        ):
                            heuristic += 7 * turn
                        else:
                        # if the player who isn't about to make a move has
                        # the advantago_us formation
                            heuristic -= 7 * turn
                    if (
                    # 1100
                                (
                        (board[(j * 7) + i]
                        == board[((j - 1) * 7) + i + 1])
                        and (0
                        == board[((j - 2) * 7) + i + 2]
                        == board[((j - 3) * 7) + i + 3])
                                )
                    # 1010
                    or (
                        (board[(j * 7) + i]
                        == board[((j - 2) * 7) + i + 2])
                        and (0
                        == board[((j - 1) * 7) + i + 1]
                        == board[((j - 3) * 7) + i + 3])
                                )
                    # 1001
                    or (
                        (board[(j * 7) + i]
                        == board[((j - 3) * 7) + i + 3])
                        and (0
                        == board[((j - 1) * 7) + i + 1]
                        == board[((j - 2) * 7) + i + 2])
                                )
                    ):
                        if board[(j * 7) + i] == turn:
                            heuristic += turn
                        else:
                            heuristic -= turn
                else:
                    if board[((j - 1) * 7) + i + 1] != 0:
                        # 0111
                        if (board[((j - 1) * 7) + i + 1]
                            == board[((j - 2) * 7) + i + 2]
                            == board[((j - 3) * 7) + i + 3]
                        ):
                            if ((board[((j - 1) * 7) + i + 1] == turn)
                            and (self.can_place((j * 7) + i))
                            ):
                                heuristic += 1000 * turn
                            elif (board[((j - 1) * 7) + i + 1] == turn
                            # and not self.can_place(the empty space)
                            ):
                                heuristic += 7 * turn
                            else:
                            # if the player who isn't about to make a move
                            # has the advantago_us formation
                                heuristic -= 7 * turn
                        if (
                        # 0110
                                    (
                            (board[((j - 1) * 7) + i + 1]
                            == board[((j - 2) * 7) + i + 2])
                            and (0
                            == board[((j - 3) * 7) + i + 3])
                                    )
                        # 0101
                        or (
                            (board[((j - 1) * 7) + i + 1]
                            == board[((j - 3) * 7) + i + 3])
                            and (0
                            == board[((j - 2) * 7) + i + 2])
                                    )
                        ):
                            if board[((j - 1) * 7) + i + 1] == turn:
                                heuristic += turn
                            else:
                                heuristic -= turn
                    else:
                        # 0011
                        if ((board[((j - 2) * 7) + i + 2] != 0)
                        and (
                                board[((j - 2) * 7) + i + 2]
                            == board[((j - 3) * 7) + i + 3]
                                    )
                        ):
                            if board[((j - 2) * 7) + i + 2] == turn:
                                heuristic += turn
                            else:
                                heuristic -= turn

            # downwards diagonals
            if i < 4 and j < 3:
                if board[(j * 7) + i] != 0:
                    if (
                    # 1110
                                (
                        (board[(j * 7) + i]
                        == board[((j + 1) * 7) + i + 1]
                        == board[((j + 2) * 7) + i + 2])
                        and (0
                        == board[((j + 3) * 7) + i + 3])
                                )
                    # 1101
                    or        (
                        (board[(j * 7) + i]
                        == board[((j + 1) * 7) + i + 1]
                        == board[((j + 3) * 7) + i + 3])
                        and (0
                        == board[((j + 2) * 7) + i + 2])
                                )
                    # 1011
                    or (
                        (board[(j * 7) + i]
                        == board[((j + 2) * 7) + i + 2]
                        == board[((j + 3) * 7) + i + 3])
                        and (0
                        == board[((j + 1) * 7) + i + 1])
                                )
                    ):
                        # each configuration will have one empty space, so only
                        # one of the following IF's OR conditions can be true
                        # the others will be checking already-filled spaces
                        # what those spaces are will depend on which OR in
                        # the previous IF condition was true
                        if ((board[(j * 7) + i] == turn)
                            and (
                                self.can_place(((j + 3) * 7) + i + 3)
                            or self.can_place(((j + 2) * 7) + i + 2)
                            or self.can_place(((j + 1) * 7) + i + 1)
                                    )
                        ):
                            heuristic += 1000 * turn
                        elif (board[(j * 7) + i] == turn
                        # and not self.can_place(the empty space)
                        ):
                            heuristic += 7 * turn
                        else:
                        # if the player who isn't about to make a move has
                        # the advantago_us formation
                            heuristic -= 7 * turn
                    if (
                    # 1100
                                (
                        (board[(j * 7) + i]
                        == board[((j + 1) * 7) + i + 1])
                        and (0
                        == board[((j + 2) * 7) + i + 2]
                        == board[((j + 3) * 7) + i + 3])
                                )
                    # 1010
                    or (
                        (board[(j * 7) + i]
                        == board[((j + 2) * 7) + i + 2])
                        and (0
                        == board[((j + 1) * 7) + i + 1]
                        == board[((j + 3) * 7) + i + 3])
                                )
                    # 1001
                    or (
                        (board[(j * 7) + i]
                        == board[((j + 3) * 7) + i + 3])
                        and (0
                        == board[((j + 1) * 7) + i + 1]
                        == board[((j + 2) * 7) + i + 2])
                                )
                    ):
                        if board[(j * 7) + i] == turn:
                            heuristic += turn
                        else:
                            heuristic -= turn
                else:
                    if board[((j + 1) * 7) + i + 1] != 0:
                        # 0111
                        if (board[((j + 1) * 7) + i + 1]
                            == board[((j + 2) * 7) + i + 2]
                            == board[((j + 3) * 7) + i + 3]
                        ):
                            if ((board[((j + 1) * 7) + i + 1] == turn)
                            and (self.can_place((j * 7) + i))
                            ):
                                heuristic += (1000 * turn)
                            elif (board[((j + 1) * 7) + i + 1] == turn
                            # and not self.can_place(the empty space)
                            ):
                                heuristic += 7 * turn
                            else:
                            # if the player who isn't about to make a move
                            # has the advantago_us formation
                                heuristic -= 7 * turn
                        if (
                        # 0110
                                    (
                            (board[((j + 1) * 7) + i + 1]
                            == board[((j + 2) * 7) + i + 2])
                        and (board[((j + 3) * 7) + i + 3])
                                    )
                        # 0101
                        or (
                            (board[((j + 1) * 7) + i + 1]
                            == board[((j + 3) * 7) + i + 3])
                        and (0
                            == board[((j + 2) * 7) + i + 2])
                                    )
                        ):
                            if board[((j + 1) * 7) + i + 1] == turn:
                                heuristic += turn
                            else:
                                heuristic -= turn
                    else:
                        # 0011
                        if (
                            (board[((j + 2) * 7) + i + 2] != 0)
                        and (
                                board[((j + 2) * 7) + i + 2]
                            == board[((j + 3) * 7) + i + 3]
                                    )
                        ):
                            if board[((j + 2) * 7) + i + 2] == turn:
                                heuristic += turn
                            else:
                                heuristic -= turn

    # returns heuristic evaluation of position
    # the larger the number, the better the position for player 1
    # the smaller the number, the better the position for player -1
    return heuristic
