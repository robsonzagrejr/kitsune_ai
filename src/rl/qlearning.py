import os
import numpy as np
import pickle
  
from collections import defaultdict


class QLearning():
    def __init__(self, init_state, n_actions, max_episodes=200, discount_factor = 1,
                            alpha = 0.6, epsilon = 0.1):
        self.file_path = "models/mario_qlearning.pkl"
        self.max_episodes = max_episodes
        self.n_actions = n_actions
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor

        #self._reset_state = init_state.copy()
        #self._last_state = init_state
        self._reset_state = ()
        self._last_state = ()
        self.epoch_reward = None


        #FIXME initial values
        self.Q = None
        if os.path.exists(self.file_path):
            print("Loading Q from saved file")
            self.load()
        if self.Q is None:
            print("Initialize Q with default values")
            self.Q = defaultdict(self._init_q)
            self.save()
        #FIXME best policy?
        #self.policy = self.createEpsilonGreedyPolicy()


    def _init_q(self):
        return np.zeros(self.n_actions)


    def policy(self, state):
        """
        Creates an epsilon-greedy policy based
        on a given Q-function and epsilon.

        Returns a function that takes the state
        as an input and returns the probabilities
        for each action in the form of a numpy array
        of length of the action space(set of possible actions).
        """
        action_probabilities = np.ones(self.n_actions,
                dtype = float) * self.epsilon / self.n_actions

        best_action = np.argmax(self.Q[state])
        action_probabilities[best_action] += (1.0 - self.epsilon)
        return action_probabilities


    def _handle_state(self, state):
        return tuple(
            [
                tuple(l)
                for l in sorted(state)
            ]
        )

    
    def step(self, state, reward, done, is_training=False):
        state = self._handle_state(state)
        if is_training:
            action = self.train(state, reward, done)
        else:
            # Get best action for this state
            action = np.argmax(self.Q[state])
        return action


    def train(self, state, reward, done):
        #state here is las_action
        # get probabilities of all actions from current state
        action_probabilities = self.policy(self._last_state)

        # choose action according to
        # the probability distribution
        action = np.random.choice(
            np.arange(len(action_probabilities)),
            p = action_probabilities
        )

        # TD Update
        best_next_action = np.argmax(self.Q[state])
        td_target = reward + self.discount_factor * self.Q[state][best_next_action]
        td_delta = td_target - self.Q[self._last_state][action]
        self.Q[self._last_state][action] += self.alpha * td_delta

        if done:
            self._last_state = self._reset_state
            self.save()
        else:
            self._last_state = state

        return action


    def save(self):
        print("Saving learning...")
        #FIXME create new file
        with open(self.file_path, 'wb+') as f:
            result_save = {
                "Q": self.Q
            }
            pickle.dump(result_save, f)


    def load(self):
        print("Loading learning...")
        with open(self.file_path, 'rb+') as f:
            print("Loading")
            result_saved = pickle.load(f)
            self.Q = result_saved['Q']

