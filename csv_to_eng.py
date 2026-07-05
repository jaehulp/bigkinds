import pandas as pd

df = pd.read_csv('./data/20010301-20241025_cleanup.csv')

mapping_df = pd.read_excel('word_features_top100_english.xlsx')
mapping_dict = dict(zip(mapping_df['keyword'], mapping_df['eng']))

def replace_words(text, mapping_dict):
    words = text.split(',')
    replaced_words = [mapping_dict[word] if word in mapping_dict else word for word in words]  # Replace words
    return ','.join(replaced_words)

df['특성추출(가중치순 상위 50개)'] = df['특성추출(가중치순 상위 50개)'].apply(lambda x: replace_words(x, mapping_dict))
df.to_csv('20010301-20241025_eng.csv', index=False)

