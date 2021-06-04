import numpy as np


class Game:
    self.board = np.zeros(42)
    self.over = False
    self.winner = 0

    def getBoard(self):
        return self.board

    def getOver(self):
        return self.over

    def getWinner(self):
        return self.winner

    def printBoard(self):
        # the board is a total of 7 columns wide and 6 rows tall
        # index the board starting from the bottom left
        # so, the bottom left is 0, the bottom right is 6, the top right is 41, etc
        pass

    def canPlace(self):
        pass

    def place(self, spot, turn):
        pass

    def checkForWin(self):
        pass

    def checkForDraw(self):
        pass

    def updateState(self):
        # check for a win and update if there is one
        # check for a draw and update if there is one
        pass

    def getBestMove(self):
        pass


    def miniMax(game, depth):
        # returns the best board state from current given board
        return miniMaxhelp(getGames(game), depth)[1]


    def miniMaxhelp(gameArr, depth):
        for board in gameArr:
            if board.getWinner():  # get winner returns true when there is one winner
                return (1, board, 0)
        if depth == 0:  # reached lowest level get best score
            maxCost = cost(gameArr[0])
            maxboard = gameArr[0]
            for i in range(1, len(gameArr)):  # calculate best board from current possition
                temp = cost(gameArr[i])
                if temp > minCost:
                    maxCost = temp
                    maxboard = gameArr[i]
            return (maxCost, maxboard, 0)  # return best score

        r = (0, gameArr[0], 1)  # first game
        temp = getGames(gameArr[0])
        if (len(temp) != 0):
            # calls minimax for first game in gameArr
            r = miniMaxhelp(temp, depth - 1)
            r = (r[0] * -1, gameArr[0], r[2] + 1)

        for i in range(1, len(gameArr)):  # check for the rest of the game
            temp = getGames(gameArr[i])
            hold = r
            if len(temp) != 0:  # if there are sub games get the best
                hold = miniMaxhelp(temp, depth - 1)
                hold = (hold[0] * -1, gameArr[i], hold[2] + 1)
            else:
                # no possible games assume we tied as we have not won yet
                hold = (0, gameArr[i], 0)

            if (hold[0] > r[0]):  # if new score is better take new score
                r = hold
            elif (hold[0] == r[0]):
                if hold[0] > 0 and hold[2] < r[2]:  # if we are in a winning line take shortest path
                    r = hold
                elif hold[2] > r[2]:  # if we are in a losing line take longest path
                    r = hold
        return r

    def evaluateState(self):
        # if no winner, hard code a way of evaluating board state in a basic way
        pass
