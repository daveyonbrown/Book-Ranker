import pickle

import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict, deque
import math
import random
import heapq
import requests

import logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')



class Graph:
    def __init__(self):
        self.data = pd.read_csv("ratings.csv")
        self.books = pd.read_csv("books.csv")
        self.user_ids = list(self.data["user_id"])
        self.book_ids = list(self.data["book_id"])
        self.book_ids_inorder = list(range(1, 10001))
        self.reviews = list(self.data["rating"])
        self.titles = list(self.books["title"])
        self.book_names = list(self.books["original_title"])
        for i in range(len(self.book_names)):
            if(pd.isna(self.book_names[i])):
                self.book_names[i] = self.titles[i]

        self.book_ids_to_names = {} ##REMOVE THIS LATER
        self.authors = list()
        for i in range(1,10001):
            self.book_ids_to_names[i] = self.book_names[i-1]
        self.graph = None


    def get_name(self, book_id):  # get name takes in the books id num returns name

        return self.book_names[book_id - 1]  # has to do id - 1 to get rid of extra line

    def get_id(self, name):
        #converts input to lowecase for case sensitivity
        name = name.lower()
        #converts all books in list to lowercase
        book_names_lower = [book_name.lower() for book_name in self.book_names]

        #finds the index of the inputed names in the lowercase book names
        index = book_names_lower.index(name)
        return index + 1















    def construct_simple_1(self):
        """
        this will be used for the shortest path algorithm.
        The weights are smaller for books where a large number of people rated both highly
        :return:
        """
        self.graph = nx.Graph() ##graph instance object
        nodes = set(self.book_ids) # each book is a node
        self.graph.add_nodes_from(nodes)

        weights = defaultdict(int) # tuple to int. book1 <---> book2: weight
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

        edges = defaultdict(list)
        for (book1, book2), weight in weights.items():
            popularity = math.exp(math.log1p(num_reviews[book1]) + math.log1p(num_reviews[book2]))
            weight = popularity / weight
            edges[book1].append((book2, weight))
            edges[book2].append((book1, weight))

        for book in edges:  # now we get the top n
            if len(edges[book]) > 32:
                edges[book] = sorted(edges[book], key=lambda x: x[1], reverse=False)[:32]

        for book in edges:
            for neighbor, wght in edges[book]:
                self.graph.add_edge(book, neighbor, weight=wght)


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


        edges = defaultdict(list)#taking top n edges by weight. Reduces randomness in random walk function and increases computation speed
        for(book1, book2), weight in weights.items(): # gets the key value pair
            popularity = math.exp(math.log1p(num_reviews[book1]) + math.log1p(num_reviews[book2]))# used for balancing out overly popular books.
            weight = popularity / weight if popularity != 0 else 0
            edges[book1].append((book2, weight))
            edges[book2].append((book1, weight))

        for book in edges: ##now we get the top n
            if len(edges[book]) >= 50:
                top_edges = sorted(edges[book], key=lambda x: x[1], reverse=True)[:32] ## gets the top 50 edges by weight. could tune around to find optimal value
                for neighbor, wght in top_edges:
                    self.graph.add_edge(book, neighbor, weight=(math.log1p(wght* (10**5))))
            else:
                for neighbor, wght in edges[book]:
                    self.graph.add_edge(book, neighbor, weight=(math.log1p(wght*(10**5))))

        return self.graph


    def save(self, name): # save as binary file so the construct simple does not have to be run every time
        with open(name, 'wb') as file:
            pickle.dump(self.graph, file)

    def load_graph(self, name):
        with open(name, 'rb') as file:
            self.graph = pickle.load(file)
        logging.debug("Pickle File Successfully loaded")


    def dijkstras_algorithm(self, source): # algorithm 1
        """
        :param source: the source vertex (book)
        :return: returns the 5 nodes that have the smallest path to the source
        """

        #loads in the graph
        self.load_graph("graphstpath.pkl")

        #if sourse not in node of graph
        if source not in self.graph:
            return None, float('infinity')

        #sets source node to 0 and sers all nodes set to inifinty
        distances = {node: float('infinity') for node in self.graph.nodes()}
        distances[source] = 0
        # priority queue
        heap = [(0, source)]


        while heap:
            #pops nodes with shortest distance from heap
            current_distance, current_book = heapq.heappop(heap)

            # skips this node if distance is greater than current
            if current_distance > distances[current_book]:
                continue

            for neighbor, edge_data in self.graph[current_book].items():
                distance = current_distance + edge_data['weight']
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))
        #sorts all nodes by distance and getsd 5 smallest distances
        results = sorted([(book, dist) for book, dist in distances.items() if book != source], key=lambda x: x[1])[:5]
        return results





    def random_walk(self, source, steps = 100, alpha = 0.0): #algorithm 2
        """

        This method uses a more probabilistic approach for the reccomendation.
        This involves assigning probabilities to each edge based off the weight of the edges between the nodes.
        The higher the weight between nodes, the higher probability using that edge and stepping to the node it points to.
        The amount of times each node is stepped over is counted, and the


        :param source: The vertex searched by the user.
        :param steps: The amount of times the function randomly switches vertices
        """

        logging.debug("Starting random walk")

        current = source
        counts = defaultdict(int) #nodes mapped how many times the walk landed on the node
        for i in range(steps):

            neighbors = list(self.graph.neighbors(current))
            if len(neighbors) == 0: ## we will handle this case later. Possibly reccomend random books
                break


            weights = []
            for neighbor in neighbors:
                edge_data = self.graph.get_edge_data(current, neighbor)
                weight = edge_data["weight"]
                weights.append(weight)
            probabilities = []
            min_weight = min(weights)
            max_weight = max(weights)
            normalized_weights = [(w - min_weight) / (max_weight - min_weight) for w in weights]
            weights_sum = sum(normalized_weights)

            for weight in normalized_weights:
                probability = weight / weights_sum # turn into a probability distribution function
                probabilities.append(probability)

            # for nbr, prob in zip(neighbors, probabilities):
            #     print("Neighbor: ", self.get_name(nbr), "Probability: ", prob)
            # print(sum(probabilities), "Does this equal 1???")

            #print(f"Source: {source}, Neighbors: {neighbors}, Probabilities: {probabilities}")
            if random.random() < alpha and current != source:
                choice = source

            else:
                choice = random.choices(neighbors, probabilities, k=1)[0]
            if choice != source:
                counts[choice] += 1
            current = choice
        return counts




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
        print("Working?")
        self.load_graph("graphrandomwalk.pkl")
        counts = defaultdict(int)
        for i in range(num_walks):
            rw = self.random_walk(source, steps)
            for node, count in rw.items():
                counts[node] += count
        reccomendations = heapq.nlargest(5, counts.items(), key=lambda x: x[1])


        return reccomendations



    def reccommend_books_helper(self, source):
        rw = self.random_walk_sim(source, 1000, 100)
        return rw
