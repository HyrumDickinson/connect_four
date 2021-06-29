import numpy as np

class Game:
    
    # SETUP
    
    def __init__(self):
        # each player is assigned a number: 1 or -1
        # 0 means that no player has been assigned the value
        # Player_1 goes first
        self.turn = 1 # whose turn is it?
            # 1 -> player 1
            # -1 -> player -1
        self.result = 0 # what is the result of the game? 
            # 0 -> undecided
            # 1 -> player 1 win
            # -1 -> player -1 win
            # 3 -> draw
        # the board is a 7 x 6, seven being the horizontal length
        # the indicies begin in the top left corner, and run horizontally 
        # to the right, like you would read a sentence, so,
        # mapping the array to the board squares:      
            # 
            #
            #          0i 1i 2i 3i 4i 5i 6i
            #                   
            #                
            #    0j    0  1  2  3  4  5  6
            #    1j    7  8  9  10 11 12 13
            #    2j    14 15 16 17 18 19 20
            #    3j    21 22 23 24 25 26 27
            #    4j    28 29 30 31 32 33 34
            #    5j    35 36 37 38 39 40 41
            #
            #
        self.board = np.zeros(42, int)
        self.heuristic = 0
        self.lastMove = 7 # what column was the most recent piece placed in?
            # must be between 0 and 6, inclusive
        self.numberOfMoves = 0
                    
    # behold the setters and getters
    def getTurn(self):
        return self.turn
    def setTurn(self, setTurn):
        self.turn = setTurn
    def getResult(self):
        return self.result
    def setResult(self, setResult):
        self.result = setResult
    def getBoard(self):
        return self.board
    def setBoard(self, array):
        npArray = np.array(array)
        self.board = npArray
    def resetGame(self):
        self.turn = 1
        self.result = 0
        self.board = np.zeros(42, int)
        self.heuristic = 0
    def selectSpace(self, i):
        assert (-1 < i < 7), "columns are numbered 0-6"
        assert (self.board[i] == 0), "this column is full"
        j = 0
        while (self.board[((j + 1) * 7) + i] == 0):
            j += 1
            if (j == 5):
                break
        return (j * 7) + i # this is the space
        # set space by index
    def setSpace(self, space, value): 
        assert (-1 < space < 42), "space is out of bounds"    
        self.board[space] = value
        # setSpace and selectSpace for lookAhead function
    def setSelectSpaceForLA(self, i): 
        j = 0
        while (self.board[((j + 1) * 7) + i] == 0):
            j += 1
            if (j == 5):
                break
        self.board[(j * 7) + i] = self.turn
        # set space by column
    def setSpaceI(self, i, value): 
        self.setSpace(self.selectSpace(i), value)
        # set space by coordinates
    def setSpaceIJ(self, i, j, value):# set space by coordinates
        assert (-1 < i < 7), "i is out of bounds"
        assert (-1 < j < 6), "j is out of bounds"
        self.board[(j * 7) + i] = value
        self.printBoard()
    def spaceToString(self, i, j):
        if (self.board[(j * 7) + i] == 0):
            return " 0 "
        if (self.board[(j * 7) + i] == 1):
            return " 1 "
        if (self.board[(j * 7) + i] == -1):
            return "-1 "   
    def getHeuristic(self):
        return self.heuristic
    def setHeuristic(self, setHeuristic):
        self.heuristic = setHeuristic
    
    # print functions in case I need them later
    # printing the board is a bit complicated
    def printTurn(self):
        print(self.turn)
    def printResult(self):
        print(self.result)
    def printBoard(self):
        print(" C0  C1  C2  C3  C4  C5  C6")
        for j in range(6):
            for i in range(7):
                print(self.spaceToString(i, j), end=' ')
            print("\n")
    def printBoardString(self):
        print(self.board)
            
    # GAMEPLAY
    
    # vital function that returns validity of piece placement on space
    def canPlace(self, space):
        assert (-1 < space < 42), "space does not exist; choose between 0-41"
        if not (self.board[space] == 0):
            return False
        elif (34 < space < 42):
            return True
        elif (self.board[space + 7] == 0):
            return False
        else:
            return True
    
    # vital function that returns an array of 
    # all squares where (canPlace == True)
    def getValidMoves(self):
        validMoves = []
        for i in range(42):
            if (self.canPlace(i)):
                validMoves.append(i)
        return validMoves 
     
    # debugging function that prints a visual display of the board 
    # and all legal moves
    def displayValidMoves(self):
        validMoves = self.copySelf()
        for j in range(6):
            for i in range(7):
                if (self.canPlace(i)):
                    validMoves[(j * 7) + i] = 5
        validMoves.printBoard()
    
    
    # vital function that updates self.result. This function works!
    def updateResult(self): 
        for j in range(6):
            for i in range(7):
                # check horizontal wins
                if ((i < 4)
                and (self.board[(j * 7) + i] != 0)
                and        (
                     self.board[(j * 7) + i] 
                  == self.board[(j * 7) + i + 1]
                  == self.board[(j * 7) + i + 2] 
                  == self.board[(j * 7) + i + 3]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return
                # check downwards diagonal wins
                if ((i < 4) and (j < 3)
                and (self.board[(j * 7) + i] != 0) 
                and        (
                     self.board[(j * 7) + i] 
                  == self.board[((j + 1) * 7) + i + 1] 
                  == self.board[((j + 2) * 7) + i + 2] 
                  == self.board[((j + 3) * 7) + i + 3]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return    
                # check upwards diagonal wins
                if ((i < 4) and (j > 2)
                and (self.board[(j * 7) + i] != 0) 
                and        (
                     self.board[(j * 7) + i] 
                  == self.board[((j - 1) * 7) + i + 1] 
                  == self.board[((j - 2) * 7) + i + 2] 
                  == self.board[((j - 3) * 7) + i + 3]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return
                # check vertical wins
                if ((j < 3)
                and (self.board[(j * 7) + i] != 0) 
                and        (
                     self.board[(j * 7) + i] 
                  == self.board[((j + 1) * 7) + i] 
                  == self.board[((j + 2) * 7) + i] 
                  == self.board[((j + 3) * 7) + i]
                            )
                ):
                    self.result = self.board[(j * 7) + i]
                    return
        # if no wins are found, self.result = 0is set to 0. 
        # This could be useful if I decide to integrate move takebacks
        
        # check draw (i.e. is the board full)
        for j in range(6):
            for i in range(7):
                if (self.board[(j * 7) + i] == 0):
                    return 
        self.result = 3
        
    # vital function that explains result status
    def displayResult(self):
        if (self.result == 1): 
            print("Player 1 wins!")
        elif (self.result == -1):
            print("Player -1 wins!")
        elif (self.result == 3):
            print("This game is a draw!")
        elif (self.result == 0):
            print("This game remains in progress")
        else:
            print("error: result has been set to an invalid value")
    
    # debugging function that prints why you can't place on space
    def whyCantPlace(self, space):
        if (self.canPlace(space)):
            print("you can place here!")
        else:
            if (space != 0):
                print("this space is occupied")
            if (space + 7 == 0):
                print("this space lies above an empty space; piece will drop")
     
    # INTELLIGENCE
    # to do:
        # heuristic function -> rates positions
        # minimax function -> searches all possible moves to specified depth
        #                     applies heuristic function
        #                     works backward to create best position, 
        #                     assuming opponent perfect play
        # alpha-beta function -> I'll have to re-read up on this
      
        
        # make this an independent class?
    
    def updateHeuristic(self):
        
        self.heuristic = 0
        # player 1 will earn positive points
        # player 2 will earn negative points
        
        for j in range(6):
            for i in range(7):
                
            # Wins
            
                # check horizontal wins
                if ((i < 4)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[(j * 7) + i + 1]
                  == self.board[(j * 7) + i + 2]
                  == self.board[(j * 7) + i + 3]
                           )
                ):
                    if (self.board[(j * 7) + i] == self.turn):
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return
                
                # check downwards diagonal wins
                if ((i < 4) and (j < 3)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j + 1) * 7) + i + 1]
                  == self.board[((j + 2) * 7) + i + 2]
                  == self.board[((j + 3) * 7) + i + 3]
                           )
                ):
                    if (self.board[(j * 7) + i] == self.turn):
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return    
                
                # check upwards diagonal wins
                if ((i < 4) and (j > 2)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j - 1) * 7) + i + 1]
                  == self.board[((j - 2) * 7) + i + 2]
                  == self.board[((j - 3) * 7) + i + 3]
                           )
                ):
                    if (self.board[(j * 7) + i] == self.turn):
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return
                
                # check vertical wins
                if ((j < 3)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j + 1) * 7) + i]
                  == self.board[((j + 2) * 7) + i]
                  == self.board[((j + 3) * 7) + i]
                           )
                ):
                    if (self.board[(j * 7) + i] == self.turn):
                        self.heuristic = 100000 * self.turn
                    else:
                        self.heuristic = -100000 * self.turn
                    return
                
            # Verticals
                
                # two vertical with an empty space on top
                if ((1 < j < 6)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i] 
                  == self.board[((j - 1) * 7)+ i]
                           )
                and (self.board[((j - 2) * 7) + i] == 0)
                ):
                    if (self.board[(j * 7) + i] == self.turn):
                        self.heuristic += self.turn
                    else:
                        self.heuristic -= self.turn
                        
                # three vertical with an empty space on top
                if ((2 < j < 6)
                and (self.board[(j * 7) + i] != 0)
                and       (
                     self.board[(j * 7) + i]
                  == self.board[((j - 1) * 7)+ i]
                  == self.board[((j - 2) * 7)+ i]
                           )
                and (self.board[((j - 3) * 7) + i] == 0)
                ):
                    if (self.board[(j * 7) + i] == self.turn
                    and self.canPlace(((j - 3) * 7) + i)
                    ):
                        self.heuristic += 1000 * self.turn
                    elif (self.board[(j * 7) + i] == self.turn
                    # and not self.canPlace(the empty space)
                    ):
                        self.heuristic += 7 * self.turn
                    else:
                    # if the player who isn't about to make a move has the 
                    # advantagous formation
                        self.heuristic -= 7 * self.turn
        
            # Horizontals and diagonals
                
                # horizontals
                if (i < 4):
                    if (self.board[(j * 7) + i] != 0):
                        if (
                        # 1110
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 2])
                         and (0
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1101
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 1] 
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 2])
                                   )
                        # 1011
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 2]
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 1])
                                   )
                        ):
                            # each configuration will have one empty space, so
                            # only one of the following IF's OR conditions can 
                            # be true. the others will be checking already
                            # filled spaceswhat those spaces are will depend on  
                            # which OR in the previous IF condition was true
                            if ((self.board[(j * 7) + i] == self.turn)
                             and      (
                                 self.canPlace((j * 7) + i + 1)     
                              or self.canPlace((j * 7) + i + 2)     
                              or self.canPlace((j * 7) + i + 3)
                                       )    
                            ):                                      
                                self.heuristic += 1000 * self.turn       
                            elif (self.board[(j * 7) + i] == self.turn
                            # and not self.canPlace(the empty space)
                            ):
                                self.heuristic += 7 * self.turn
                            else:
                            # if the player who isn't about to make a move has 
                            # the advantagous formation
                                self.heuristic -= 7 * self.turn
                        if (
                        # 1100 
                                  (
                            (self.board[(j * 7) + i] 
                          == self.board[(j * 7) + i + 1])
                         and (0 
                          == self.board[(j * 7) + i + 2] 
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1010
                        or        (
                            (self.board[(j * 7) + i] 
                          == self.board[(j * 7) + i + 2])
                         and (0 
                          == self.board[(j * 7) + i + 1] 
                          == self.board[(j * 7) + i + 3])
                                   )
                        # 1001
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[(j * 7) + i + 3])
                         and (0
                          == self.board[(j * 7) + i + 1]
                          == self.board[(j * 7) + i + 2])
                                   )
                        ):
                            if (self.board[(j * 7) + i] == self.turn):
                                self.heuristic += self.turn
                            else:
                                self.heuristic -= self.turn
                    else: # if (self.board[(j * 7) + i] == 0):
                        if (self.board[(j * 7) + i + 1] != 0):
                            # 0111
                            if (self.board[(j * 7) + i + 1]
                             == self.board[(j * 7) + i + 2]
                             == self.board[(j * 7) + i + 3]
                            ):
                                if ((self.board[(j * 7) + i + 1] == self.turn)
                                and (self.canPlace((j * 7) + i))
                                ):                                 
                                    self.heuristic += 1000 * self.turn    
                                elif (self.board[(j * 7) + i + 1] == self.turn
                                # and not self.canPlace(the empty space)
                                ):
                                    self.heuristic += 7 * self.turn
                                else:
                                # if the player who isn't about to make a move 
                                # has the advantagous formation
                                    self.heuristic -= 7 * self.turn
                            if (
                            # 0110
                                      (
                                (self.board[(j * 7) + i + 1]
                              == self.board[(j * 7) + i + 2])
                             and (0 
                              == self.board[(j * 7) + i + 3])
                                       )
                            # 0101
                            or        (
                                (self.board[(j * 7) + i + 1]
                              == self.board[(j * 7) + i + 3])
                             and (0 
                              == self.board[(j * 7) + i + 2])
                                       )
                            ):
                                if (self.board[(j * 7) + i + 1] == self.turn):
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                        else: # if (self.board[(j * 7) + i + 1] == 0):
                            # 0011
                            if ((self.board[(j * 7) + i + 2] != 0)
                            and       (
                                 self.board[(j * 7) + i + 2]
                              == self.board[(j * 7) + i + 3]
                                       )
                            ):
                                if (self.board[(j * 7) + i + 2] == self.turn):
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                
                # upwards diagonals
                if ((i < 4) and (j > 2)):
                    if (self.board[(j * 7) + i] != 0):
                        if (
                        # 1110
                                   (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 2) * 7) + i + 2])
                         and (0
                          == self.board[((j - 3) * 7) + i + 3])
                                    )
                        # 1101
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 1) * 7) + i + 1]
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0
                          == self.board[((j - 2) * 7) + i + 2])
                                   )
                        # 1011
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j - 2) * 7) + i + 2]
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0
                          == self.board[((j - 1) * 7) + i + 1])
                                   )
                        ):
                            # each scenario will have an empty space, so only
                            # 1 of the following IF's OR conditions can be true
                            # the others will be checking already-filled spaces
                            # what those spaces are will depend on which OR in 
                            # the previous IF condition was true
                            if ((self.board[(j * 7) + i] == self.turn)
                             and      (
                                 self.canPlace(((j - 3) * 7) + i + 3)
                              or self.canPlace(((j - 2) * 7) + i + 2)
                              or self.canPlace(((j - 1) * 7) + i + 1)
                                      )
                            ): 
                                self.heuristic += 1000 * self.turn
                            elif (self.board[(j * 7) + i] == self.turn
                            # and not self.canPlace(the empty space)
                            ):
                                self.heuristic += 7 * self.turn
                            else:
                            # if the player who isn't about to make a move has 
                            # the advantagous formation
                                self.heuristic -= 7 * self.turn
                        if (
                        # 1100 
                                  (
                            (self.board[(j * 7) + i] 
                          == self.board[((j - 1) * 7) + i + 1])
                         and (0 
                          == self.board[((j - 2) * 7) + i + 2] 
                          == self.board[((j - 3) * 7) + i + 3])
                                   )
                        # 1010
                        or        (
                            (self.board[(j * 7) + i] 
                          == self.board[((j - 2) * 7) + i + 2])
                         and (0 
                          == self.board[((j - 1) * 7) + i + 1] 
                          == self.board[((j - 3) * 7) + i + 3])
                                   )
                        # 1001
                        or        (
                            (self.board[(j * 7) + i] 
                          == self.board[((j - 3) * 7) + i + 3])
                         and (0 
                          == self.board[((j - 1) * 7) + i + 1] 
                          == self.board[((j - 2) * 7) + i + 2])
                                   )
                        ):
                            if (self.board[(j * 7) + i] == self.turn):
                                self.heuristic += self.turn
                            else:
                                self.heuristic -= self.turn
                    else: # if (self.board[(j * 7) + i] == 0):
                        if (self.board[((j - 1) * 7) + i + 1] != 0):
                            # 0111
                            if ( self.board[((j - 1) * 7) + i + 1]
                              == self.board[((j - 2) * 7) + i + 2] 
                              == self.board[((j - 3) * 7) + i + 3]
                            ):
                                if ((self.board[((j - 1) * 7) + i + 1] == self.turn)
                                and (self.canPlace((j * 7) + i))
                                ):                                 
                                    self.heuristic += 1000 * self.turn    
                                elif (self.board[((j - 1) * 7) + i + 1] == self.turn
                                # and not self.canPlace(the empty space)
                                ):
                                    self.heuristic += 7 * self.turn
                                else:
                                # if the player who isn't about to make a move 
                                # has the advantagous formation
                                    self.heuristic -= 7 * self.turn
                            if (
                            # 0110 
                                      (
                                (self.board[((j - 1) * 7) + i + 1] 
                              == self.board[((j - 2) * 7) + i + 2])
                             and (0 
                              == self.board[((j - 3) * 7) + i + 3])
                                       )
                            # 0101
                            or        (
                                (self.board[((j - 1) * 7) + i + 1] 
                              == self.board[((j - 3) * 7) + i + 3])
                             and (0 
                              == self.board[((j - 2) * 7) + i + 2])
                                       )
                            ):
                                if (self.board[((j - 1) * 7) + i + 1] == self.turn):
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                        else: # if (self.board[((j - 1) * 7) + i + 1] == 0):
                            # 0011
                            if ((self.board[((j - 2) * 7) + i + 2] != 0)
                            and       (
                                 self.board[((j - 2) * 7) + i + 2] 
                              == self.board[((j - 3) * 7) + i + 3]
                                       )
                            ):
                                if (self.board[((j - 2) * 7) + i + 2] == self.turn):
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                            
                # downwards diagonals
                if ((i < 4) and (j < 3)):
                    if (self.board[(j * 7) + i] != 0):
                        if (
                        # 1110
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 2) * 7) + i + 2])
                         and (0
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1101
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 3) * 7) + i + 3])
                         and (0
                          == self.board[((j + 2) * 7) + i + 2])
                                   )
                        # 1011
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 2) * 7) + i + 2]
                          == self.board[((j + 3) * 7) + i + 3])
                         and (0 
                          == self.board[((j + 1) * 7) + i + 1])
                                   )
                        ):
                            # each configuration will have one empty space, so only
                            # one of the following IF's OR conditions can be true
                            # the others will be checking already-filled spaces
                            # what those spaces are will depend on which OR in 
                            # the previous IF condition was true
                            if ((self.board[(j * 7) + i] == self.turn)
                             and       (
                                 self.canPlace(((j + 3) * 7) + i + 3)
                              or self.canPlace(((j + 2) * 7) + i + 2)
                              or self.canPlace(((j + 1) * 7) + i + 1)
                                        )
                            ): 
                                self.heuristic += 1000 * self.turn
                            elif (self.board[(j * 7) + i] == self.turn
                            # and not self.canPlace(the empty space)
                            ):
                                self.heuristic += 7 * self.turn
                            else:
                            # if the player who isn't about to make a move has 
                            # the advantagous formation
                                self.heuristic -= 7 * self.turn
                        if (
                        # 1100 
                                  (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 1) * 7) + i + 1])
                         and (0
                          == self.board[((j + 2) * 7) + i + 2]
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1010
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 2) * 7) + i + 2])
                         and (0
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 3) * 7) + i + 3])
                                   )
                        # 1001
                        or        (
                            (self.board[(j * 7) + i]
                          == self.board[((j + 3) * 7) + i + 3])
                         and (0
                          == self.board[((j + 1) * 7) + i + 1]
                          == self.board[((j + 2) * 7) + i + 2])
                                   )
                        ):
                            if (self.board[(j * 7) + i] == self.turn):
                                self.heuristic += self.turn
                            else:
                                self.heuristic -= self.turn
                    else: # if (self.board[(j * 7) + i] == 0):
                        if (self.board[((j + 1) * 7) + i + 1] != 0):
                            # 0111
                            if (self.board[((j + 1) * 7) + i + 1]
                             == self.board[((j + 2) * 7) + i + 2]
                             == self.board[((j + 3) * 7) + i + 3]
                            ):
                                if ((self.board[((j + 1) * 7) + i + 1] == self.turn)
                                and (self.canPlace((j * 7) + i))
                                ):                                 
                                    self.heuristic += (1000 * self.turn)     
                                elif (self.board[((j + 1) * 7) + i + 1] == self.turn
                                # and not self.canPlace(the empty space)
                                ):
                                    self.heuristic += 7 * self.turn
                                else:
                                # if the player who isn't about to make a move 
                                # has the advantagous formation
                                    self.heuristic -= 7 * self.turn
                            if (
                            # 0110
                                      (
                                (self.board[((j + 1) * 7) + i + 1]
                              == self.board[((j + 2) * 7) + i + 2])
                            and (self.board[((j + 3) * 7) + i + 3])
                                       )
                            # 0101
                            or        (
                                (self.board[((j + 1) * 7) + i + 1] 
                              == self.board[((j + 3) * 7) + i + 3])
                            and (0 
                              == self.board[((j + 2) * 7) + i + 2])
                                       )
                            ):
                                if (self.board[((j + 1) * 7) + i + 1] == self.turn):
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                        else: # if (self.board[((j + 1) * 7) + i + 1] == 0):
                            # 0011
                            if (
                                (self.board[((j + 2) * 7) + i + 2] != 0)
                            and       (
                                 self.board[((j + 2) * 7) + i + 2]
                              == self.board[((j + 3) * 7) + i + 3]
                                       )
                            ):
                                if (self.board[((j + 2) * 7) + i + 2] == self.turn):
                                    self.heuristic += self.turn
                                else:
                                    self.heuristic -= self.turn
                            
        # returns heuristic evaluation of position  
        # the larger the number, the better the position for player 1
        # the smaller the number, the better the position for player -1
        return self.heuristic
        
    def displayHeuristic(self):
        if (self.heuristic == 100000):
            print ("heuristic: infinity")
        elif (self.heuristic == -100000):
            print ("heuristic: -infinity")
        else:
            print("heuristic: " + str(self.heuristic))
        
    def copySelf(self):
        copy = Game()
        copy.board = np.array([i for i in self.board])
        copy.turn = self.turn
        copy.result = self.result
        copy.heuristic = self.heuristic
        return copy
    
    def getNextMoves(self): # isinstance(game, Game())
        nextMoves = [self.copySelf(), self.copySelf(), 
                     self.copySelf(), self.copySelf(), 
                     self.copySelf(), self.copySelf(), 
                     self.copySelf()]
        for i in range(7):
            if nextMoves[i].board[i] == 0: # if space to make a move, 
               nextMoves[i].goForLA(i)     # makes a move
            else:
               nextMoves[i] = 9   
        return nextMoves
        
    def getBestMove(self, depth): # isinstance(game, Game())
        if ((depth == 0) or (self.result != 0)):
            return
        if (depth == 1):
            self.lookAhead()
        nextMoves = [self.copySelf(), self.copySelf(), 
                     self.copySelf(), self.copySelf(), 
                     self.copySelf(), self.copySelf(), 
                     self.copySelf()]
        for i in range(7):
                if nextMoves[i].board[i] == 0: # if space to make a move, 
                   nextMoves[i].goForLA(i)     # makes a move
                else:
                   nextMoves[i] = 9  
        for i in range(7):
            if (isinstance(nextMoves[i], Game())):
                self.getBestMove(nextMoves[i], depth - 1)
    
    def minimax(self, depth, originalDepth, alpha, beta):
        if ((depth == 0) or (self.result != 0)):
            return self
        if self.turn == 1:
            maxEval = -np.inf
            nextMoves = [self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf()]
            bestMove = Game()
            for i in range(7):
                if nextMoves[i].board[i] == 0: # if space to make a move, 
                   nextMoves[i].goForLA(i)     # makes a move
                   move = nextMoves[i].minimax(depth - 1, originalDepth, alpha, beta)
                   # max() can't run on all potential moves at once because 
                   # the number of potential moves will very depending on
                   # whether one or more columns are full
                   if (move.heuristic > maxEval):
                       maxEval = move.heuristic
                       bestMove = move
                       bestColumn = i
                   if (move.heuristic > alpha):
                       alpha = move.heuristic
                       if (beta <= alpha):
                           break
            if (depth == originalDepth):
                return bestColumn
            else:
                return bestMove
        else:
            minEval = np.inf
            nextMoves = [self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf()]
            bestMove = Game()
            for i in range(7):
                if nextMoves[i].board[i] == 0: # if space to make a move, 
                   nextMoves[i].goForLA(i)     # makes a move
                   move = nextMoves[i].minimax(depth - 1, originalDepth, alpha, beta)
                   if (move.heuristic < minEval):
                       minEval = move.heuristic
                       bestMove = move
                       bestColumn = i
                   if (move.heuristic < beta):
                       beta = move.heuristic
                       if (beta <= alpha):
                           break
            if (depth == originalDepth):
                return bestColumn
            else:
                return bestMove
            
    def preAlphaBeta(self, depth, originalDepth):
        if ((depth == 0) or (self.result != 0)):
            return self
        if self.turn == 1:
            maxEval = -np.inf
            nextMoves = [self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf()]
            bestMove = Game()
            for i in range(7):
                if nextMoves[i].board[i] == 0: # if space to make a move, 
                   nextMoves[i].goForLA(i)     # makes a move
                   move = nextMoves[i].preAlphaBeta(depth - 1, originalDepth)
                   # max() can't run on all potential moves at once because 
                   # the number of potential moves will very depending on
                   # whether one or more columns are full
                   if (move.heuristic > maxEval):
                       maxEval = move.heuristic
                       bestMove = move
                       bestColumn = i
            if (depth == originalDepth):
                return bestColumn
            else:
                return bestMove
        else:
            minEval = np.inf
            nextMoves = [self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf()]
            bestMove = Game()
            for i in range(7):
                if nextMoves[i].board[i] == 0: # if space to make a move, 
                   nextMoves[i].goForLA(i)     # makes a move
                   move = nextMoves[i].preAlphaBeta(depth - 1, originalDepth)
                   if (move.heuristic < minEval):
                       minEval = move.heuristic
                       bestMove = move
                       bestColumn = i
            if (depth == originalDepth):
                return bestColumn
            else:
                return bestMove
    
        # looks one move ahead and chooses the best move based on heuristic 
    def lookAhead(self): # isinstance(self, Game())
        assert (self.result == 0), "cannot calculate future moves on a finished game"
        # possibleMoves is a 7-index array of games, 
        # each index representing the board state if 
        # a move is made in the column with the 
        # same i-number as the array index
        possibleMoves = [self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf(), self.copySelf(), 
                         self.copySelf()]
        # sets start to correspond to something valid
        # creates an initial best, which will be updated 
        # each time it is compared with another move
        # plays move where move plays are valid, 
        # marks columns where plays are not valid
        for i in range(7):
            if possibleMoves[i].board[i] == 0: # if space to make a move, 
               possibleMoves[i].goForLA(i)     # makes a move
               if self.turn == 1:
                   bestHeuristic = -np.inf
                   if (possibleMoves[i].heuristic > bestHeuristic):
                        bestHeuristic = possibleMoves[i]
                        bestColumn = i
               else:
                   bestHeuristic = np.inf
                   if (possibleMoves[i].heuristic < bestHeuristic):
                        bestHeuristic = possibleMoves[i]
                        bestColumn = i
        # bestMove, the position, exists for comparison against other positions
        # bestColumn, the column, exists to be returned 
        # after all comparisons are completed
        return bestColumn
    
    # checks to see if both players have made at least one move
    # if not, returns True
    def isFirstTurns(self):
        oneMove = False
        twoMoves = False
        for i in range(42):
            if (self.board[i] != 0):
                if (oneMove == False):
                    twoMoves = True
                else:
                    oneMove = True
        return not twoMoves
    
    # plays a random non-side move for a first turn
    def playFirstTurn(self):
        self.goU(np.random.randint(1,5))
    
    # plays two random non-side moves. designed to start games where both sides
    # are played by robots
    def playFirstTurns(self):
        self.goU(np.random.randint(1,5))
        self.goU(np.random.randint(1,5))
        
    def displayInfo(self):
        self.displayResult()
        self.printBoard()
        self.displayHeuristic()
    
    # human plays one turn; computer displays result and information about game
    def goU(self, i):
        assert (self.result == 0), "this game is over! you can't place pieces anymore."
        self.setSpace(self.selectSpace(i), self.turn)
        if (self.turn == -1):
            self.numberOfMoves += 1
        self.turn = np.negative(self.turn)
        # print(" ")
        # self.updateHeuristic()
        # self.displayHeuristic()
        # self.printBoard()
        self.updateResult()
        # self.displayResult()
        # print(" ")
    
    # computer plays the pre-alpha-beta minimax recommended turn
    def goPreAB(self, depth):
        if self.isFirstTurns():
            self.playFirstTurn()
        else: 
            self.goU(self.preAlphaBeta(depth, depth))
    
    # plays one turn for lookAhead function
    def goForLA(self, i):
        self.setSelectSpaceForLA(i)
        self.turn = np.negative(self.turn)
        self.updateResult()
        self.updateHeuristic()
    
    # computer plays the minimax-recommended turn
    def goMinimax(self, depth):
        assert (depth > 0), "minimax cannot search to a depth less than one"
        if self.isFirstTurns():
            self.playFirstTurn()
        else: 
            self.goU(self.minimax(depth, depth, -np.inf, np.inf))
        
    # computer plays minimax-recommended turn for turns number of turns, switching between sides
    def goMinimaxxX(self, depth, turns):
        for i in range(turns):
            if (self.result != 0):
               self.resetGame()
               break
            if self.isFirstTurns():
               self.playFirstTurn()
            else: 
               self.goMinimax(depth)
            
    # computer plays the heuristic-recommended turn
    def goHeuristic(self):
        if self.isFirstTurns():
            self.playFirstTurn()
        else: 
            self.goU(self.lookAhead())
    
    # computer plays heuristic-recommended turn for turns number of turns, switching between sides
    def goHeuristicxX(self, turns):
        for i in range(turns):
            if (self.result != 0):
               self.resetGame()
               break
            if self.isFirstTurns():
               self.playFirstTurn()
            else: 
               self.goHeuristic()
    
    # computer plays a random turn
    def goRandom(self):
        column = np.random.randint(0, 6)
        while (self.board[column] != 0):
            column = np.random.randint(0, 6)
        self.goU(column)
    
    # computer plays random turn for turns number of turns, switching between sides
    def goRandomxX(self, turns):
        for i in range(turns):
            if (self.result != 0):
               self.resetGame()
               break
               self.goRandom()
    
    # human plays a move
    def goHuman(self):
        print("input an integer between 0 and 6, inclusive")
        column = int(input("which column do you choose to place your piece in? "))
        while not(column == 0
                    or column == 1
                    or column == 2
                    or column == 3
                    or column == 4
                    or column == 5
                    or column == 6):
            column = int(input("that was not an integer between 0 and 6. try again: "))
        self.goU(column)
            
    
    # human plays a game versus a computer opponent
    def playGame(self):
        isHumanFirst = np.random.choice([True, False])
        if (isHumanFirst == True):
            print("You are player 1")
        else:
            print("You are player 2")
        print(" ")
        print("input an integer between 0 and 3, inclusive")
        level = int(input("which strength AI do you choose to play against? "))
        while not (level == 0
                    or level == 1
                    or level == 2
                    or level == 3
                    or level == 4
                    or level == 5
                    or level == 6):
            level = int(input("that was not an integer between 0 and 6. try again: "))
        self.printBoard()
        if (isHumanFirst == True):
            self.goHuman()
            self.playFirstTurn()
            self.goHuman()
        else:
            self.playFirstTurn()
            self.goHuman()
        if (level == 0):
            while (self.result == 0):
                self.goRandom()
                if (self.result != 0):
                    self.resetGame()
                    return
                self.goHuman()
        else:
            while (self.result == 0):
                self.goMinimax(level)
                if (self.result != 0):
                    self.resetGame()
                    return
                self.goHuman()
                
    # preAB plays a game against itself
    def preABVsPreAB(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goPreAB(depth)
        self.resetGame()
    
    # preAB plays a game against Minimax
    def preABVsMinimax(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goPreAB(depth)
            if (self.result != 0):
                break
            self.goMinimax(depth)
        self.resetGame()
    
    # Minimax plays a game against preAB
    def minimaxVsPreAB(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goMinimax(depth)
            if (self.result != 0):
                break
            self.goPreAB(depth)
        self.resetGame()
        
    # single function for all computer vs computer matchups
    def compMatchup(self, player1_level, player2_level):
        self.resetGame()
        assert ((-1 < player1_level < 7) 
            and (-1 < player2_level < 7)), "AI levels go from zero to six"
        self.playFirstTurns()
        if (player1_level == 0 and player2_level == 0):
            while (self.result == 0):
                self.goRandom()
        elif (player1_level == 0 and player2_level != 0):
            while (self.result == 0):
                self.goRandom()
                if (self.result != 0):
                    break
                self.goMinimax(player2_level)
        elif (player1_level != 0 and player2_level == 0):
            while (self.result == 0):
                self.goMinimax(player1_level)
                if (self.result != 0):
                    break
                self.goRandom()
        else: # if (player1_level != 0 and player2_level != 0)
            while (self.result == 0):
                self.goMinimax(player1_level)
                if (self.result != 0):
                    break
                self.goMinimax(player2_level)
        # if (self.result == 1):
        #     print("The level " + str(player1_level) + " player, who went \
        #     first, beat the level " + str(player2_level) + " player in " \
        #     + str(self.numberOfMoves) + " moves.")
        # else:   
        #     print("The level " + str(player2_level) + " player, who went \
        #     second, beat the level " + str(player1_level) + " player in "\
        #     + str(self.numberOfMoves) + " moves.")
        return self.result
    
    # plays games of a specified computer vs computer matchup and returns each 
    # player's win percentage
    def compMatchupUltra(self, player1_level, player2_level, numberOfGames):
        winIndex = np.zeros(numberOfGames, int)
        winPercentage = 0
        drawPercentage = 0
        for i in range(numberOfGames):
            winIndex[i] = self.compMatchup(player1_level, player2_level)
            if (winIndex[i] == 1):
                winPercentage += 1
            elif (winIndex[i] == 3):
                drawPercentage += 1
            print("game " + str(i) + "     result: " + str(winIndex[i]))
        winPercentage = int(winPercentage) * (100 / int(numberOfGames))
        drawPercentage = int(drawPercentage) * (100 / int(numberOfGames))
        print("In " + str(numberOfGames) + " games, the level " \
              + str(player1_level) + " player, who went first, \
              beat the level " + str(player2_level) + " player " \
              + str(winPercentage) + "% of the time. " + str(drawPercentage) \
              + "% of the games were draws.")
    
    # Minimax plays a game against Minimax
    def minimaxVsMinimax(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goMinimax(depth)
        self.resetGame()
    
    # Minimax plays a game against Minimax with different search depth
    def minimaxVsMinimax2(self, depth1, depth2):
        self.playFirstTurns()
        while (self.result == 0):
            self.goMinimax(depth1)
            if (self.result != 0):
                break
            self.goMinimax(depth2)
        self.resetGame()
    
    # Minimax plays a game against Heuristic
    def minimaxVsHeuristic(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goMinimax(depth)
            if (self.result != 0):
                break
            self.goHeuristic()
        self.resetGame()
    
    # Minimax plays a game against Random
    def minimaxVsRandom(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goMinimax(depth)
            if (self.result != 0):
                break
            self.goRandom()
        self.resetGame()
    
    # Heuristic plays a game against Minimax
    def heuristicVsMinimax(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goHeuristic()
            if (self.result != 0):
                break
            self.goMinimax(depth)
        self.resetGame()
    
    # Heuristic plays a game against Heuristic
    def heuristicVsHeuristic(self): 
        self.playFirstTurns()
        while (self.result == 0):
            self.goHeuristic()
        self.resetGame()
    
    # Heuristic plays a game against Random
    def heuristicVsRandom(self):
        self.playFirstTurns()
        while (self.result == 0):
            self.goHeuristic()
            if (self.result != 0):
                break
            self.goRandom()
        self.resetGame()
    
    # Random plays a game against Minimax
    def randomVsMinimax(self, depth):
        self.playFirstTurns()
        while (self.result == 0):
            self.goRandom()
            if (self.result != 0):
                break
            self.goMinimax(depth)
        self.resetGame()
    
    # Random plays a game against Heuristic
    def randomVsHeuristic(self):
        self.playFirstTurns()
        while (self.result == 0):
            self.goRandom()
            if (self.result != 0):
                break
            self.goHeuristic()
        self.resetGame()
    
    # Random plays a game against Random
    def randomVsRandom(self):
        while (self.result == 0):
            self.goRandom()
        self.resetGame()
    
            
        
g = Game()
    
