import os
import numpy as np
import copy
from functools import partial
  
from collections import defaultdict

import src.rl.utils as utils


class QLearning():
    result_save = {}
    def __init__(self, n_actions, gamma=0.75, alpha = 1, epsilon = 0.1):
        self.file_path = "models/mario_qlearning"
        self.n_actions = n_actions
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma #discount factor

        self._reset_state = ()
        self._last_state = ()
        self._last_action = 0
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


    def policy(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            # Random choise
            action = np.random.randint(0, self.n_actions)
        else:
            # Best action
            action = np.argmax(self.Q[state])
        return action


    def train(self, state, reward, done):
        # reward is always based in last state and last action

        # Algorithm based on Bellman equation
        best_next_action = np.argmax(self.Q[state])
        temporal_difference_target = (
            reward + self.gamma 
            * self.Q[state][best_next_action]
            - self.Q[self._last_state][self._last_action]
        )
        self.Q[self._last_state][self._last_action] += (
            self.alpha
            * temporal_difference_target
        )

        # Chooseing action based in policy derived from Q
        action = self.policy(state)

        # Update last values
        self._last_state = copy.deepcopy(state)
        self._last_action = action


        # Update metrics
        self.epoch_metrics[self.epoch]["acc_reward"] += reward

        if done:
            self._last_state = self._reset_state
            self._last_action = 0

            if self.epoch % self._save_in_each_epoch == 0:
                self.save()

            self.epoch += 1
            #Reset epoch metrics
            self.epoch_metrics[self.epoch] = {
                "epoch": self.epoch,
                "acc_reward": 0,
            }

            # Decreassing alpha
            self.alpha = self.alpha*0.95

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

