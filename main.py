import pandas
from collections import defaultdict
from graph import Graph
import pickle

def main():
    g = Graph()
    source = 500
    q = g.random_walk_sim(source, num_walks=1000, steps=100)

    for a, b in q:
        print("Book", a)
        print("Count", b)











if __name__ == "__main__":
    main()


