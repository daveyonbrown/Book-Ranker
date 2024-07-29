import pandas
from collections import defaultdict
from graph import Graph
import pickle

def main():
    g = Graph()
    g.construct_simple()




    g.save("graph.pkl")




if __name__ == "__main__":
    main()


