
import numpy as np
from scipy.stats import pearsonr
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import matplotlib.pyplot as plt
from graph_tool.all import Graph, graph_draw, sfdp_layout, GraphView

def compute_correlation_matrix(matrix):
    n = matrix.shape[0] 
    correlation_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j:
                correlation_matrix[i, j] = 1.0 
            else:
                corr, _ = pearsonr(matrix[i], matrix[j])
                correlation_matrix[i, j] = corr
    
    return correlation_matrix

def concor(matrix, max_iter=25, tol=0.2):
    prev_matrix = matrix.copy()
    for iteration in range(max_iter):
        corr_matrix = compute_correlation_matrix(prev_matrix)
        
        delta = np.linalg.norm(corr_matrix - prev_matrix, ord='fro')
        print(f"Iteration {iteration + 1}: delta = {delta:.8f}")
        
        if delta < tol:
            print("Converged!")
            break
    
        prev_matrix = corr_matrix.copy()        

    return corr_matrix

def recursive_concor(matrix, indices=None, cluster_id=0, max_depth=2, depth=0, cluster_dict=None):
    if cluster_dict is None:
        cluster_dict = {}
    if indices is None:
        indices = np.arange(matrix.shape[0])
    
    # Base condition: assign a unique cluster ID to remaining nodes
    if depth >= max_depth or len(indices) <= 1:
        for i in indices:
            cluster_dict[i] = cluster_id
        return cluster_dict

    print(f"Recursion depth {depth}, splitting {len(indices)} nodes (Cluster ID: {cluster_id})")
    submatrix = matrix[indices][:, indices]
#    submatrix = submatrix / submatrix.max(axis=0)
    corr_matrix = concor(submatrix)
    corr_matrix = np.where(corr_matrix >= 0, 1, -1)

    unique_vectors = np.unique(corr_matrix, axis=0)

#    eigenvalues, eigenvectors = np.linalg.eigh(corr_matrix)
#    first_eigenvector = eigenvectors[:, -1]
#    cluster1 = indices[first_eigenvector >= 0]
#    cluster2 = indices[first_eigenvector < 0]

    match1 = np.all(corr_matrix == unique_vectors[0], axis=1)
    cluster1 = indices[match1]
    match2 = np.all(corr_matrix == unique_vectors[1], axis=1)
    cluster2 = indices[match2]

    if len(cluster1) + len(cluster2) != len(indices):
        raise RunTimeError('Clustering have missing classification.')  

    next_cluster_id1 = cluster_id * 2 + 1
    next_cluster_id2 = cluster_id * 2 + 2

    recursive_concor(matrix, cluster1, next_cluster_id1, max_depth, depth + 1, cluster_dict)
    recursive_concor(matrix, cluster2, next_cluster_id2, max_depth, depth + 1, cluster_dict)
    return cluster_dict
