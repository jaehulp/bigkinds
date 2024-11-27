import pandas as pd
import networkx as nx
import time

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

G = nx.Graph()

for (kw1, kw2), weight in pair_counts.items():
    G.add_edge(kw1, kw2, weight = weight)

print(f'Generating graph done    {time.time() - start_time}')

eigen_centrality = nx.eigenvector_centrality(G, weight='weight')

print(f'eigenvector centrality done   {time.time() - start_time}')

top_eigen_keywords = sorted(eigen_centrality.items(), key=lambda x: x[1], reverse=True)
print("Top keywords by eigenvalue centrality:", top_eigen_keywords[:10])

centrality_df = pd.DataFrame(top_eigen_keywords, columns=['keyword', 'eigen_centrality'])

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

pos = nx.spring_layout(G)

print(f'something went wrong')

colors = centrality_df['cluster']

print(f'something went wrong')

nx.draw(G, pos, node_color=colors, with_labels=True, font_family='NanumGothic')

print(f'something went wrong')

plt.savefig('./temp_fig.png', dpi=300)

print(f'something went wrong')


