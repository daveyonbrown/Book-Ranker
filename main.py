from flask import Flask, render_template, request, jsonify

import pandas
from collections import defaultdict
from graph import Graph
import pickle
import requests




def main():

    g = Graph()
    g.construct_simple_1()
    g.save("graphstpath.pkl")

    # g.load_graph("graphstpath.pkl")
    # print(g.book_ids_to_names[500])
    #
    # #rw = g.random_walk_sim(500, num_walks=1000, steps=100)
    #
    # #for a, b in rw:
    # #    print(a, b)
    # #    print(g.book_ids_to_names[a])
    #
    # print(len(list(g.graph.nodes())))
    # print(len(list(g.graph.edges())))
    #
    # book_n_edges = list(g.graph.edges(500, data = True))
    # print("Number of edges: ", len(book_n_edges))
    # for edge in book_n_edges:
    #     print("Edge to: ", g.book_ids_to_names[edge[1]])
    #
    #
    # #g = Graph()
    # source = 500
    # q = g.random_walk_sim(source, num_walks=1000, steps=100)
    #
    # for a, b in q:
    #     print("Book", g.book_ids_to_names[a])
    #     print("Count", b)


    source_book_id = 1
    print(f"Book name for ID {source_book_id}: {g.book_ids_to_names[source_book_id]}")

    shortest_paths = g.dijkstras_algorithm(source_book_id)
    print("Dijkstra's algorithm results (top 5 closest books):")
    for book_id, distance in shortest_paths:
        print(f"Book ID: {book_id}, Book Name: {g.book_ids_to_names[book_id]}, Distance: {distance}")


if __name__ == "__main__":
    main()


