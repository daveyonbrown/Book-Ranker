import pandas
from collections import defaultdict
from graph import Graph
import pickle
import requests

def main():

    g = Graph()
    #g.construct_simple_2()
    #g.save("graphrandomwalk.pkl")

    g.load_graph("graphrandomwalk.pkl")
    print(g.book_ids_to_names[1])

    #rw = g.random_walk_sim(500, num_walks=1000, steps=100)

    #for a, b in rw:
    #    print(a, b)
    #    print(g.book_ids_to_names[a])

    print(len(list(g.graph.nodes())))
    print(len(list(g.graph.edges())))

    book_n_edges = list(g.graph.edges(1, data = True))
    print("Number of edges: ", len(book_n_edges))
    for edge in book_n_edges:
        print("Edge to: ", g.book_ids_to_names[edge[1]])


    #g = Graph()
    source = 499

    q = g.random_walk_sim(source, num_walks=1000, steps=100)
    for a, b in q:
        print("Book", g.book_ids_to_names[a])


























if __name__ == "__main__":
    main()


