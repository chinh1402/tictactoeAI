import random
import time

from copy import deepcopy
from math import inf as infinity
import Machine.bigBoardLogic.bigBoardAIConfig.gamesettings as game_settings
import Machine.bigBoardLogic.bigBoardAIConfig.aisettings as ai_settings
from Machine.bigBoardLogic.state import State
from Machine.bigBoardLogic.minimaxnode import MinimaxNode

class ABPruningAI:
    def __init__(self) -> None:
        self.ran = 0
        self.prune = 0
    def alpha_beta(self, current_node: MinimaxNode, depth, alpha, beta, maximizingPlayer):
        if(depth == 0 or State.game_over(current_node.board)):
            self.ran += 1
            O_score, X_score = State.evaluate(current_node.board)
            return X_score - O_score
        
        if maximizingPlayer:
            self.ran += 1
            value = -infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = self.alpha_beta(child_node, depth - 1, alpha, beta, False)
                alpha = max(alpha, value)
                if temp > value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                if alpha >= beta:
                    self.prune += 1
                    break
            return value
        else:
            self.ran += 1
            value = + infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = self.alpha_beta(child_node, depth - 1, alpha, beta, True)
                beta = min(beta, value)
                if temp < value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                if alpha >= beta:
                    self.prune += 1
                    break
            return value