import pandas as pd

df1 = pd.read_csv('cluster_words.csv')
df2 = pd.read_csv('word_features.csv')
df3 = df2[:100]

df1.to_excel('cluster_words.xlsx', index=False)
df2.to_excel('word_features.xlsx', index=False)
df3.to_excel('word_features_top100.xlsx', index=False)
