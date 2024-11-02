import random
import time
from collections import deque
from copy import deepcopy
from template import Agent
from Reversi.reversi_model import ReversiGameRule


class myAgent(Agent):

    def __init__(self, _id):
        super().__init__(_id)
        self.my_id = self.id
        self.op_id = 1 - self.id
        self.time_limit = 1
        self.epsilon = 0.1
        self.gamma = 0.9

    def time_permit(self, start_time):
        return time.time() - start_time < self.time_limit

    def epsilon_greedy(self):
        return random.uniform(0, 1) < 1 - self.epsilon

    # Opponent's move: assuming opponent will move such that it will maximum its score each round
    def op_best_move(self, next_state):
        op_next_actions = self.game_rule.getLegalActions(next_state, self.op_id)
        op_max_score = 0
        op_best_action = random.choice(op_next_actions)
        op_best_state = self.game_rule.generateSuccessor(next_state, op_best_action, self.op_id)
        for op_action in op_next_actions:
            op_next_state = self.game_rule.generateSuccessor(next_state, op_action, self.op_id)
            op_next_score = self.game_rule.calScore(op_next_state, self.op_id)
            if op_next_score > op_max_score:
                op_max_score = op_next_score
                op_best_action = op_action
                op_best_state = op_next_state
        return op_best_action, op_best_state

    def game_end(self, state):
        return self.game_rule.getLegalActions(state, self.my_id) == ["Pass"] and self.game_rule.getLegalActions(state, self.op_id) == ["Pass"]

    def state_to_string(self, state):
        board = state.board
        result = ""
        for line in board:
            for cell in line:
                if cell.__str__() == "Cell.WHITE":
                    cell_string = "w"
                elif cell.__str__() == "Cell.BLACK":
                    cell_string = "b"
                else:
                    cell_string = "e"
                result += cell_string
        return result

    def SelectAction(self, actions, game_state):

        self.game_rule = ReversiGameRule(num_of_agent=2)
        self.game_rule.agent_colors = game_state.agent_colors

        start_time = time.time()

        solution = random.choice(actions)

        state_v_dict = dict()  # Record value of each state
        state_n_dict = dict()  # Record visit times of each state
        state_best_action_dict = dict()  # Record the best action for each state
        state_expanded_actions_dict = dict()  # Record expanded actions for each state

        root_state_string = self.state_to_string(game_state)

        # Select
        while self.time_permit(start_time):
            current_state = deepcopy(game_state)
            current_actions = actions.copy()
            current_state_string = root_state_string
            path = deque([])  # For backpropagation

            # Searching for a not-fully-expanded state
            while self.time_permit(start_time) and not self.game_end(current_state):

                if current_state_string in state_expanded_actions_dict:
                    expanded_actions = state_expanded_actions_dict[current_state_string]
                    unexpanded_actions = list(set(current_actions).difference(set(expanded_actions)))
                else:
                    unexpanded_actions = current_actions

                if unexpanded_actions != 0:
                    break

                if self.epsilon_greedy():
                    selected_action = state_best_action_dict[current_state_string]
                else:
                    selected_action = random.choice(current_actions)

                next_state = self.game_rule.generateSuccessor(current_state, selected_action, self.my_id)
                path.append((current_state_string, selected_action))
                op_best_action, op_best_state = self.op_best_move(next_state)
                current_actions = self.game_rule.getLegalActions(op_best_state, self.my_id)
                current_state = op_best_state

                current_state_string = self.state_to_string(current_state)
            # Expansion
            if current_state_string in state_expanded_actions_dict:
                expanded_actions = state_expanded_actions_dict[current_state_string]
                unexpanded_actions = list(set(current_actions).difference(set(expanded_actions)))
            else:
                unexpanded_actions = current_actions

            if len(unexpanded_actions) == 0:
                expanded_action = random.choice(current_actions)
            else:
                expanded_action = random.choice(unexpanded_actions)

            if current_state_string in state_expanded_actions_dict:
                state_expanded_actions_dict[current_state_string].append(expanded_action)
            else:
                state_expanded_actions_dict[current_state_string] = [expanded_action]

            path.append((current_state_string, expanded_action))

            next_state = self.game_rule.generateSuccessor(current_state, expanded_action, self.my_id)
            op_best_action, op_best_state = self.op_best_move(next_state)
            current_actions = self.game_rule.getLegalActions(op_best_state, self.my_id)
            current_state = op_best_state

            # Simulation
            length = 0
            max_length = 12
            while self.time_permit(start_time) and not self.game_end(current_state) and length <= max_length:
                length += 1
                next_action = random.choice(current_actions)
                next_state = self.game_rule.generateSuccessor(current_state, next_action, self.my_id)
                op_next_action, op_next_state = self.op_best_move(next_state)
                current_actions = self.game_rule.getLegalActions(op_next_state, self.my_id)
                current_state = op_next_state
            reward = self.game_rule.calScore(current_state, self.my_id) - self.game_rule.calScore(current_state, self.op_id)

            # BackPropagation
            value = reward * (self.gamma ** length)
            while len(path) != 0:
                state_string, action = path.pop()
                if state_string in state_v_dict:
                    if value > state_v_dict[state_string]:
                        state_v_dict[state_string] = value
                        state_best_action_dict[state_string] = action
                    state_n_dict[state_string] += 1
                else:
                    state_v_dict[state_string] = value
                    state_n_dict[state_string] = 1
                    state_best_action_dict[state_string] = action
                value *= self.gamma
            if root_state_string in state_best_action_dict:
                solution = state_best_action_dict[root_state_string]

        return solution
