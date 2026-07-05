import pandas as pd

df = pd.read_csv('./data/20010301-20241025_rmall.csv')
modified_words_set = set()

def remove_end(text):
    words = text.split(',')
    modified_words = set()
    for word in words:
        if word.endswith('들'):
            modified_words.add(word[:-1])
            modified_words_set.add(word[:-1])
        else:
            modified_words.add(word)

    return ','.join(set(modified_words))

df['특성추출(가중치순 상위 50개)'] = df['특성추출(가중치순 상위 50개)'].apply(remove_end)

df.to_csv('20010301-20241025_cleanup.csv', index=False)

print(modified_words_set)
#df_a = pd.DataFrame({'Word': list(modified_words_set)})
#df_a.to_csv('20010301-20241025_checkend.csv', index=False)
