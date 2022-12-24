    def set_select_space_for_la(self, i: int):
        '''
        set_space and select_space for look_ahead function

        Args:
            i (int): _description_
        '''
        j = 0
        while self.board[((j + 1) * 7) + i] == 0:
            j += 1
            if j == 5:
                break
        self.board[(j * 7) + i] = self.turn

    def get_next_moves(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        next_moves = self.next_moves()
        for i in range(7):
            # if space to make a move, # makes a move
            if next_moves[i].board[i] == 0:
                next_moves[i].go_for_la(i)
            else:
                next_moves[i] = 9
        return next_moves

    def next_moves(self):
        '''
        _summary_

        Returns:
            _type_: _description_
        '''
        return [
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self(),
            self.copy_self()
        ]

    def get_best_move(self, depth: int):
        '''
        _summary_

        Args:
            depth (_type_): _description_
        '''
        if depth == 0 or self.result != 0:
            return
        if depth == 1:
            self.look_ahead()
        next_moves = self.next_moves()
        for i in range(7):
            # if space to make a move, makes a move
            if next_moves[i].board[i] == 0:
                next_moves[i].go_for_la(i)
            else:
                next_moves[i] = 9
        for i in range(7):
            if isinstance(next_moves[i], Game):
                self.get_best_move(depth - 1)

    # this should create boards and analyze them
    def minimax(self, depth: int, original_depth: int, alpha, beta):
        '''
        _summary_

        Args:
            depth (int): _description_
            original_depth (int): _description_
            alpha (_type_): _description_
            beta (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if ((depth == 0) or (self.result != 0)):
            return self
        if self.turn == 1:
            max_eval = -np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].minimax(depth - 1, original_depth, alpha, beta)
                    # max() can't run on all potential moves at once because
                    # the number of potential moves will very depending on
                    # whether one or more columns are full
                    if move.heuristic > max_eval:
                        max_eval = move.heuristic
                        best_move = move
                        best_column = i
                    if move.heuristic > alpha:
                        alpha = move.heuristic
                        if beta <= alpha:
                            break
            if depth == original_depth:
                return best_column
            else:
                return best_move
        else:
            min_eval = np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].minimax(depth - 1, original_depth, alpha, beta)
                    if move.heuristic < min_eval:
                        min_eval = move.heuristic
                        best_move = move
                        best_column = i
                    if move.heuristic < beta:
                        beta = move.heuristic
                        if beta <= alpha:
                            break
            if depth == original_depth:
                return best_column
            else:
                return best_move

    def pre_alpha_beta(self, depth: int, original_depth: int):
        '''
        _summary_

        Args:
            depth (_type_): _description_
            original_depth (_type_): _description_

        Returns:
            _type_: _description_
        '''
        if ((depth == 0) or (self.result != 0)):
            return self
        if self.turn == 1:
            max_eval = -np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].pre_alpha_beta(depth - 1, original_depth)
                    # max() can't run on all potential moves at once because
                    # the number of potential moves will very depending on
                    # whether one or more columns are full
                    if move.heuristic > max_eval:
                        max_eval = move.heuristic
                        best_move = move
                        best_column = i
            if depth == original_depth:
                return best_column
            else:
                return best_move
        else:
            min_eval = np.inf
            next_moves = self.next_moves()
            best_move = Game()
            for i in range(7):
                if next_moves[i].board[i] == 0:
                    next_moves[i].go_for_la(i)
                    move = next_moves[i].pre_alpha_beta(depth - 1, original_depth)
                    if move.heuristic < min_eval:
                        min_eval = move.heuristic
                        best_move = move
                        best_column = i
            if depth == original_depth:
                return best_column
            else:
                return best_move