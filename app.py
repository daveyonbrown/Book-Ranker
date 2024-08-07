from flask import Flask, render_template, request, jsonify
from graph import Graph
import time


#creates instance of flask app
app = Flask(__name__)




@app.route('/') #sets up root to url

def index():  #handls request to root of url
    return render_template('index.html') #loads the html template

@app.route('/search', methods=['POST']) # defines rrout for the search endpoinds that allows for POST request
def search():
    try:

        print("program start")
        #sorts the json data from the request
        data = request.get_json()

        print("getting request")
        #extracts book name from json data puts in lowercase to compare
        book_name = (data['book_name'])


        # #instance of graph
        graph = Graph()


        #gets book id from name and if DNE its an error
        book_id = graph.get_id(book_name)
        print("BOOK ID: ", book_id)
        if book_id is None:
            print("book err")
            return jsonify(error="Book not found"), 400

        print(book_id)

        print("Starting Dijkstra's algorithm")
        print(book_id)

        #sets and empty list to store the alg results
        dijkstra_results = []

        time3 = time.time()

        # runs random walk simulation for book recommendations
        recommendations = graph.random_walk_sim(book_id, num_walks=1000, steps=100)

        time4 = time.time()
        time_randomwalk = float(f"{time4-time3:.2f}")



        #runs dijkstras to find shortest path

        time1 = time.time()
        shortest_paths = graph.dijkstras_algorithm(book_id)
        time2 = time.time()
        time_dijkstra = float(f"{time2 - time1:.2f}")



        #not used in flask but to print out the results in console
        for book_id, distance in shortest_paths[:5]:
            print(f"Book ID: {book_id}, Book Name: {graph.book_ids_to_names[book_id]}, Distance: {distance}")
            dijkstra_results.append({'book_name': graph.get_name(book_id)})


        print("Starting random walk")




        #stores the book names from random walk
        book_names = [graph.get_name(rec[0]) for rec in recommendations]


        current_node = 1
        neighbors = list(graph.graph.neighbors(current_node))

        if not neighbors:
            print(f"No neighbors found for node {current_node}.")
        else:
            print(f"Edges for node {current_node} ({graph.get_name(current_node)}):")
            for neighbor in neighbors:
                edge_data = graph.graph.get_edge_data(current_node, neighbor)
                weight = edge_data["weight"] if "weight" in edge_data else "No weight"
                print(
                    f"Edge from {current_node} ({graph.get_name(current_node)}) to {neighbor} ({graph.get_name(neighbor)}) with weight {weight}")
    # not used in flask but to print out the results in console
        for a, b in recommendations:
            print("Book", graph.book_ids_to_names[a])

        #returns thw names and pushes them as a json response in the html file
        return jsonify(dijkstra_results=dijkstra_results, book_names=book_names,time_dijkstra=f"{time_dijkstra}s", time_randomwalk=f"{time_randomwalk}s")

    except Exception as e:
        return jsonify(error=str(e)), 400


if __name__ == '__main__':
    app.run(debug=True)
