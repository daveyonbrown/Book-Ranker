# Project 3: Book Ranker

This project is a web application that generates book recommendations for the user.
## Installation

To run this project you must install the libraries:
1. jsonify
2. Flask
3. request

The program uses the following libraries to construct the graph:
1. NetworkX
2. pandas

## Usage

To construct the graphs, unzip the ratings.csv file and run main.py. This should create the 2 pickle files graphrandomwalk.pkl, graphstpath.pkl. (This should not be necessary since they are both included on Git)

To start the program run the app.py file. This should generate a link for the website in the terminal using flask.

To use the search tool, input the title of any book. It must be the exact title, capitalization does not matter. Then click the search button once. If the book that is being searched is invalid or not found, an error message will be presented to the user.


## Features

Generates 5 books each using Dijkstra's algorithm and the random walk algorithm. Will return to the user in the form of a table. The runtime for each algorithm will be provided under the tables.