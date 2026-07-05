import os
import pandas as pd

df = pd.read_csv('./data/20010301-20241025_cleanup.csv')


print(df['특성추출(가중치순 상위 50개)'][0])