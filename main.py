import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Random graph simulation
def simulate_random_graph(num_nodes, num_edges):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    return G

# Perform k-means clustering on the graph
def perform_kmeans_clustering(graph, num_clusters):
    # Get the adjacency matrix of the graph
    adjacency_matrix = nx.adjacency_matrix(graph)

    # Perform k-means clustering on the adjacency matrix
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(adjacency_matrix)

    # Get the cluster labels
    cluster_labels = kmeans.labels_

    return cluster_labels

# Example usage
random_graph = simulate_random_graph(10, 15)
num_clusters = 3

# Perform k-means clustering on the random graph
cluster_labels = perform_kmeans_clustering(random_graph, num_clusters)

# Visualization (optional)
pos = nx.spring_layout(random_graph)
nx.draw(random_graph, pos, node_color=cluster_labels, cmap='viridis', with_labels=True)
plt.show()
