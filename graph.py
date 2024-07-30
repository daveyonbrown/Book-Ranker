import pickle

import pandas as pd
import networkx as nx
from collections import defaultdict
import math
import random


class Graph:
    def __init__(self):
        data = pd.read_csv("ratings.csv")
        books = pd.read_csv("books.csv")
        self.user_ids = list(data["user_id"])
        self.book_ids = list(data["book_id"])
        self.reviews = list(data["rating"])
        self.book_names = list(books["original_title"])
        self.graph = None



    def construct_simple_1(self):
        """
        this will be used for the shortest path algorithm.
        The weights are smaller for books where a large number of people rated both highly
        :return:
        """
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

        for (book1, book2), weight in weights.items():  # gets the key value pair
            popularity = math.log1p(num_reviews[book1]) + math.log1p(
                num_reviews[book2])  # used for balancing out overly popular books.
            self.graph.add_edge(book1, book2, weight= popularity / weight)  # adds edge on the graph. This is inversely related to the number of people who rated both books highly
        return self.graph


    def construct_simple_2(self):
        """
        This will be used for the random walk.
        Here, the weights are higher for books where a large number of people rated both highly.

        :return:
        """
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
            popularity = math.log1p(num_reviews[book1]) + math.log1p(num_reviews[book2])# used for balancing out overly popular books.
            self.graph.add_edge(book1, book2, weight= weight / popularity if popularity != 0 else 0) #adds edge on the graph
        return self.graph


    def save(self, name): # save as binary file so the construct simple does not have to be run every time
        with open(name, 'wb') as file:
            pickle.dump(self.graph, file)

    def load_graph(self, name):
        with open(name, 'rb') as file:
            self.graph = pickle.load(file)


    def dijkstras_algorithm(self, source): # algorithm 1
        """

        :param source:
        :return: returns
        """

    def random_walk(self, source, steps = 100): #algorithm 2
        """

        This method uses a more probabilistic approach for the reccomendation.
        This involves assigning probabilities to each edge based off the weight of the edges between the nodes.
        The higher the weight between nodes, the higher probability using that edge and stepping to the node it points to.
        The amount of times each node is stepped over is counted, and the


        :param source: The vertex searched by the user.
        :param steps: The amount of times the function randomly switches vertices
        """
        self.load_graph("graph.pkl")

        current = source
        counts = defaultdict(int) #nodes mapped how many times the walk landed on the node
        for i in range(steps):
            counts[current] += 1
            neighbors = list(self.graph.neighbors(current))
            weights = []
            for neighbor in neighbors:
                weights.append(self.graph.get_edge_data(current, neighbor)["weight"])
                probabilities = [weight / sum(weights) for weight in weights] # Turns the weights of the edges into a probability distribution
                choice = random.choices(neighbors, probabilities, k=1)[0] ## randomly selects a neighboring node to visit
        counts[choice] += 1
        return counts ##this is one random walk. Run many times

    def random_walk_sim(self, source, num_walks, steps = 100):
        """
        here we test out the best number of random walks to do.
        Ex: running 1 random walk leaves it susceptible to outliers, meaning a book can get reccommended that has almost nothing to do with the orgiginal book
        Although doing 1 million walks almost certainly removes the possibility of outliers getting reccommended, this likely just wastes time and is not necessary
        So, we try to find a number of walks where the accuracy starts to converge.
        :param source: where the random walk should start
        :param num_walks: The parameter we are trying to figure out by simulation; the amount of times we run the random walk function
        :param steps: used in the random walk function
        :return: a mapping to nodes and how many times the random walk function landed on them. The top 5 will be taken as reccomendation
        """











    def reccommend_books(self):
        return 0











