# -*- coding: utf-8 -*-
from environment import GraphicDisplay, Env

class Agent:
    def __init__(self, env):
        self.env = env
        # 2-d list for the value function
        self.value_table = [[0.0] * env.width for _ in range(env.height)]
        self.discount_factor = 0.9

    # get next value function table from the current value function table
    def udpate_value(self):
         raise NotImplementedError()

    # get action according to the current value function table
    def get_action(self, state):
        action_list = []
        max_value = -99999

        if state == [2, 2]:
            return []

        # calculating q values for the all actions and
        # append the action to action list which has maximum q value
        for action in self.env.possible_actions: #[0, 1,2,3] = [up, down, left, right]

            ## exception handling(boundary case)
            row, col = state
            if row == 0 and action == 0:  continue # ignore
            if row == 4 and action == 1:  continue # ignore
            if col == 0 and action == 2:  continue # ignore
            if col == 4 and action == 3:  continue # ignore

            ## exception handling(hazard case)
            if row == 1 and col == 1 and action == 3:  continue # ignore
            if row == 0 and col == 2 and action == 1:  continue # ignore
            if row == 1 and col == 3 and action == 2:  continue # ignore
            
            if row == 1 and col == 1 and action == 1:  continue # ignore
            if row == 2 and col == 0 and action == 3:  continue # ignore
            if row == 3 and col == 1 and action == 0:  continue # ignore

            # store only max value actions (without reward)
            next_state = self.env.state_after_action(state, action)
            next_value = self.get_value(next_state)
            value = self.discount_factor * next_value

            if value > max_value:
                action_list.clear()
                action_list.append(action)
                max_value = value
            elif value == max_value:
                action_list.append(action)

        return action_list

    def get_value(self, state):
        return round(self.value_table[state[0]][state[1]], 2)


class SimpleValueUpdateAgent(Agent):
    # get next value function table from the current value function table
    def udpate_value(self):
        next_value_table = [[0.0] * self.env.width for _ in range(self.env.height)]

        for state in self.env.get_all_states():
            if state == [2, 2]:
                next_value_table[state[0]][state[1]] = 2.0  # <-- we just set value
                continue

            ## hazard exception handling
            if state in [ [1, 2], [2,1] ] :
                next_value_table[state[0]][state[1]] = 0.0
                continue

            # ------------------------- FROM HERE ----------------------------#
            # code proper values
            #
            # useful methods and variables
            #   - self.env.possible_actions : return all possible actions in current state
            #   - self.env.state_after_action(state, action) : retrieve next state
            #   - self.get_value(state) : return value of the state
            #   - self.discount_factor : discount factor
            maximum_value = 0
            for possible_action in self.env.possible_actions:
                possible_action_state = self.env.state_after_action(state, possible_action)
                pas_value = self.get_value(possible_action_state)
                if maximum_value < pas_value:
                    maximum_value = pas_value
            value_prime = maximum_value * self.discount_factor

            # ---------------------------------- UNTTIL HERE ----------------------------- #
            next_value_table[state[0]][state[1]] = value_prime

        self.value_table = next_value_table

   

if __name__ == "__main__":
    env = Env()
    agent = SimpleValueUpdateAgent(env)
    grid_world = GraphicDisplay(agent)
    grid_world.mainloop()
