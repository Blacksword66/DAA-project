from collections import defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx

# Set matplotlib to a non-interactive backend to avoid GUI issues on macOS
plt.switch_backend('Agg')

# Push-Relabel for Maximum Flow
class PushRelabel:
    def __init__(self, graph, source, sink):
        self.graph = graph          # residual capacity graph
        self.source = source        # source node
        self.sink = sink            # sink node
        self.height = {}            # height of nodes
        self.excess = {}            # excess flow of nodes
        self.neighbor_index = {}    # current neighbor to check for each node

        # Initialize height, excess, and neighbor index for each node
        for node in self.graph:
            self.height[node] = 0
            self.excess[node] = 0
            self.neighbor_index[node] = 0

        # Set the source node's height to the number of nodes
        self.height[self.source] = len(self.graph)

    def initialize_preflow(self):
        for neighbor, capacity in self.graph[self.source].items():
            self.graph[self.source][neighbor] -= capacity
            if neighbor not in self.graph:
                self.graph[neighbor] = {}
            self.graph[neighbor][self.source] = capacity
            self.excess[neighbor] = capacity
            self.excess[self.source] -= capacity

    def push(self, u, v):
        push_flow = min(self.excess[u], self.graph[u][v])
        self.graph[u][v] -= push_flow
        if v not in self.graph:
            self.graph[v] = {}
        if u in self.graph[v]:
            self.graph[v][u] += push_flow
        else:
            self.graph[v][u] = push_flow
        self.excess[u] -= push_flow
        self.excess[v] += push_flow

    def relabel(self, u):
        min_height = float('inf')
        for v, capacity in self.graph[u].items():
            if capacity > 0:
                min_height = min(min_height, self.height[v])
        if min_height < float('inf'):
            self.height[u] = min_height + 1

    def discharge(self, u):
        while self.excess[u] > 0:
            neighbors = list(self.graph[u].keys())
            if self.neighbor_index[u] < len(neighbors):
                v = neighbors[self.neighbor_index[u]]
                if self.graph[u][v] > 0 and self.height[u] == self.height[v] + 1:
                    self.push(u, v)
                else:
                    self.neighbor_index[u] += 1
            else:
                self.relabel(u)
                self.neighbor_index[u] = 0

    def max_flow(self):
        self.initialize_preflow()
        active_nodes = [u for u in self.graph if u != self.source and u != self.sink]
        while any(self.excess[u] > 0 for u in active_nodes):
            for u in active_nodes:
                if self.excess[u] > 0:
                    self.discharge(u)
        return self.excess[self.sink]

# Bellman-Ford for Shortest Path
def bellman_ford(graph, source):
    distance = {v: float('inf') for v in graph}
    distance[source] = 0
    for i in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
    return distance

# Function to visualize the graph
def visualize_graph(graph, source, sink, filename='static/graph.png'):
    try:
        G = nx.DiGraph()  # create a directed graph
        for u in graph:
            for v, capacity in graph[u].items():
                G.add_edge(u, v, capacity=capacity)  # add edges with capacities as labels
        
        pos = nx.spring_layout(G)  # layout for visualization
        plt.figure(figsize=(10, 6))
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

        # Draw edges
        edge_labels = {(u, v): f"{capacity}" for u, v, capacity in G.edges(data='capacity')}
        nx.draw_networkx_edges(G, pos, edge_color='black', arrowstyle='-|>', arrowsize=20)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        # Highlight source and sink nodes
        nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', node_size=800, label="Source")
        nx.draw_networkx_nodes(G, pos, nodelist=[sink], node_color='orange', node_size=800, label="Sink")

        plt.title("Graph Visualization with Capacities")
        plt.savefig(filename)  # Save the graph as an image
    except Exception as e:
        print(f"Error during visualization: {e}")
    finally:
        plt.close()  # Close the plot to free memory

# Sample graph input for testing
graph = {
    0: {1: 10, 2: 5},
    1: {2: 2, 3: 1},
    2: {1: 3, 3: 9, 4: 2},
    3: {4: 4},
    4: {}
}
source, sink = 0, 4

# Running Push-Relabel for Maximum Flow
pr = PushRelabel(graph, source, sink)
print("Maximum Flow:", pr.max_flow())

# Running Bellman-Ford for Shortest Path
print("Shortest Path from source:", bellman_ford(graph, source))

# Visualize the graph
visualize_graph(graph, source, sink)