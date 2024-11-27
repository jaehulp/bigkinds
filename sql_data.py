import pandas as pd
import time

from itertools import combinations
from collections import Counter

from joblib import dok_matrix



data_list = ['20010301-20070228.xlsx',
             '20070301-20100930.xlsx',
             '20101001-20140930.xlsx',
             '20141001-20191031.xlsx',
             '20191101-20241025.xlsx']

df = pd.read_excel(data_list[0])

keywords = df['키워드']

keyword_pair = []

start_time = time.time()

for i, keyword in enumerate(keywords):
    keyword = keyword.split(',')
    keyword_pair.extend(combinations(keyword, 2))
    if i == 1:
        break
print(keyword_pair)