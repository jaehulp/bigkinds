import os
import math
import random

import numpy as np
import pandas as pd
import graph_tool.all as gt
import networkx as nx

from itertools import combinations
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.cm as cm


def count_keyword(dataframe, key_column='특성추출(가중치순 상위 50개)', batch_size=1000):

    counts = Counter()

    for start in range(0, len(dataframe), batch_size):

        batch_keyword = []
        batch = dataframe.iloc[start:start + batch_size]

        for keyword in dataframe[key_column]:
            keyword = keyword.split(',')
            batch_keyword.extend(keyword)

    counts.update(batch_keyword)
    keyword_list = list(counts.items())

    df = pd.DataFrame.from_records(keyword_list, columns=['keyword', 'count'])

    df['frequency'] = df['count'] / len(dataframe)

    # Sort the DataFrame by count in descending order
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)

    return df

def generate_pair(dataframe, top_keywords, key_column='특성추출(가중치순 상위 50개)', batch_size=1000):

    pair_counts = Counter()

    if top_keywords is not None:
        dataframe[key_column] = dataframe[key_column].apply(
            lambda keywords: ','.join([k for k in keywords.split(',') if k in top_keywords])
        )
    
    for start in range(0, len(dataframe), batch_size):

        batch = dataframe.iloc[start:start + batch_size]
        keyword_pair = []

        for keyword in batch[key_column]:
            keyword = keyword.split(',')
            keyword_pair.extend(set(combinations(keyword, 2)))

        pair_counts.update(keyword_pair)
    pair_list = list(pair_counts.items())

    df = pd.DataFrame.from_records(pair_list, columns=["pair", "count"])
    df[['word 1', 'word 2']] = df["pair"].tolist()
    df = df.drop(columns=['pair'])
    df = df[['word 1', 'word 2', 'count']]

    return df

def pair_to_matrix(keywords, pair_df):

    # Initialize an empty KxK matrix
    K = len(keywords)
    adjacency_matrix = np.zeros((K, K), dtype=int)

    # Create a mapping from keyword to index
    keyword_to_index = {keyword: idx for idx, keyword in enumerate(keywords)}

    # Populate the matrix with pair counts
    for _, row in pair_df.iterrows():
        word1 = row['word 1']
        word2 = row['word 2']
        count = row['count']

        if word1 in keyword_to_index and word2 in keyword_to_index:
            i, j = keyword_to_index[word1], keyword_to_index[word2]
            adjacency_matrix[i, j] = count
            adjacency_matrix[j, i] = count  # Since the graph is undirected

    return adjacency_matrix

def matrix_to_graph(matrix, words):

    g = gt.Graph(directed=False)

    vertex_label = g.new_vertex_property("string")
    vertices = []
    for word in words:
        v = g.add_vertex()
        vertex_label[v] = word
        vertices.append(v)

    weight_property = g.new_edge_property("float")  
    row, col = matrix.nonzero() 
    for i, j in zip(row, col):
        if i <= j: 
            edge = g.add_edge(vertices[i], vertices[j])
            weight_property[edge] = matrix[i, j]

    g.edge_properties["weight"] = weight_property
    g.vertex_properties["label"] = vertex_label 

    return g

def matrix_to_nx_graph(matrix, keywords):

    index_to_keyword = {idx: keyword for idx, keyword in enumerate(keywords)}

    g = nx.from_numpy_array(matrix)
    nx.set_node_attributes(g, index_to_keyword, 'label')

    return g

def plot_graph(g, output_dir):

    pos = gt.sfdp_layout(g, gamma=10)  # Force-directed layout

    vprops = {"text": g.vertex_properties["label"],
                'size': 5,
                'font_size': 12,
                'shape': 'square',
                'fill_color': 'blue',
                'text_out_color': 'white',
                'text_out_width': 0.1
            }
    eprops={"penwidth": 0.05,
            'color': [0.4, 0.4, 0.4, 0.7]
}

    gt.graph_draw(g, pos=pos,
                    vertex_font_family='NanumGothic',
                    vertex_size=5,
                    vertex_text_position=1,
                    bg_color=[1, 1, 1, 1],
                    vprops = vprops,
                    eprops = eprops,
                    output_size=(1000,1000),
                    output=output_dir)

