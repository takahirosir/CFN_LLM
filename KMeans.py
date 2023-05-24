'''
To simulate graph-based clustering using the k-means algorithm on a random graph, you can follow these steps:
Generate a random graph using NetworkX.
Retrieve the node positions from the graph.
Apply the k-means algorithm to cluster the nodes based on their positions.
Visualize the clusters.
Here's the Python code that implements this simulation:.
要在随机图上使用k-均值算法模拟基于图的聚类，您可以按照以下步骤操作：
使用NetworkX生成随机图。
从图中检索节点位置。
应用k-均值算法根据节点的位置将其聚类。
可视化集群。
以下是实现此模拟的Python代码:
'''


import networkx as nx
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generate a random graph
# 生成一个随机图
def generate_random_graph(num_nodes, num_edges):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    return G

# Perform k-means clustering on node positions
# 应用k-均值算法根据节点的位置将其聚类
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
num_nodes = 50    # 50个节点
num_edges = 100     # 100条边
num_clusters = 3  # 3类

random_graph = generate_random_graph(num_nodes, num_edges)
labels = perform_kmeans_clustering(random_graph, num_clusters)
visualize_clusters(random_graph, labels)

# Print the clustering result
print("Node\tCluster")
for node, label in enumerate(labels):
    print(f"{node}\t{label}")
