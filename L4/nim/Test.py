import math
import random
import time
import pandas as pd


class NimAI:
    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        """
            stateT = tuple(state)
            actionT = tuple(action)
            self.q = [stateT, actionT]
            """
        self.q = [state, action]
        if not self.q:
            print(self.q)
            print("00000")
            return 0
        else:
            self.q = [state, action]
            print(self.q)
            return self.q


state = 2
action = 2


ai_agent = NimAI()

test = ai_agent.get_q_value(state, action)
print(test)
