"""
https://towardsdatascience.com/evolving-neural-networks-b24517bb3701
"""
import copy

import numpy as np


class NaturalEvolution():

    def __init__(self, n_actions, population_size=5, holdout=0.1, mating=True):
        self.generation = 0
        self.population_size = population_size

        if holdout == 'sqrt':
            self.holdout = max(1, int(np.sqrt(population_size)))
        elif holdout == 'log':
            self.holdout = max(1, int(np.log(population_size)))
        elif holdout > 0 and holdout < 1:
            self.holdout = max(1, int(holdout * population_size))
        else:
            self.holdout = max(1, int(holdout))
 
        self.mating = mating

        self.n_actions = n_actions
        self.steps = 0
        self.best_organism = {
            "score": 0,
            "organismo": None,
        }

        # ==Calculing the number of inputs==
        # There is 9 information of object,
        #in screen, we got a 256x240 screen.
        #commonly a object got 16x16, so we must
        #be prepare to recive ~256/16 objects.
        self.max_objs = int((256*240)/(16*16) * 9)

        # Generating first population
        # here will be softmax because we will select one of the
        # n possible actions that already contains the combinations
        self.population = [
            self._gen_organism()
            for _ in range(self.population_size)
        ]
        self._last_population = []
        self._organism = self.population.pop()
        self._last_acc_score = 0
        self._last_acc_score_cache = 0


    def _gen_organism(self):
        return Organism([self.max_objs, 16, 16, 16, self.n_actions], output="softmax")


    def _handle_state(self, state):
        # Handling all objects to be 
        flatten_state = (
            np.array([y if y else -999 for x in state for y in x])
            .flatten()
        )
        empty_values = np.full(int(self.max_objs-flatten_state.size), -999)
        return np.concatenate([flatten_state, empty_values])


    def step(self, state, reward, done, is_training=False):
        state = self._handle_state(state)
        if is_training:
            action = self.train(state, reward, done)

        return action


    def train(self, state, reward, done):
        self.steps += 1
        self._last_acc_score += reward
        reset = False
        if self.steps % 100 == 0:
            if self._last_acc_score_cache >= self._last_acc_score:
                reset = True
            else:
                self._last_acc_score_cache = self._last_acc_score

        action = 0
        if reset:
            action = 13 #reset command
            done = True

        # Reseting steps
        if done:
            self.steps = 0
            self._last_population.append(
                (self._last_acc_score, self._organism)
            )

            if len(self.population) == 0:
                self._next_generation()

            self._organism = self.population.pop()
            self._last_acc_score = 0
            self._last_acc_score_cache = 0
        else:
            action = self._organism.predict(state)
            action = np.argmax(action.flatten())

        return action


    def _next_generation(self):
        self.generation += 1
        print(f"Creating Generation: {self.generation}")

        order_population = sorted(self._last_population, key=lambda x: x[0], reverse=True)
        order_population = [o[1] for o in order_population]
        new_population = []
        for i in range(self.population_size):
            parent_1_idx = i % self.holdout
            if self.mating:
                parent_2_idx = min(self.population_size - 1, int(np.random.exponential(self.holdout)))
            else:
                parent_2_idx = parent_1_idx
            offspring = order_population[parent_1_idx].mate(order_population[parent_2_idx])
            new_population.append(offspring)

        # Ensure best organism survives
        new_population[-1] = order_population[0]
        self.population = copy.deepcopy(new_population)
        self._last_population = []


    def generation(self, repeats=1, keep_best=True):
        rewards = [np.mean([self.scoring_function(x) for _ in range(repeats)]) for x in self.population]
        self.population = [self.population[x] for x in np.argsort(rewards)[::-1]]
        new_population = []
        for i in range(self.population_size):
            parent_1_idx = i % self.holdout
            if self.mating:
                parent_2_idx = min(self.population_size - 1, int(np.random.exponential(self.holdout)))
            else:
                parent_2_idx = parent_1_idx
            offspring = self.population[parent_1_idx].mate(self.population[parent_2_idx])
            new_population.append(offspring)
        if keep_best:
            new_population[-1] = self.population[0] # Ensure best organism survives
        self.population = new_population

        # Ensure best organism survives
        new_population[-1] = self.population[0]
        self.population = new_population



class Organism():
    def __init__(self, dimensions, use_bias=True, output='softmax'):
        self.layers = []
        self.biases = []
        self.use_bias = use_bias
        self.output = self._activation(output)
        for i in range(len(dimensions)-1):
            shape = (dimensions[i], dimensions[i+1])
            std = np.sqrt(2 / sum(shape))
            layer = np.random.normal(0, std, shape)
            bias = np.random.normal(0, std, (1,  dimensions[i+1])) * use_bias
            self.layers.append(layer)
            self.biases.append(bias)


    def _activation(self, output):
        if output == 'softmax':
            return lambda X : np.exp(X) / np.sum(np.exp(X), axis=1).reshape(-1, 1)
        if output == 'sigmoid':
            return lambda X : (1 / (1 + np.exp(-X)))
        if output == 'linear':
            return lambda X : X


    def predict(self, X):
        for index, (layer, bias) in enumerate(zip(self.layers, self.biases)):
            X = X @ layer + np.ones((X.shape[0], 1)) @ bias
            if index == len(self.layers) - 1:
                X = self.output(X) # output activation
            else:
                X = np.clip(X, 0, np.inf)  # ReLU
        
        return X


    #FIXME ?
    def predict_choice(self, X, deterministic=True):
        probabilities = self.predict(X)
        if deterministic:
            return np.argmax(probabilities, axis=1).reshape((-1, 1))

        if any(np.sum(probabilities, axis=1) != 1):
            raise ValueError(f'Output values must sum to 1 to use deterministic=False')
        if any(probabilities < 0):
            raise ValueError(f'Output values cannot be negative to use deterministic=False')
        choices = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            U = np.random.rand(X.shape[0])
            c = 0
            while U > probabilities[i, c]:
                U -= probabilities[i, c]
                c += 1
            else:
                choices[i] = c
        return choices.reshape((-1,1))


    def mutate(self, stdev=0.03):
        for i in range(len(self.layers)):
            self.layers[i] += np.random.normal(0, stdev, self.layers[i].shape)
            if self.use_bias:
                self.biases[i] += np.random.normal(0, stdev, self.biases[i].shape)


    def mate(self, other, mutate=True):
        if self.use_bias != other.use_bias:
            raise ValueError('Both parents must use bias or not use bias')
        if not len(self.layers) == len(other.layers):
            raise ValueError('Both parents must have same number of layers')
        if not all(self.layers[x].shape == other.layers[x].shape for x in range(len(self.layers))):
            raise ValueError('Both parents must have same shape')

        child = copy.deepcopy(self)
        for i in range(len(child.layers)):
            pass_on = np.random.rand(1, child.layers[i].shape[1]) < 0.5
            child.layers[i] = pass_on * self.layers[i] + ~pass_on * other.layers[i]
            child.biases[i] = pass_on * self.biases[i] + ~pass_on * other.biases[i]
        if mutate:
            child.mutate()
        return child

