from flask import Flask, render_template, request
from algorithms import PushRelabel, bellman_ford, visualize_graph  # Ensure visualize_graph is imported

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    # Extract input data (e.g., network details, source, sink)
    source = int(request.form.get('source'))
    sink = int(request.form.get('sink'))
    
    # Initialize graph and algorithms
    graph = {
        0: {1: 10, 2: 5},
        1: {2: 2, 3: 1},
        2: {1: 3, 3: 9, 4: 2},
        3: {4: 4},
        4: {}
    }  # Replace with network data or user input if applicable

    # Calculate maximum flow and shortest path
    pr = PushRelabel(graph, source, sink)
    max_flow = pr.max_flow()
    shortest_path = bellman_ford(graph, source)

    # Visualize the graph and save the image
    graph_image_path = 'static/graph.png'  # Path where the image will be saved
    visualize_graph(graph, source, sink, filename=graph_image_path)

    # Pass results and image path to HTML for display
    return render_template('result.html', max_flow=max_flow, shortest_path=shortest_path, graph_image_path=graph_image_path)

if __name__ == '__main__':
    app.run(debug=True)