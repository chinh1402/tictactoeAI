import copy
import random
import time
from threading import Thread

from Board.BoardLogic import AdvancedBoardLogic

from math import inf as infinity
from Machine.bigBoardLogic.minimaxnode import MinimaxNode
from Machine.bigBoardLogic.abpruningai import ABPruningAI
from Machine.bigBoardLogic.state import State
import Machine.bigBoardLogic.bigBoardAIConfig.aisettings as ai_settings
import Machine.bigBoardLogic.bigBoardAIConfig.gamesettings as game_settings

class AI:
    def __init__(self, aiLevel=1, aiPlayer=2, userPlayer=1):
        self.aiLevel = aiLevel
        self.aiPlayer = aiPlayer
        self.userPlayer = userPlayer
        self.minDepth = 0
        self.ran = 0

    def minimax_update(self, board, isMaximizing, alpha, beta, depth):
        self.ran += 1
        print("Have ran: ", self.ran)
        if board.isFull() or depth == 0:
            return 0, None

        if board.getWinningState() == self.userPlayer:
            return 1, None

        if board.getWinningState() == self.aiPlayer:
            return -1, None

        if isMaximizing:
            maxEval = -100
            bestMove = None
            emptySqrs = board.getEmptySquares()
            for (row, col) in emptySqrs:
                tempBoard = copy.deepcopy(board)
                tempBoard.markSquare(self.userPlayer, row, col)
                myEval = self.minimax_update(tempBoard, False, alpha, beta, depth - 1)[0]
                if myEval > maxEval:
                    # This causes the infinite loop
                    maxEval = myEval
                    bestMove = (row, col)
                alpha = max(alpha, myEval)
                if beta <= alpha:
                    break
            return maxEval, bestMove

        if not isMaximizing:
            minEval = 100
            bestMove = None
            emptySqrs = board.getEmptySquares()
            for (row, col) in emptySqrs:
                tempBoard = copy.deepcopy(board)
                tempBoard.markSquare(self.aiPlayer, row, col)
                myEval = self.minimax_update(tempBoard, True, alpha, beta, depth - 1)[0]
                if myEval < minEval:
                    minEval = myEval
                    bestMove = (row, col)
                beta = min(beta, myEval)
                if beta <= alpha:
                    break
            return minEval, bestMove

    def minimax(self, board: AdvancedBoardLogic, isMaximizing, depth):
        self.ran += 1
        print("Have ran: ", self.ran)
        if board.isFull() or depth == 0:
            return 0, None

        if board.getWinningState() == self.userPlayer:
            return 1, None

        if board.getWinningState() == self.aiPlayer:
            return -1, None

        if isMaximizing:
            maxEval = -100
            bestMove = None
            emptySqrs = board.getEmptySquares()
            for (row, col) in emptySqrs:
                
                tempBoard = copy.deepcopy(board)
                tempBoard.markSquare(self.userPlayer, row, col)
                myEval = self.minimax(tempBoard, False, depth - 1)[0]
                if myEval > maxEval:
                    maxEval = myEval
                    bestMove = (row, col)
            return maxEval, bestMove

        if not isMaximizing:
            minEval = 100
            bestMove = None
            emptySqrs = board.getEmptySquares()
            for (row, col) in emptySqrs:
                tempBoard = copy.deepcopy(board)
                tempBoard.markSquare(self.aiPlayer, row, col)
                myEval = self.minimax(tempBoard, True, depth - 1)[0]
                if myEval < minEval:
                    minEval = myEval
                    bestMove = (row, col)
            return minEval, bestMove

    # Do mình hiện tại ko thể rẽ nhánh code dựa trường hợp, nên mình sẽ tạm thời comment lại
    # codes của hàm chạy cho bảng 3x3. Và code cho những bảng lớn hơn 
    def evalMove(self, main_board: AdvancedBoardLogic):
        if self.aiLevel == 1:
            # print("Easy")
            # self.mostMove(main_board) => main_board.getMostBenefitSqrs(self.aiPlayer, self.userPlayer)
            # => next_mark => (row,col)
            return self.mostMove(main_board)
        
        elif self.aiLevel == 2:
            # print("Medium")
            # self.mediumLevel(main_board) => move
            return self.mediumLevel(main_board)
        else:
            # print("Hard")
            # self.hardLevel(main_board) => move
            return self.hardLevel(main_board)

    def mostMove(self, main_board):
        print(main_board._squares)
        # return a coordination of the move (nextmark);
        return main_board.getMostBenefitSqrs(self.aiPlayer, self.userPlayer)
    

    def randomLevel(self, main_board):
        emptySqrs = main_board.getEmptySquares()
        move = emptySqrs[random.randint(0, len(emptySqrs) - 1)]
        return move

    def easyLevel(self, main_board):
        return self.mostMove(main_board)

    def mediumLevel(self, main_board):
        if main_board.getNumberOfTurn() < 2:
            squaresState = main_board._squares
            possible_moves = State.generate_possible_moves(squaresState, ai_settings.EXPANSION_RANGE)
            move = random.choice(possible_moves)
        else:
            # Why this doesn't work? Because there's no artificial evaluation rather than 0 -1 1
            # myEval, move = self.minimax(main_board, False, 10)

        # =====================================
            move = self.mediumGetNextMove(main_board)

        return move

    def hardLevel(self, main_board):
        # Added random move to remove first move bug
        if main_board.getNumberOfTurn() <= 2:
            squaresState = main_board._squares
            possible_moves = State.generate_possible_moves(squaresState, ai_settings.EXPANSION_RANGE)
            move = random.choice(possible_moves)
            return move
        else: 
            # myEval, move = self.minimax_update(main_board, False, -100, 100, 10)
            move = self.hardGetNextMove(main_board)
        return move

