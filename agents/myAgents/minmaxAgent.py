import random
import time
from template import Agent
from Reversi.reversi_model import ReversiGameRule
from Reversi.reversi_utils import filpColor


class myAgent(Agent):
    def __init__(self,_id):
        super().__init__(_id)
        self.id = _id
        self.heuristic_table = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]

        self.rule = ReversiGameRule(2)
        

    def alphabeta(self,state,depth,alpha,beta,player,start):
        if depth == 0 or time.time()-start > 1:
            return "Pass",self.evaluate(state.board,state.agent_colors[player])

        actions = self.rule.getLegalActions(state,player)
        op_actions = self.rule.getLegalActions(state,(player+1)%2)

        if "Pass" in actions and "Pass" in op_actions:
            score = self.rule.calScore(state,player)
            op_score = self.rule.calScore(state,(player+1)%2)
            gap = score - op_score
            if gap < 0:
                return "Pass",-float("inf")
            elif gap > 0:
                return "Pass",float("inf")
            else:
                return "Pass",score

        if "Pass" in actions:
            if not "Pass" in op_actions:
                return "Pass",-self.alphabeta(state,depth-1,-beta,-alpha,(player+1)%2,start)[1]

        choice = actions[0]
        for action in actions:
            if alpha >= beta:
                break
            new = self.rule.generateSuccessor(state,action,player)
            score = -self.alphabeta(new,depth-1,-beta,-alpha,(player+1)%2,start)[1]
            if score > alpha:
                alpha = score
                choice = action
        return choice,alpha


    def SelectAction(self,actions,game_state):
        color = game_state.agent_colors[self.id]
        self.rule.agent_colors = game_state.agent_colors
        self.update_weight(game_state, color)
        start_time = time.time()
        action,score = self.alphabeta(game_state,3,-float("inf"),float("inf"),self.id,start_time)
        if action == None:
            return random.choice(actions)
        return action


    def evaluate(self, board, color):
        board_size = len(board)
        uncolor = filpColor(color)
        score = 0
        for i in range(board_size):
            for j in range(board_size):
                if board[i][j] == color:
                    score += self.heuristic_table[i][j]
                elif board[i][j] == uncolor:
                    score -= self.heuristic_table[i][j]
        return score

    def update_weight(self, game_state, color):

        if game_state.getCell((0, 0)) == color:
            self.heuristic_table[0][1] = 20
            self.heuristic_table[1][1] = 40
            self.heuristic_table[1][0] = 20
        if game_state.getCell((0, 7)) == color:
            self.heuristic_table[0][6] = 20
            self.heuristic_table[1][7] = 20
            self.heuristic_table[1][6] = 40
        if game_state.getCell((7, 0)) == color:
            self.heuristic_table[7][1] = 20
            self.heuristic_table[6][0] = 20
            self.heuristic_table[6][1] = 40
        if game_state.getCell((7, 7)) == color:
            self.heuristic_table[7][6] = 20
            self.heuristic_table[6][6] = 40
            self.heuristic_table[6][7] = 20    