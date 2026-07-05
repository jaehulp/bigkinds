import os
import pandas as pd

from konlpy.tag import Hannanum, Kkma, Okt

poser = Hannanum()
#poser = Kkma()
#poser = Okt()

with open('./stopwords/stopwords-ko.txt', 'r') as f:
    stopwords = f.read().splitlines()

df = pd.read_csv('20010301-20241025-100/word_features.csv')

words = df['keyword']
overlapped = words[words.isin(stopwords)]
print(overlapped)

overlapped.to_csv('stopwords.csv', index=False)

