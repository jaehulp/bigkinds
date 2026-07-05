import pandas as pd

df_stopword = pd.read_csv('stopwords.csv')
stopword = df_stopword['keyword']
stopword = set(stopword)

df = pd.read_csv('20010301-20241025_cleanup.csv')
#df = pd.read_csv('20010301-20241025_rmsimilar_rmasia_rmnum.csv')


def remove_stopwords(text, stopword):
    words = text.split(',')
    filtered_words = [word for word in words if word not in stopword]
    deleted_words = [word for word in words if word in stopword]
    return ','.join(filtered_words)

def get_overlapped_words(df, column, stopword_set):
    keyword_words = set(word for row in df[column] for word in row.split(','))  # Extract all words from 'keyword'
    print(len(keyword_words))
    return keyword_words & stopword_set  # Find intersection with stopword list

overlapped_word_set = get_overlapped_words(df, '특성추출(가중치순 상위 50개)', stopword)
print(overlapped_word_set)

#df['특성추출(가중치순 상위 50개)'] = df['특성추출(가중치순 상위 50개)'].apply(lambda x: remove_stopwords(x, set(stopword)))
#df.to_csv('20010301-20241025_cleanup.csv', index=False)
