import pandas as pd
import graph_tool.all as gt
import time

import multiprocessing

from itertools import combinations
from collections import Counter

from scipy.sparse import dok_matrix


data_list = ['20010301-20070228.xlsx',
             '20070301-20100930.xlsx',
             '20101001-20140930.xlsx',
             '20141001-20191031.xlsx',
             '20191101-20241025.xlsx']

df = pd.read_excel(data_list[4])

keywords = df['키워드']


start_time = time.time()

batch_size = 1000
pair_counts = Counter()
for start in range(0, len(df), batch_size):

    batch = df.iloc[start:start + batch_size]
    keyword_pair = []

    for keyword in batch['키워드']:
        keyword = keyword.split(',')
        keyword_pair.extend(combinations(keyword, 2))

    pair_counts.update(keyword_pair)

    print(f'Sample {start} Done')


def generate_graph():
    graph = gt.Graph(directed=False)

gt_graph = gt.Graph(directed=False)
weight_property = gt_graph.new_edge_property('float')
vertex_map = {}

for (kw1, kw2), weight in pair_counts.items():
    if kw1 not in vertex_map:
        vertex_map[kw1] = gt_graph.add_vertex()
    if kw2 not in vertex_map:
        vertex_map[kw2] = gt_graph.add_vertex()

    edge = gt_graph.add_edge(vertex_map[kw1], vertex_map[kw2])
    weight_property[edge] = weight

print(f'Generating graph done    {time.time() - start_time}')

gt_graph.edge_properties["weight"] = weight_property
eigenvector_property = gt.eigenvector(gt_graph, weight=weight_property)[1]

print(f'eigenvector centrality done   {time.time() - start_time}')

eigen_centrality_values = [(kw, eigenvector_property[vertex_map[kw]]) for kw in vertex_map]
top_keywords = sorted(eigen_centrality_values, key=lambda x: x[1], reverse=True)
print("Top keywords by eigenvalue centrality:", top_keywords[:10])

centrality_df = pd.DataFrame(top_keywords, columns=['keyword', 'eigen_centrality'])

from sklearn.cluster import KMeans

# Set up clustering using eigen_centrality values
n_clusters = 5  # Define the number of clusters
kmeans = KMeans(n_clusters=n_clusters)
centrality_df['cluster'] = kmeans.fit_predict(centrality_df[['eigen_centrality']])

print(f'Clustering done    {time.time() - start_time}')

# Display the clustering result
print("Keywords clustered by eigen_centrality:")
print(centrality_df)

# Optional: Visualize clustering in the network graph
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


fe = fm.FontEntry(
    fname=r'./font/NanumGothic.ttf', name='NanumGothic')                       
fm.fontManager.ttflist.insert(0, fe)  
plt.rcParams.update({'font.size': 18, 'font.family': 'NanumGothic'})
plt.rc('font', family='NanumGothic')

print(f'font imported')

plt.figure(figsize=(10, 10))

print(f'something went wrong')

pos = gt.sfdp_layout(gt_graph)

print(f'something went wrong')

colors = centrality_df['cluster']

print(f'something went wrong')

gt.graph_draw(gt_graph, pos=pos, vertex_text=gt_graph.vertex_index,
              vertex_font_size=8, edge_pen_width=weight_property,
              output_size=(1000, 1000), output="graph_tool_layout.png")

print(f'something went wrong')

plt.savefig('./temp_fig.png', dpi=300)

print(f'something went wrong')


