import pandas as pd

data_list = ['20010301-20070228.xlsx',
             '20070301-20100930.xlsx',
             '20101001-20140930.xlsx',
             '20141001-20191031.xlsx',
             '20191101-20241025.xlsx']

df_list = []

for d in data_list:
    df = pd.read_excel(d)
    print(len(df))
    df_list.append(df)

df_all = pd.concat(df_list).sort_values(by=['일자']).reset_index(drop=True)
print(len(df_all))
df_all.to_csv('20010301-20241025.csv', index=False)
