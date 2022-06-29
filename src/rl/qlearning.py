import numpy as np
import pandas as pd
  
from collections import defaultdict


class QLearning():

    def __init__(self, init_state, n_actions, max_episodes=200, discount_factor = 1.0,
                            alpha = 0.6, epsilon = 0.1):
        self.max_episodes = max_episodes
        self.n_actions = n_actions
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount_factor = discount_factor

        #self._reset_state = init_state.copy()
        #self._last_state = init_state
        self._reset_state = ()
        self._last_state = ()
        self._last_reward = None
        self._last_done = None

        #FIXME initial values
        self.Q = defaultdict(lambda: np.zeros(self.n_actions))
        #FIXME best policy?
        self.policy = self.createEpsilonGreedyPolicy()


    def createEpsilonGreedyPolicy(self):
        Q = self.Q
        epsilon = self.epsilon
        num_actions = self.n_actions
        """
        Creates an epsilon-greedy policy based
        on a given Q-function and epsilon.

        Returns a function that takes the state
        as an input and returns the probabilities
        for each action in the form of a numpy array
        of length of the action space(set of possible actions).
        """
        def policyFunction(state):

            Action_probabilities = np.ones(num_actions,
                    dtype = float) * epsilon / num_actions

            best_action = np.argmax(self.Q[state])
            Action_probabilities[best_action] += (1.0 - epsilon)
            return Action_probabilities

        return policyFunction


    def _handle_state(self, state):
        return tuple(
            [
                tuple(l)
                for l in sorted(state)
            ]
        )

    
    def step(self, state, reward, done, is_training=False):
        state = self._handle_state(state)
        print(state)
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
        else:
            self._last_state = state

        return action


    def qLearning(env, num_episodes, discount_factor = 1.0,
                                alpha = 0.6, epsilon = 0.1):
        """
        Q-Learning algorithm: Off-policy TD control.
        Finds the optimal greedy policy while improving
        following an epsilon-greedy policy"""

        # Action value function
        # A nested dictionary that maps
        # state -> (action -> action-value).
        Q = defaultdict(lambda: np.zeros(env.action_space.n))

        # Create an epsilon greedy policy function
        # appropriately for environment action space
        policy = createEpsilonGreedyPolicy(Q, epsilon, env.action_space.n)

        # For every episode
        for ith_episode in range(num_episodes):

            # Reset the environment and pick the first action
            state = env.reset()

            #While true
            for t in itertools.count():

                # get probabilities of all actions from current state
                action_probabilities = policy(state)

                # choose action according to
                # the probability distribution
                action = np.random.choice(np.arange(
                          len(action_probabilities)),
                           p = action_probabilities)

                # take action and get reward, transit to next state
                next_state, reward, done, _ = env.step(action)


                # TD Update
                best_next_action = np.argmax(Q[next_state])
                td_target = reward + discount_factor * Q[next_state][best_next_action]
                td_delta = td_target - Q[state][action]
                Q[state][action] += alpha * td_delta

                # done is True if episode terminated
                if done:
                    break

                state = next_state