# class AIThreading(Thread):
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs={}, Verbose=None):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#
#     def run(self):
#         # noinspection PyUnresolvedReferences
#         if self._target is not None:
#             # noinspection PyUnresolvedReferences
#             self._return = self._target(*self._args,
#                                         **self._kwargs)
#
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return
    def mediumGetNextMove(self, main_board):
        # Check for checkmate move and run the alphabeta pruning with depth = 1
        last_move = main_board._listMarked[-1].position
        squaresState = main_board._squares
        id_AI = self.aiPlayer

        com_checkmate_move = State.checkmate(squaresState, id_AI)
        if com_checkmate_move: 
            return com_checkmate_move
        
        opponent_checkmate_move = State.checkmate(squaresState, game_settings.get_opponent(id_AI))
        if opponent_checkmate_move:
            return opponent_checkmate_move
        
        start_time = time.time()

        root_node = MinimaxNode(squaresState, last_move, id_AI, None)
        ai_instance = ABPruningAI()
        ai_instance.alpha_beta(root_node, 2, -infinity, +infinity, True)
        
        end_time = time.time()

        AI_Calculation_time = round(end_time - start_time, 3)
        
        print("Algorithm ran: " + str(ai_instance.ran))
        print("Pruned:" + str(ai_instance.prune))
        print("Time:" + str(AI_Calculation_time) + "s")
        return root_node.planing_next_move

    def hardGetNextMove(self, main_board):
        # Check for checkmate move, high impact move and combo move, then run the alphabeta pruning with depth = 2

        last_move = main_board._listMarked[-1].position
        squaresState = main_board._squares
        id_AI = self.aiPlayer

        # Check checkmate move for either
        com_checkmate_move = State.checkmate(squaresState, id_AI)
        if com_checkmate_move: 
            print("AI has checkmate move.")
            return com_checkmate_move
        
        opponent_checkmate_move = State.checkmate(squaresState, game_settings.get_opponent(id_AI))
        if opponent_checkmate_move:
            print("HUMAN has checkmate move.")
            return opponent_checkmate_move
        print("No one has checkmate move.")
        print("---------------------------------")

        print("Checking for high-impact move...")

        if ai_settings.ENABLE_HIGH_IMPACT_MOVE:
            opponent_high_impact_move, opponent_high_impact_score = State.high_impact_move(squaresState, game_settings.get_opponent(id_AI))
            com_high_impact_move, com_high_impact_score = State.high_impact_move(squaresState, id_AI)
            if opponent_high_impact_move and opponent_high_impact_score > com_high_impact_score:
                print("AI has discovered that HUMAN has a high-impact move.")
                print("AI has taken this move (a defensive move).")
                return opponent_high_impact_move
            if com_high_impact_move and com_high_impact_score >= opponent_high_impact_score: # >=: Prioritize playing the move to the advantage of the player
                print("AI has discovered that it has a high-impact move.")
                print("AI has taken this move (an offensive move).")
                return com_high_impact_move
            print("AI did not discover any high-impact moves.")
        print("---------------------------------")
        # Check combo move
        print("Checking for combo moves...")
        opponent_combo_move = State.combo_move(squaresState, game_settings.get_opponent(id_AI))
        com_combo_move = State.combo_move(squaresState, id_AI)
        if com_combo_move:
            print("AI has a combo move. Take it!")
            return com_combo_move
        if opponent_combo_move: 
            print("HUMAN has a combo move. Block it!")
            return opponent_combo_move

        # # Announcement
        print("There is no combo move.")
        print("---------------------------------")

        # =======================================
        # if not

        # Announcement
        print("AI has decided to use the Alpha-Beta pruning algorithm. Calculating...")

        start_time = time.time()
        
        root_node = MinimaxNode(squaresState, last_move, id_AI, None)
        ai_instance = ABPruningAI()
        ai_instance.alpha_beta(root_node, ai_settings.MAX_TREE_DEPTH_LEVEL, -infinity, +infinity, True)
        
        end_time = time.time()

        AI_Calculation_time = round(end_time - start_time, 3)
        
        print("Algorithm ran: " + str(ai_instance.ran))
        print("Pruned:" + str(ai_instance.prune))
        print("Time:" + str(AI_Calculation_time) + "s")
        return root_node.planing_next_move
