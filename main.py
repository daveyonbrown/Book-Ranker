import pandas
from collections import defaultdict
from graph import Graph
import pickle

def main():
    g = Graph()
    g.construct_simple_1()




    g.save("graphstpath.pkl")

    y = Graph()
    y.construct_simple_2()

    y.save("graphrandomwalk.pkl")





if __name__ == "__main__":
    main()


