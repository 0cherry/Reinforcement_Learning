# -*- coding: utf-8 -*-
from environment import GraphicDisplay, Env

class Agent:
    def __init__(self, env):
        self.env = env
        # 2-d list for the value function
        self.value_table = [[0.0] * env.width for _ in range(env.height)]
        self.discount_factor = 0.9

    # get next value function table from the current value function table
    def update_value(self):
        next_value_table = [[0.0] * self.env.width for _ in range(self.env.height)]
        for state in self.env.get_all_states():
            if state == [2, 2]:
                next_value_table[state[0]][state[1]] = 0.0
                continue
            value_list = []

            # ------------------------- FROM HERE ----------------------------#
            # make value_list s --> s' by certain action a
            #
            for possible_action in self.env.possible_actions:
                next_state = self.env.state_after_action(state, possible_action)
                pas_value = self.get_value(next_state)
                pas_value *= self.discount_factor
                pas_value += self.env.get_reward(state, possible_action)
                value_list.append(pas_value)
            # ------------------------- UNTIL HERE ---------------------------#

            # return the maximum value(it is the optimality equation!!)
            next_value_table[state[0]][state[1]] = round(max(value_list), 2)
        self.value_table = next_value_table

    # get action according to the current value function table
    def get_action(self, state):
        action_list = []
        max_value = -99999

        if state == [2, 2]:
            return []

        # calculating values for the all actions and
        # append the action to action list which has maximum q value
        # ------------------------- FROM HERE ----------------------------#
        # make action_list ( which is a list for possible next optimal action )
        next_actions = [] # substitute action_list.clear()
        for possible_action in self.env.possible_actions:
            next_state = self.env.state_after_action(state, possible_action)
            next_state_value = self.get_value(next_state)
            next_state_value += self.env.get_reward(state, possible_action)
            if max_value < next_state_value:
                next_actions = []
                max_value = next_state_value
                next_actions.append(possible_action)
            elif max_value == next_state_value:
                next_actions.append(possible_action)
        [action_list.append(action) for action in next_actions]

        # ------------------------- UNTIL HERE ---------------------------#
        return action_list

    def get_value(self, state):
        return round(self.value_table[state[0]][state[1]], 2)


if __name__ == "__main__":
    env = Env()
    agent = Agent(env)
    grid_world = GraphicDisplay(agent)
    grid_world.mainloop()
