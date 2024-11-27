import pandas as pd
import graph_tool.all as gt
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

keywords = df['본문']

print(keywords[1])
print(len(keywords[1]))