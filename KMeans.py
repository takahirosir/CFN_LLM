'''
To simulate graph-based clustering using the k-means algorithm on a random graph, you can follow these steps:
Generate a random graph using NetworkX.
Retrieve the node positions from the graph.
Apply the k-means algorithm to cluster the nodes based on their positions.
Visualize the clusters.
Here's the Python code that implements this simulation:

'''


import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generate a random graph
def generate_random_graph(num_nodes, num_edges):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    return G

# Perform k-means clustering on node positions
def perform_kmeans_clustering(graph, num_clusters):
    node_positions = nx.spring_layout(graph)
    positions = np.array(list(node_positions.values()))
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(positions)
    return kmeans.labels_

# Visualize the clusters
def visualize_clusters(graph, labels):
    node_positions = nx.spring_layout(graph)
    nx.draw(graph, pos=node_positions, node_color=labels, cmap='viridis', with_labels=True)
    plt.show()

# Example usage
num_nodes = 50
num_edges = 100
num_clusters = 3

random_graph = generate_random_graph(num_nodes, num_edges)
labels = perform_kmeans_clustering(random_graph, num_clusters)
visualize_clusters(random_graph, labels)

# Print the clustering result
print("Node\tCluster")
for node, label in enumerate(labels):
    print(f"{node}\t{label}")
