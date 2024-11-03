import random
import time
from template import Agent
from Reversi.reversi_model import ReversiGameRule

# This is a uniform cost search using the score difference between opponent agent and my agent as cost
class myAgent(Agent):

    def __init__(self, _id):
        super().__init__(_id)
        self.my_id = self.id
        self.op_id = 1 - self.id
        self.time_limit = 1

    def time_permit(self, start_time):
        return time.time() - start_time < self.time_limit

    def SelectAction(self, actions, game_state):

        # Create a reversi game state to be equal to current game state
        self.game_state = ReversiGameRule(num_of_agent=2)
        self.game_state.agent_colors = game_state.agent_colors

        # Set start time
        start_time = time.time()

        # Initialize open list and corresponding priority list
        initial_node = (game_state, [])
        open_list = [initial_node]
        priority_list = [0]

        # Initialize max score that my agent can achieve next round and path of actions from next round
        my_next_path = []

        # BFS algorithm continuously search if open list not empty and time limit permits
        while open_list != [] and priority_list != [] and self.time_permit(start_time):

            # Pop the state with max priority
            current_max_priority = max(priority_list)
            current_index = priority_list.index(current_max_priority)
            current_node = current_state, current_path = open_list[current_index]
            priority_list.remove(current_max_priority)
            open_list.remove(current_node)

            # Calculate current score of my agent
            current_score = self.game_state.calScore(current_state, self.my_id)

            # Generate a list of actions of my agent at current state
            my_next_actions = self.game_state.getLegalActions(current_state, self.my_id)

            # For each candidate legal actions
            for next_action in my_next_actions:

                # Check whether time permit
                if self.time_permit(start_time):

                    # For selected action: generate next state & extend next path & calculate next score
                    my_next_path = current_path + [next_action]
                    my_next_state = self.game_state.generateSuccessor(current_state, next_action, self.my_id)
                    my_next_score = self.game_state.calScore(current_state, self.my_id)

                    # For opponent, assuming it will act as to max its next score
                    op_next_actions = self.game_state.getLegalActions(my_next_state, self.op_id)
                    op_max_score = 0
                    for op_action in op_next_actions:
                        op_next_state = self.game_state.generateSuccessor(my_next_state, op_action, self.op_id)
                        op_next_score = self.game_state.calScore(my_next_state, self.op_id)
                        if op_max_score < op_next_score:
                            op_max_score = op_next_score
                            my_next_state = op_next_state

                    # Generate next node and heuristics of next node and push it into open list
                    next_node = (my_next_state, my_next_path)
                    next_heuristic = current_score + my_next_score - op_max_score
                    open_list.append(next_node)
                    priority_list.append(next_heuristic)

                # If time not permit, break the while loop
                else:
                    break

        # Choose the next action to be the initial action in the path list
        if my_next_path != []:
            solution = my_next_path[0]
        else:
            solution = random.choice(actions)

        # Return solution
        return solution


