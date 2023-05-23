from sklearn.metrics import adjusted_rand_score, silhouette_score


# Assuming you have ground truth labels for the nodes
ground_truth_labels = [0, 0, 1, 1, 2, 2, 2, 1, 0, 0]


ari = adjusted_rand_score(ground_truth_labels, labels)
silhouette = silhouette_score(positions, labels)

print(f"Adjusted Rand Index: {ari}")
print(f"Silhouette Coefficient: {silhouette}")
