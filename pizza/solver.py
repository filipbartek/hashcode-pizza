import math
import random

import matplotlib.pyplot as plt
import numpy as np

from pizza.solution import Solution


class Solver:
    def __init__(self, populate=True, generations=0):
        self.populate = populate
        self.generations = generations

    def solve(self, instance, solution=None):
        if solution is None:
            solution = Solution(instance)
        if self.populate:
            solution.populate()
        base_temp = 1
        scores = []
        temperatures = []
        best_solution = solution
        for i in range(self.generations):
            assert (solution.is_valid())
            scores.append(solution.score)
            temperature = base_temp * (1 - (i / self.generations))
            temperatures.append(temperature)
            if solution.score >= instance.max_score():
                break
            n = solution.mutate()
            if not n:
                continue
            scoredif = n.score - solution.score
            if scoredif > 0 or (temperature > 0 and math.exp(scoredif / temperature) >= random.random()):
                solution = n
                print(f'{i}: {solution.score}')
                if solution.score > best_solution.score:
                    best_solution = solution
        t = range(len(scores))
        plt.plot(t, np.asarray(temperatures) * instance.max_score(), '-', t, scores, '-')
        return solution