def rotate_point(x, y, angle):
    """Rotates (x, y) by 'angle' radians around the origin."""
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    return (x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta)

def plot_cluster_graph(g, cluster_info, output_dir, K):

    # Assign cluster colors
    cluster_ids = list(set(cluster_info.values()))
    color_map = cm.get_cmap('tab10', len(cluster_ids))  # Use a colormap for clusters
    cluster_color = {cluster_id: color_map(i) for i, cluster_id in enumerate(cluster_ids)}

    # Create vertex property for color
    color_prop = g.new_vertex_property("string")
    cluster = g.new_vertex_property('int')
    for v in g.vertices():
        cluster_id = cluster_info[int(v)]  # Get cluster ID for the vertex
        cluster[v] = cluster_id
        r, gr, b, _ = cluster_color[cluster_id]  # Extract RGB color
        color_prop[v] = f"#{int(r*255):02x}{int(gr*255):02x}{int(b*255):02x}"  # Convert to HEX

    # pos = gt.sfdp_layout(g, multilevel=True)  # Force-directed layout

    unique_cluster = set(cluster_info.values())

    radius = 6.5  # Larger radius to avoid cluster overlap
    offset = 0.2
    angle_increment = 2 * math.pi / len(unique_cluster)

    cluster_positions = {
        cluster: [
            radius * math.cos(i * angle_increment + 0.25 * math.pi) + radius + offset,
            radius * math.sin(i * angle_increment + 0.25 * math.pi) + radius + offset
        ]
        for i, cluster in enumerate(unique_cluster)
    }

    # Jittered grid layout for individual nodes within each cluster
    grid_size = 1  # Controls how widely the nodes are spread within a cluster
    node_offset = 0.1  # Small random jitter to prevent perfect alignment
    pos = g.new_vertex_property("vector<double>")

    tilt_angle = math.pi / 6

    for cluster_id in unique_cluster:
        cluster_center = cluster_positions[cluster_id]
        
        # Get nodes in this cluster
        cluster_nodes = [v for v in g.vertices() if cluster_info[int(v)] == cluster_id]
        
        # Create grid dimensions dynamically
        rows = int(math.ceil(math.sqrt(len(cluster_nodes))))  # Square-ish layout
        cols = (len(cluster_nodes) // rows) + 1
        
        # Assign grid positions with jitter
        for i, v in enumerate(cluster_nodes):
            row = i // cols
            col = i % cols

            x_offset = (col - cols / 2) * grid_size + random.uniform(-node_offset, node_offset)
            y_offset = (row - rows / 2) * grid_size + random.uniform(-node_offset, node_offset)

            x_rot, y_rot = rotate_point(x_offset, y_offset, tilt_angle)

            pos[v] = (cluster_center[0] + x_rot, cluster_center[1] + y_rot)


    vprops = {"text": g.vertex_properties["label"],
                'text_out_color': 'white',
                'text_out_width': 0.1,
                'size': 1,
                'font_size': 12,
                'shape': 'square',
                'fill_color': color_prop}
    eprops={"pen_width": 0.6,
            'color': [0.4, 0.4, 0.4, 0.7]}

    gt.graph_draw(g, pos=pos,
                    vertex_font_family='NanumGothic',
                    vertex_size=5,
                    vertex_text_position=1,
                    bg_color=[1,1,1,1],
                    vprops=vprops,
                    eprops=eprops,
                    output_size = (1000,1000),
                    output=output_dir
                    )

def cluster_df(top_keywords, cluster_info, output_dir):

    group_word = {group: [] for group in set(cluster_info.values())}
    for idx, group in cluster_info.items():
        group_word[group].append(top_keywords[idx])
    
    df = pd.DataFrame.from_dict(group_word, orient='index')
    df = df.transpose()

    df.to_csv(os.path.join(output_dir, 'cluster_words.csv'), index=False, header=False)