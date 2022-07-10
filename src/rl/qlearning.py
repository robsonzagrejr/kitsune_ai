import os
import numpy as np
from functools import partial
  
from collections import defaultdict

import src.rl.utils as utils


class QLearning():
    result_save = {}
    def __init__(self, n_actions, discount_factor = 0.6, alpha = 0.6, epsilon = 0.1):
        self.file_path = "models/mario_qlearning"
        self.n_actions = n_actions
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor

        self._reset_state = ()
        self._last_state = ()
        self.load_saved = True
        self._save_in_each_epoch = 1
        self.epoch = 0


        #FIXME initial values
        self.Q = None
        if self.load_saved and os.path.exists(self.file_path+".pkl"):
            self.load()

        if self.Q is None:
            self.Q = defaultdict(partial(np.zeros, n_actions))

        self.epoch_metrics = {
            self.epoch: {
                "epoch": self.epoch,
                "acc_reward": 0,
            }
        }

        self.save()



    def policy(self, state):
        #FIXME best policy?
        """
        Creates an epsilon-greedy policy based
        on a given Q-function and epsilon.

        Returns a function that takes the state
        as an input and returns the probabilities
        for each action in the form of a numpy array
        of length of the action space(set of possible actions).
        """
        action_probabilities = (
            np.ones(
                self.n_actions,
                dtype = float
            )
            * (self.epsilon / self.n_actions)
        )
        best_action = np.argmax(self.Q[state])
        action_probabilities[best_action] += (1.0 - self.epsilon)
        return action_probabilities


    def _handle_state(self, state):
        return tuple(
            [
                #Force int value to get less memory sinze we are talking
                # a range of NES screen
                tuple([np.int16(x) if x is not None else -999 for x in l])
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

        # Update metrics
        self.epoch_metrics[self.epoch]["acc_reward"] += reward

        if done:
            self._last_state = self._reset_state

            if self.epoch % self._save_in_each_epoch == 0:
                self.save(self.epoch, self.epoch_metrics)

            self.epoch += 1
            #Reset epoch metrics
            self.epoch_metrics[self.epoch] = {
                "epoch": self.epoch,
                "acc_reward": 0,
            }

        else:
            self._last_state = state

        return action


    def save(self):
        result_save = {
            "Q": self.Q,
            "metrics": self.epoch_metrics,
            "epoch": self.epoch
        }
        utils.save(result_save, self.file_path)


    def load(self):
        result_load = utils.load(self.file_path)
        self.Q = result_load.get('Q', None)
        metrics = result_load.get('metrics', {})
        if metrics:
            self.epoch_metrics = metrics
        self.epoch = result_load.get("epoch", -1) + 1

