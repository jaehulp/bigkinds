import pandas ad pd


df1 = pd.read_csv('20010301-20241025_checkend.csv')
df1.to_excel('', index=False)

df2 = pd.read_csv('불용어리스트.csv')
df2.to_excel('불용어리스트', index=False)