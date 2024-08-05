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
    print(g.book_ids_to_names[499])

    #rw = g.random_walk_sim(500, num_walks=1000, steps=100)

    #for a, b in rw:
    #    print(a, b)
    #    print(g.book_ids_to_names[a])

    print(len(list(g.graph.nodes())))
    print(len(list(g.graph.edges())))

    book_n_edges = sorted(list(g.graph.edges(500, data = True)), key=lambda x: x[2]["weight"], reverse=True)
    for book in book_n_edges:
        # book is a tuple like (node1, node2, attributes)
        node1, node2, attributes = book
        weight = attributes.get('weight', 'No weight attribute')  # Access the weight attribute
        print(f"Neighbor: {g.get_name(node2)}, Weight: {weight}")

    g = Graph()
    source = 15

    q = g.random_walk_sim(source, num_walks=1, steps=1)
    for a, b in q:
        print("Book", g.book_ids_to_names[a])



if __name__ == "__main__":
    main()


