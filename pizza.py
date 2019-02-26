#!/usr/bin/env python3

import argparse
import random
import sys

import matplotlib.pyplot as plt

from pizza.instance import Instance
from pizza.solution import Solution
from pizza.solver import Solver


def main():
    random.seed(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('instance', nargs='?', type=argparse.FileType('r', encoding='utf_8'))
    parser.add_argument('-R', type=int)
    parser.add_argument('-C', type=int)
    parser.add_argument('-L', type=int)
    parser.add_argument('-H', type=int)
    parser.add_argument('--solution', type=argparse.FileType('r', encoding='utf_8'))
    parser.add_argument('--generations', type=int, default=0)
    parser.add_argument('--nopopulate', action='store_true')
    parser.add_argument('--out', '-o', type=argparse.FileType('w', encoding='utf_8'))
    parser.add_argument('--outinfo', type=argparse.FileType('w', encoding='utf_8'))

    namespace = parser.parse_args()

    if namespace.instance is not None:
        instance = Instance.read(namespace.instance)
    else:
        instance = Instance.random(namespace.R, namespace.C, namespace.L, namespace.H)
    print(instance)

    solution = None
    populate = not namespace.nopopulate
    if namespace.solution is not None:
        solution = Solution.read(instance, namespace.solution)
        populate = False

    solver = Solver(populate=populate, generations=namespace.generations)
    solution = solver.solve(instance, solution=solution)
    print(solution.score)

    outfile = namespace.out
    if outfile is None:
        outfilename = f'{instance.name}.{solution.score}.txt'
        outfile = open(outfilename, 'w')

    solution.write(outfile)

    if namespace.outinfo is not None:
        namespace.outinfo.write(f'Score: {solution.score}\n')

    solution.show()
    plt.show()

    sys.exit(0)


if __name__ == '__main__':
    main()
