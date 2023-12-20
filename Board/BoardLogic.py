import numpy as np

from Board.BoardMoveDetails import BoardTurnDetails
from GameSettings.DefaultSettings import *
import copy


class BasicBoardLogic:
    def __init__(self, board_row=3, board_col=3, number_score_to_win=3):
        self._number_of_turn = 0
        self.board_row = board_row
        self.board_col = board_col
        self.number_score_to_win = number_score_to_win
        self.square_size = board_width // self.board_row
        # Create an array which filled with "0"
        self._squares = np.zeros((board_row, board_col))
        # This array contain all the squares that are marked
        self._listMarked = []
        self._winningLine = None

    # Mark squares action
    def markSquare(self, playerId, row, col):
        # Mark the squares that was checked to be from playerId, so the board can only have
        # 2 numerical value which represent each player, imagine a random matrix of bit
        self._squares[row][col] = playerId
        self._number_of_turn += 1
        self._listMarked.append(BoardTurnDetails(playerId, row, col))

    # Get board winning state, return playerId if it has won player else return 0
    def getWinningState(self):
        # The logic is: check the last turn data, then use checkLineFromPos to determined if the game is won or not
        if len(self._listMarked) == 0:
            return 0
        lastTurn = self._listMarked[-1]
        playerId = lastTurn.playerId
        row, col = lastTurn.position
        # Take the isWinning bool
        if self.checkLineFromPos(playerId, row, col, 1, 0)[0] \
                or self.checkLineFromPos(playerId, row, col, 0, 1)[0] \
                or self.checkLineFromPos(playerId, row, col, 1, 1)[0] \
                or self.checkLineFromPos(playerId, row, col, 1, -1)[0]:
            return playerId
        return 0

    # Checking from position

    # Each time Inputting a move, invoke markSquare (in BoardGUI), which in turn, invoke getWinningStates, which invokes this (checkLineFromPos)
    # Fine logic; After inputting in a move (I assumed), Taking that move as the position to
    # be checked! Changerow, changeCol value can be either 1, 0, represent the directions
    # If count > score (3 or 5) => Win! 


    def checkLineFromPos(self, playerId, row, col, changeRow, changeCol):
        # Get before squares from pos
        tempRow = row - changeRow
        tempCol = col - changeCol
        count = 1
        # Holding Initial position
        startPoint = (row, col)

        # While it is valid & it is from the same player 
        while self.isValidateRowCol(tempRow, tempCol) and self._squares[tempRow][tempCol] == playerId:
            count += 1
            startPoint = (tempRow, tempCol)
            tempRow -= changeRow
            tempCol -= changeCol

        # Get after squares from pos
        tempRow = row + changeRow
        tempCol = col + changeCol
        endPoint = (row, col)
        while self.isValidateRowCol(tempRow, tempCol) and self._squares[tempRow][tempCol] == playerId:
            count += 1
            endPoint = (tempRow, tempCol)
            tempRow += changeRow
            tempCol += changeCol

        # If win, save startPoint and endPoint of winning line
        isWinning = count >= self.number_score_to_win
        if isWinning:
            self._winningLine = (startPoint, endPoint)
        return isWinning, count

    # Get empty squares that didn't mark by player
    def getEmptySquares(self):
        emptySqrs = []
        [emptySqrs.append((row, col)) for row in range(self.board_row)
         for col in range(self.board_col) if self._squares[row][col] == 0]
        return emptySqrs

    def getNeighborEmptySquares(self, pos_x, pos_y):
        neightBorSqrs = []
        [neightBorSqrs.append((row, col)) for row in range(pos_x - 1, pos_x + 2) \
         for col in range(pos_y - 1, pos_y + 2) if self.isValidateRowCol(row, col)
         and self._squares[row][col] == 0]
        return neightBorSqrs

    def getScoreOfPosition(self, playerId, row, col):
        return max(self.checkLineFromPos(playerId, row, col, 1, 0)[1],
                   self.checkLineFromPos(playerId, row, col, 0, 1)[1],
                   self.checkLineFromPos(playerId, row, col, 1, 1)[1],
                   self.checkLineFromPos(playerId, row, col, 1, -1)[1])

    def isFull(self):
        return self._number_of_turn >= self.board_row * self.board_col

    def isEmpty(self):
        return self._number_of_turn == 0

    def isOver(self):
        return self.getWinningState() != 0 or self.isFull()

    def isSquareEmpty(self, row, col):
        if self.isValidateRowCol(row, col):
            return self._squares[row][col] == 0
        return False

    def copyBoard(self, other):
        self.board_col = other.board_col
        self.board_row = other.board_row
        self._number_of_turn = other.getNumberOfTurn()
        self._winningLine = copy.deepcopy(other.getWinningLine())
        self._listMarked = copy.deepcopy(other.getListMarked())
        self._squares = copy.deepcopy(other.getSquares())

    def getNumberOfTurn(self):
        return self._number_of_turn

    def getWinningLine(self):
        return self._winningLine

    def getListMarked(self):
        return self._listMarked

    def getSquares(self):
        return self._squares

    # Check if row_index or col_index is invalid
    def isValidateRowCol(self, row_index, col_index):
        if 0 <= row_index < self.board_row and 0 <= col_index < self.board_col:
            return True
        return False


class AdvancedBoardLogic(BasicBoardLogic):
    def getMostBenefitSqrs(self, selfPlayer, oppositePlayer):
        if self.isFull():
            return -1, -1
        emptySqr = self.getEmptySquares()
        max_point = 0
        next_mark = emptySqr[0]
        for row, col in emptySqr:
            # It gonna check: if opponent has more or equal point than you then block, otherwise, play
            
            self_point = self.getScoreOfPosition(selfPlayer, row, col)
            # assume player gonna goes into specific square

            opposite_point = self.getScoreOfPosition(oppositePlayer, row, col)
            max_point = max(max_point, self_point, opposite_point)
            # If somehow point are equal, both gonna be assigned, therefore, bot will play rather than block
            if opposite_point >= max_point:
                next_mark = (row, col)
            if self_point >= max_point:
                next_mark = (row, col)
            # If somehow reach dead-end, it still play =))))
        return next_mark

    def getSquaresHasPointLargeThan(self, selfPlayer, oppositePlayer, minPoint):
        emptySqr = self.getEmptySquares()
        mySqr = list()
        for row,col in emptySqr:
            if self.getScoreOfPosition(selfPlayer, row, col) > minPoint or self.getScoreOfPosition(oppositePlayer, row, col) > minPoint:
                mySqr.append((row, col))
        return mySqr

    def getMostBenefitEnhance(self, selfPlayer, oppositePlayer):
        if self.isFull():
            return -1, -1
        emptySqr = self.getEmptySquares()
        max_point = 0
        get_self_point = 0
        get_op_point = 0
        next_mark = emptySqr[0]
        for row, col in emptySqr:
            self_point = self.getScoreOfPosition(selfPlayer, row, col)
            opposite_point = self.getScoreOfPosition(oppositePlayer, row, col)
            max_point = max(max_point, self_point, opposite_point)
            if self_point >= max_point:
                if self_point == get_self_point:
                    if opposite_point > get_op_point:
                        get_op_point = opposite_point
                        next_mark = (row, col)
                else:
                    get_self_point = self_point
                    next_mark = (row, col)

            if opposite_point >= max_point:
                if opposite_point == get_op_point:
                    if self_point > get_self_point:
                        get_self_point = self_point
                        next_mark = (row, col)
                else:
                    get_op_point = opposite_point
                    next_mark = (row, col)
        return next_mark
    
    

