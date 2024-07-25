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
        for i in range(len(self.reviews)):
            if self.reviews[i] == 5:
                for j in range(i + 1, len(self.reviews))
                if self.reviews[j]







