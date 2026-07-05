import pandas as pd

df = pd.read_csv('20010301-20241025_cleanup.csv')

def remove_numeric_words(keyword_string):
    words = keyword_string.split(',')
    filtered_words = [word for word in words if not word[0].isdigit()]
    return ','.join(filtered_words)

def check_numeric_words(keyword_string):
    words = keyword_string.split(',')
    filtered_words = [word for word in words if word[0].isdigit()]
    return ','.join(filtered_words)

df['특성추출(가중치순 상위 50개)'] = df['특성추출(가중치순 상위 50개)'].apply(check_numeric_words)

df.to_csv('20010301-20241025_number.csv')

