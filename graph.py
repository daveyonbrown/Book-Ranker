import pickle

import pandas as pd
import networkx as nx
from collections import defaultdict
import math


class Graph:
    def __init__(self):
        data = pd.read_csv("ratings.csv")
        books = pd.read_csv("books.csv")
        self.user_ids = list(data["user_id"])
        self.book_ids = list(data["book_id"])
        self.reviews = list(data["rating"])
        self.book_names = list(books["original_title"])
        self.graph = None




    def construct_simple(self):
        self.graph = nx.Graph() ##graph instance object
        nodes = set(self.book_ids) # each book is a node
        self.graph.add_nodes_from(nodes)

        weights = defaultdict(int) # tuple to int. book1 <---> book2: weigth
        user_books = defaultdict(list) # user : books they rated 5 stars
        num_reviews = defaultdict(int) # determines popularity of book. Used for balancing of weights.

        for i in range(len(self.reviews)):
            if self.reviews[i] == 5:
                user_books[self.user_ids[i]].append(self.book_ids[i]) #maps user id to the books they reviewed 5 stars
                num_reviews[self.book_ids[i]] += 1 # the popularity of each book, number of high reviews

        for books in user_books.values():
            for i in range(len(books)):
                for j in range(i + 1, len(books)):
                    weights[(books[i], books[j])] += 1 # adds 1 to weight between books if user rates both books highly



        for(book1, book2), weight in weights.items(): # gets the key value pair
            popularity = math.log1p(num_reviews[book1]) + math.log1p(num_reviews[book2])# used for balancing out overly popular books
            self.graph.add_edge(book1, book2, weight= weight / popularity if popularity != 0 else 0) #adds edge on the graph
        return self.graph


    def save(self, name): # save as binary file so the construct simple does not have to be run every time
        with open(name, 'wb') as file:
            pickle.dump(self.graph, file)

    def load_graph(self, name):
        with open(name, 'rb') as file:
            self.graph = pickle.load(file)


    def random_walk(self):
        return 0
    def reccommend_books(self):
        return 0











