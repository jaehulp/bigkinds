import pandas as pd

df = pd.read_csv('20010301-20241025_cleanup_08.csv')

target = ['범죄>성범죄>성추행', '범죄>성범죄>성희롱', '범죄>성범죄>성폭행', '사고>산업사고>붕괴', '범죄>범죄일반>유괴/납치']
#df = df[df['사건/사고 분류1'].isin(['범죄>성범죄>성추행', '범죄>성범죄>성희롱'])]

df = df[~(df['언론사']=='아시아투데이') & ~(df['사건/사고 분류1'].isin(target))]

df.to_csv('20010301-20241025_cleanup_08_asia.csv', index=False)

