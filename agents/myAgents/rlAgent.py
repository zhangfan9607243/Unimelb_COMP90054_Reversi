import random
import time
from collections import deque
from copy import deepcopy

from Reversi.reversi_utils import Cell
from template import Agent
from Reversi.reversi_model import ReversiGameRule
import sys
sys.path.append("agents/myAgents/")
import json

class myAgent(Agent):

    def __init__(self, _id):
        super().__init__(_id)
        self.game_rule = ReversiGameRule(num_of_agent=2)
        self.think_time = 1
        self.corner_pos = [(0,0), (0,7), (7,0), (7,7)]
        self.sub_corner_pos = [(1,1), (1,6), (6,1), (6,6)]
        self.epsilon = 0.6
        self.gamma = 0.9
        self.weight = [0, 0, 0, 0, 0, 0]
        with open("agents/myAgents/rl_weight.json", "r", encoding="utf-8") as fw:
            self.weight = json.load(fw)["weight"]

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    def OppoGetActions(self, state):
        return self.game_rule.getLegalActions(state, 1-self.id)

    def ExcuteAction(self, state, action):
        next_state = self.game_rule.generateSuccessor(state, action, self.id)
        return next_state

    def OppoExcuteAction(self, state, action):
        next_state = self.game_rule.generateSuccessor(state, action, 1-self.id)
        return next_state

    def GameEnd(self, state):
        return self.GetActions(state) == ["Pass"] and self.OppoGetActions(state) == ["Pass"]

    def CalculateScore(self, state):
        return self.game_rule.calScore(state, self.id) - self.game_rule.calScore(state, 1-self.id)

    def TransformState(self, state):
        result = ""
        for line in state.board:
            for cell in line:
                result += str(cell.value + 1)
        return result

    def CalFeatures(self, state, action):
        self_color = self.game_rule.agent_colors[self.id]
        features = []
        next_state = self.ExcuteAction(state, action)
        # F1 self count
        self_score = self.game_rule.calScore(next_state, self.id)
        features.append(self_score / 64)
        # F2 oppo count
        oppo_score = self.game_rule.calScore(next_state, 1-self.id)
        features.append(oppo_score / 64)
        # F3/4 corner/subcorner
        c3 = 0
        c4 = 0
        c5 = 0
        visited = set()

        def BrfsFindEdge(pos):
            res = 0
            if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                return 0
            if pos in visited:
                return 0
            if next_state.board[pos[0]][pos[1]] == self.game_rule.agent_colors[self.id]:
                visited.add(pos)
                res += 1
                res += BrfsFindEdge((pos[0] + 1, pos[1]))
                res += BrfsFindEdge((pos[0] - 1, pos[1]))
                res += BrfsFindEdge((pos[0], pos[1] + 1))
                res += BrfsFindEdge((pos[0], pos[1] - 1))
            return res

        for i in range(4):
            if next_state.board[self.corner_pos[i][0]][self.corner_pos[i][1]] == self_color:
                c3 += 1
                c5 += BrfsFindEdge(self.corner_pos[i])
            if next_state.board[self.corner_pos[i][0]][self.corner_pos[i][1]] == Cell.EMPTY:
                c4 += 1

        features.append(c3/4)
        features.append(c4/4)
        # c5 edge
        features.append(c5/28)
        # F6 oppo Corner
        oppo_new_actions = self.OppoGetActions(next_state)
        c6 = len(set(oppo_new_actions).intersection(set(self.corner_pos)))
        features.append(c6/4)
        return features

    def CalQValue(self, state, action):
        features = self.CalFeatures(state, action)
        if len(features) != len(self.weight):
            print("F & W length not matched !")
            return -999999
        else:
            ans = 0
            for i in range(len(features)):
                ans += features[i] * self.weight[i]
            return ans

    def SelectAction(self, actions, game_state):
        self.game_rule.agent_colors = game_state.agent_colors
        start_time = time.time()
        solution = random.choice(actions)
        best_Q_value = -999999
        for action in actions:
            if time.time() - start_time > self.think_time:
                print("Time out !")
                break
            Q_value = self.CalQValue(game_state, action)
            if Q_value > best_Q_value:
                best_Q_value = Q_value
                solution = action

        return solution
