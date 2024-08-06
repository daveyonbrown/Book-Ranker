from flask import Flask, render_template, request, jsonify

import pandas
from collections import defaultdict
from graph import Graph
import pickle
import requests




def main():

    g = Graph()
    # g.construct_simple_1()
    # g.save("graphstpath.pkl")
    # g.construct_simple_2()
    # g.save("graphrandomwalk.pkl")

    #
    g.load_graph("graphrandomwalk.pkl")

    print("Testing get_id method with book names from book_ids:")
    for book_id in g.book_ids:
        book_name = g.get_name(book_id)
        retrieved_id = g.get_id(book_name)
        print(f"Book Name: '{book_name}', Original ID: {book_id}, Retrieved ID: {retrieved_id}")
        assert book_id == retrieved_id, f"Mismatch for book '{book_name}': Original ID = {book_id}, Retrieved ID = {retrieved_id}"

    # print(g.book_ids_to_names[499])
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
    # book_n_edges = list(g.graph.edges(1, data = True))
    # print(len(book_n_edges))
    # for book in book_n_edges:
    #     print(g.get_name(book[1]))
    #


    # # #g = Graph()
    # source = 1
    # #
    # q = g.random_walk_sim(source, num_walks=1000, steps=100)
    # for a, b in q:
    #     print("Book", g.book_ids_to_names[a])

    # g.load_graph("graphstpath.pkl")

    # source_book_id = 1
    # print(f"Book name for ID {source_book_id}: {g.book_ids_to_names[source_book_id]}")
    #
    # shortest_paths = g.dijkstras_algorithm(source_book_id)
    # print("Dijkstra's algorithm results (top 5 closest books):")
    # for book_id, distance in shortest_paths:
    #     print(f"Book ID: {book_id}, Book Name: {g.book_ids_to_names[book_id]}, Distance: {distance}")
    #



























if __name__ == "__main__":
    main()


