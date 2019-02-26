.PHONY: all

all: out/a_example.out out/b_small.out out/c_medium.out out/d_big.out

out/a_example.out: data/a_example.in
	mkdir -p out
	PYTHONOPTIMIZE=TRUE ./pizza.py $+ --out $@ --outinfo $@.info --generations=10000

out/b_small.out: data/b_small.in
	mkdir -p out
	PYTHONOPTIMIZE=TRUE ./pizza.py $+ --out $@ --outinfo $@.info --generations=100000

out/c_medium.out: data/c_medium.in
	mkdir -p out
	PYTHONOPTIMIZE=TRUE ./pizza.py $+ --out $@ --outinfo $@.info

out/d_big.out: data/d_big.in
	mkdir -p out
	PYTHONOPTIMIZE=TRUE ./pizza.py $+ --out $@ --outinfo $@.info

