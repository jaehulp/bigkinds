import graph_tool.all as gt
import networkx as nx


def get_centrality(nx_graph):
    degree_centrality = nx.degree_centrality(nx_graph)
    eigenvector_centrality = nx.eigenvector_centrality(nx_graph, weight='weight')

    return degree_centrality, eigenvector_centrality