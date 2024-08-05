from flask import Flask, render_template, request, jsonify
from graph import Graph


#creates instance of flask app
app = Flask(__name__)


#instance of graph
graph = Graph()



@app.route('/') #sets up root to url

def index():  #handls request to root of url
    return render_template('index.html') #loads the html template

@app.route('/search', methods=['POST']) # defines rrout for the search endpoinds that allows for POST request
def search():
    try:


        #sorts the json data from the request
        data = request.get_json()

        #extracts book ID from json data and converts to integer
        book_id = int(data['book_id'])

        source = 500
        # q = graph.random_walk_sim(book_id, num_walks=1000, steps=100)
        #
        # for a, b in q:
        #     print("Book", graph.book_ids_to_names[a])
        #     print("Count", b)

        # #gets the book name that is attached to book ID using graph
        # book_name = graph.get_name(book_id)

        print(book_id)

        # #returns the book name in JSON text
        # return jsonify(book_name=book_name)



        # Get the random walk recommendations
        recommendations = graph.random_walk_sim(book_id, num_walks=1000, steps=100)

        # Get the book names for the recommendations
        book_names = [graph.get_name(rec[0]) for rec in recommendations]

        return jsonify(book_names=book_names)


    #errror if runs into any 400 status codes
    except Exception as e:
        return jsonify(error=str(e)), 400


if __name__ == '__main__':
    app.run(debug=True)
