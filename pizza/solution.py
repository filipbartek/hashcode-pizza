import math
import random

import matplotlib.pyplot as plt
import numpy as np


class Solution:
    def __init__(self, instance):
        self.instance = instance
        self.rects = np.empty((4, 0), dtype=np.int)
        self.taken = np.zeros(self.instance.pizza.shape, dtype=np.bool)
        self.score = 0
        assert (self.is_valid())

    def copy(self):
        res = Solution(self.instance)
        res.rects = np.copy(self.rects)
        res.taken = np.copy(self.taken)
        res.score = self.score
        return res

    def n_rects(self):
        return self.rects.shape[1]

    def is_valid(self):
        assert (self.score >= 0)
        assert (self.score <= self.instance.max_score())
        assert (self.score == self.calculate_score_from_taken())
        assert (self.score == self.calculate_score_from_rects())
        return True

    @staticmethod
    def rect_area(rect):
        return (rect[1] - rect[0]) * (rect[3] - rect[2])

    def add_rect(self, rect):
        assert (self.can_be_added(rect))
        self.rects = np.append(self.rects, np.transpose(np.matrix(rect)), axis=1)
        self.taken[rect[0]:rect[1], rect[2]:rect[3]] = True
        self.score = self.score + self.rect_area(rect)
        assert (self.is_valid())

    def remove_rect(self, i):
        rect = self.get_rect(i)
        self.taken[rect[0]:rect[1], rect[2]:rect[3]] = False
        self.rects = np.delete(self.rects, i, 1)
        self.score = self.score - self.rect_area(rect)
        assert (self.is_valid())

    def calculate_score_from_taken(self):
        return np.count_nonzero(self.taken)

    def calculate_score_from_rects(self):
        score_rects = 0
        for i in range(self.n_rects()):
            rect = self.get_rect(i)
            assert (self.instance.is_valid(rect))
            assert (np.all(self.taken[rect[0]:rect[1], rect[2]:rect[3]]))
            score_rects = score_rects + self.rect_area(rect)
        return score_rects

    def __str__(self):
        return str(self.rects)

    def write(self, outfile):
        S = self.n_rects()
        outfile.write(f'{S}\n')
        for i in range(S):
            rect = self.get_rect(i)
            r1 = rect[0]
            r2 = rect[1] - 1
            c1 = rect[2]
            c2 = rect[3] - 1
            outfile.write(f'{r1} {c1} {r2} {c2}\n')

    @staticmethod
    def read(instance, infile):
        res = Solution(instance)
        S = int(next(infile))
        for line, i in zip(infile, range(S)):
            r1, c1, r2, c2 = [int(x) for x in line.split()]
            rect = [r1, r2 + 1, c1, c2 + 1]
            res.add_rect(rect)
        assert (res.is_valid())
        return res

    def is_compatible(self, rect):
        t = self.taken[rect[0]:rect[1], rect[2]:rect[3]]
        return not np.any(t)

    def can_be_added(self, rect):
        if not self.instance.is_valid(rect):
            return False
        if not self.is_compatible(rect):
            return False
        return True

    def get_rect(self, i):
        assert (i < self.rects.shape[1])
        return np.asarray(self.rects[:, i]).flatten()

    def mutate_spawn(self, r=None, c=None):
        area = random.randrange(self.instance.L * 2, min(self.instance.H, self.instance.R * self.instance.C) + 1)
        rsize = random.randrange(1, area + 1)
        if rsize > self.instance.R:
            return None
        if area % rsize != 0:
            return None
        csize = area // rsize
        if csize > self.instance.C:
            return None
        if r is None:
            r1 = random.randrange(self.instance.R - rsize + 1)
        else:
            r1 = random.randrange(r - rsize + 1, r + 1)
        if c is None:
            c1 = random.randrange(self.instance.C - csize + 1)
        else:
            c1 = random.randrange(c - csize + 1, c + 1)
        rect = [r1, r1 + rsize, c1, c1 + csize]
        if not self.can_be_added(rect):
            return None
        res = self.copy()
        res.add_rect(rect)
        return res

    def mutate_pop(self):
        if self.n_rects() == 0:
            return None
        res = self.copy()
        i = random.randrange(self.rects.shape[1])
        res.remove_rect(i)
        return res

    def mutate_respawn(self):
        if self.n_rects() == 0:
            return None
        res = self.copy()
        i = random.randrange(self.rects.shape[1])
        rect = res.get_rect(i)
        res.remove_rect(i)
        r = random.randrange(rect[0], rect[1])
        c = random.randrange(rect[2], rect[3])
        return res.mutate_spawn(r=r, c=c)

    def mutate_changedim(self):
        if self.rects.shape[1] == 0:
            return None
        i = random.randrange(self.rects.shape[1])
        rect = self.get_rect(i)
        res = self.copy()
        res.remove_rect(i)
        j = random.randrange(4)
        rect[j] = rect[j] + random.choice([-1, 1])
        if res.can_be_added(rect):
            res.add_rect(rect)
            return res
        return None

    def mutate(self):
        f = random.choice([self.mutate_spawn, self.mutate_pop, self.mutate_respawn])
        #f = random.choice([self.mutate_respawn])
        res = f()
        return res

    def show(self):
        a = np.zeros(self.instance.pizza.shape, dtype=np.int)
        for i in range(self.rects.shape[1]):
            rect = self.get_rect(i)
            a[rect[0]:rect[1], rect[2]:rect[3]] = i + 1
        plt.matshow(a)

    def populate(self):
        for r1 in range(self.instance.R):
            print(r1)
            nextc1 = 0
            for c1 in range(self.instance.C):
                if c1 < nextc1:
                    continue
                for area in range(self.instance.H, self.instance.L * 2 - 1, -1):
                    for r2 in range(r1 + 1, min(r1 + self.instance.H, self.instance.R) + 1):
                        rsize = r2 - r1
                        if area % rsize != 0:
                            continue
                        csize = area // rsize
                        c2 = c1 + csize
                        rect = [r1, r2, c1, c2]
                        if self.can_be_added(rect):
                            self.add_rect(rect)
                            nextc1 = c2
                            break
                    if c1 < nextc1:
                        break
