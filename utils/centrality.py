
import graph_tool.all as gt

def eigenvector_centrality(graph, weight_property):

    value = gt.eigenvector(graph, weight=weight_property)[1]