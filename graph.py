import pandas as pd
import networkx as nx
from collections import defaultdict
class Graph:
    def __init__(self):
        data = pd.read_csv("ratings.csv")
        books = pd.read_csv("books.csv")
        self.user_ids = list(data["user_id"])
        self.book_ids = list(data["book_id"])
        self.reviews = list(data["rating"])
        self.book_names = list(books["original_title"])




    def construct_simple(self):
        graph = nx.Graph()
        nodes = set(self.book_ids)
        graph.add_nodes_from(nodes)

        weights = defaultdict(int)
        user_books = defaultdict(list)

        for i in range(len(self.reviews)):
            if self.reviews[i] == 5:
                user_books[self.user_ids[i]].append(self.book_ids[i]) #maps user id to the books they reviewed 5 stars

        for books in user_books.values():
            for i in range(len(books)):
                for j in range(i + 1, len(books)):
                    weights[(books[i], books[j])] += 1 # adds wei



        for(book1, book2), weight in weights.items(): # gets the key value pair, which is tuple to int
            graph.add_edge(book1, book2, weight=weight)









