import pandas
from collections import defaultdict
from graph import Graph
import pickle
import requests

def main():

    g = Graph()
    g.load_graph("graphrandomwalk.pkl")

    print("Number of nodes in the graph:", len(g.graph.nodes()))
    print("Number of edges in the graph:", len(g.graph.edges()))

    print(sorted(g.graph.nodes()))


    """
    g = Graph()
    source = 800
    q = g.random_walk_sim(source, num_walks=1000, steps=100)

    for a, b in q:
        print("Book", a)
        print("Count", b)
    """















if __name__ == "__main__":
    main()


