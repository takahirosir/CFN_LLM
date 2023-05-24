'''
层次聚类算法Hierarchical Clustering
'''
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hc

def generate_network(num_nodes, num_edges, connectivity):
    """
    Generates a random network with the specified number of nodes, edges, and connectivity.
    生成具有指定数量的节点、边缘节点和连接的随机网络。
    """
    graph = np.random.randint(0, 2, (num_nodes, num_nodes))
    return graph

def cluster_network(graph, method='ward'):
    """
    Clusters the network using the specified clustering algorithm.
    用层次聚类算法Hierarchical Clustering进行聚类
    """
    cluster_labels = hc.linkage(graph, method=method)
    return cluster_labels

def plot_clusters(cluster_labels):
    """
    Plots the clusters.
    画图
    """
    plt.figure()
    plt.scatter(cluster_labels[:, 0], cluster_labels[:,
                1], c=cluster_labels[:, 2], s=100)
    plt.show()

if __name__ == '__main__':
    num_nodes = 100
    num_edges = 1000
    connectivity = 0.5

    # Generate the network
    graph = generate_network(num_nodes, num_edges, connectivity)

    # Cluster the network
    cluster_labels = cluster_network(graph)

    # Plot the clusters
    plot_clusters(cluster_labels)

    plt.savefig('fig/clusting.png')

