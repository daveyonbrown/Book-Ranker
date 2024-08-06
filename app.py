from flask import Flask, render_template, request, jsonify
from graph import Graph


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
        book_name = data['book_name'].strip().lower()

        # #instance of graph
        graph = Graph()

        #gets book id from name and if DNE its an error
        book_id = graph.get_id(book_name)
        if book_id is None:
            print("book err")
            return jsonify(error="Book not found"), 400

        print("Starting Dijkstra's algorithm")

        #sets and empty list to store the alg results
        dijkstra_results = []

        #runs dijkstras to find shortest path
        shortest_paths = graph.dijkstras_algorithm(book_id)


        #not used in flask but to print out the results in console
        for book_id, distance in shortest_paths[:5]:
            print(f"Book ID: {book_id}, Book Name: {graph.book_ids_to_names[book_id]}, Distance: {distance}")
            dijkstra_results.append({'book_name': graph.get_name(book_id)})


        print("Starting random walk")

        #runs random walk simulation for book recommendations
        recommendations = graph.random_walk_sim(book_id, num_walks=1000, steps=100)

        #stores the book names from random walk
        book_names = [graph.get_name(rec[0]) for rec in recommendations]

        # not used in flask but to print out the results in console
        for a, b in recommendations:
            print("Book", graph.book_ids_to_names[a])

        #returns thw names and pushes them as a json response in the html file
        return jsonify(dijkstra_results=dijkstra_results, book_names=book_names)

    except Exception as e:
        return jsonify(error=str(e)), 400


if __name__ == '__main__':
    app.run(debug=True)
