import numpy as np


class Instance:
    def __init__(self, R, C, L, H, pizza, name):
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.pizza = pizza
        self.name = name

    def __str__(self):
        return f'L={self.L} H={self.H}\n{self.pizza}\n'

    def is_valid(self, rect):
        if 0 > rect[0]:
            return False
        if rect[0] > rect[1]:
            return False
        if rect[1] > self.R:
            return False
        if 0 > rect[2]:
            return False
        if rect[2] > rect[3]:
            return False
        if rect[3] > self.C:
            return False
        pizza_slice = self.pizza[rect[0]:rect[1], rect[2]:rect[3]]
        if pizza_slice.size > self.H:
            return False
        n_tomatoes = pizza_slice.sum()
        if n_tomatoes < self.L:
            return False
        if pizza_slice.size - n_tomatoes < self.L:
            return False
        return True

    def max_score(self):
        return self.R * self.C

    @staticmethod
    def read(infile):
        R, C, L, H = [int(x) for x in next(infile).split()]
        p = np.empty([R, C], dtype=np.bool)
        for row in range(R):
            for ing, col in zip(infile.readline(), range(C)):
                if ing == 'T':
                    p[row, col] = True
                else:
                    assert (ing == 'M')
                    p[row, col] = False
        return Instance(R, C, L, H, p, infile.name)

    @staticmethod
    def random(R, C, L, H):
        p = np.random.randint(2, size=[R, C])
        return Instance(R, C, L, H, p, f'{R}_{C}_{L}_{H}')
