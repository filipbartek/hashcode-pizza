# Pizza solver

Solver of the practice problem Pizza in [Hash Code](https://codingcompetitions.withgoogle.com/hashcode) 2019

Score:

* A: 15 / 15
* B: 42 / 42
* C: 49216 / 50000
* D: 894448 / 1000000
* Total: 943721 / 1050057

## Description

Starting in the top-left corner and proceeding row by row,
the program populates the pizza with slices as large as possible.
Once populated, simulated annealing attempts to improve the solution.

Mutations:

* Spawn a random slice
* Remove a random slice
* Respawn a random slice (remove the slice and spawn a new one intersecting with the old one)

The simulated annealing only yields good results on the instances A and B.
