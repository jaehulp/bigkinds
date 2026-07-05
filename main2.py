import os
import pandas as pd
import numpy as np

from utils.utils import *
from utils.cluster import recursive_concor
from utils.centrality import get_centrality

df = pd.read_csv('20010301-20241025_eng.csv')

#start_date = 20010301
#end_date = 20241025

date_zip = [(20010301, 20241025), (20010301, 20070228), (20070301, 20100930), (20101001, 20140930), (20141001, 20191031), (20191101, 20241025)]

def process(start_date, end_date):
    K = 50
    cluster_depth = 2

    assert start_date >= 20010301 and end_date <= 20241025

    output_dir = f'{start_date}-{end_date}-{K}'
    os.makedirs(output_dir, exist_ok=True)

    target_df = df[(df['일자'] >= start_date) & (df['일자'] <= end_date)]

    keyword_df = count_keyword(target_df)

    keywords = list(keyword_df['keyword'])
    pair_df = generate_pair(target_df, None)
    matrix = pair_to_matrix(keywords, pair_df)
    nx_g = matrix_to_nx_graph(matrix, keywords)

    #pair_df.to_csv(os.path.join(output_dir, 'pair_data.csv'), index=False)
    np.save('total_graph_array.npy', matrix)

    degree_centrality, eigenvector_centrality = get_centrality(nx_g)

    keyword_df['degree_centrality'] = list(degree_centrality.values())
    keyword_df['eigenvector_centrality'] = list(eigenvector_centrality.values())

    keyword_df.to_csv(os.path.join(output_dir, 'word_features.csv'), index=False)
    top_keywords = list(keyword_df['keyword'][:K])

    top_key_pair_df = generate_pair(target_df, top_keywords)
    top_key_matrix = pair_to_matrix(top_keywords, top_key_pair_df)
    g = matrix_to_graph(top_key_matrix, top_keywords)
    g.save(os.path.join(output_dir, 'key_graph.gt'))

    plot_graph(g, os.path.join(output_dir, 'graph.png'))

    cluster_dict = recursive_concor(top_key_matrix, max_depth=cluster_depth)

    plot_cluster_graph(g, cluster_dict, os.path.join(output_dir,'cluster_graph.png'), K)

    cluster_df(top_keywords, cluster_dict, output_dir)

for (start_date, end_date) in date_zip:
    print(f'Date {start_date}~{end_date}')
    process(start_date, end_date)