import pandas as pd

def jaccard_similarity(set1, set2):
    """
    Calculates the Jaccard similarity between two sets.
    """
    return len(set1 & set2) / len(set1 | set2)

def remove_similar_news(df, threshold=0.9):
    """
    Removes similar news articles with the same Date and Press if Keywords are similar using Jaccard Similarity.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Date', 'Press', and 'Keywords' columns.
        threshold (float): Jaccard similarity threshold for considering two articles as duplicates.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with duplicates removed.
    """
    # Sort and group the DataFrame
    df = df.sort_values(by=['일자', '언론사']).reset_index(drop=True)
    cleaned_rows = []
    total_processed = 0
    total_erasure = 0
    
    clean_df = pd.DataFrame(columns=df.columns)

    for (date, press), group in df.groupby(['일자', '언론사']):
        group = group.reset_index(drop=True)
        total_processed += len(group)
        
        if len(group) == 1:
            clean_df = pd.concat([clean_df, group])
            continue
        
        to_drop = set()
        # Convert keywords into sets for comparison
        keyword_sets = [set(keywords.split(',')) for keywords in group['특성추출(가중치순 상위 50개)']]
        
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if j not in to_drop:
                    sim = jaccard_similarity(keyword_sets[i], keyword_sets[j])
                    if sim > threshold:
                        to_drop.add(j)  # Mark duplicate for removal
                        total_erasure +=1
        # Append non-duplicate rows
        clean_df = pd.concat([clean_df, group.drop(index=list(to_drop))])

    print(f"Total erasure: {total_erasure}")
    print(f"Total rows processed: {total_processed}")
    return clean_df

def get_similar_news(df, threshold=0.9):
    """
    Removes similar news articles with the same Date and Press if Keywords are similar using Jaccard Similarity.
    
    Args:
        df (pd.DataFrame): DataFrame with 'Date', 'Press', and 'Keywords' columns.
        threshold (float): Jaccard similarity threshold for considering two articles as duplicates.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with duplicates removed.
    """
    # Sort and group the DataFrame
    df = df.sort_values(by=['일자', '언론사']).reset_index(drop=True)
    cleaned_rows = []
    total_processed = 0
    total_erasure = 0
    
    clean_df = pd.DataFrame(columns=df.columns)

    for (date, press), group in df.groupby(['일자', '언론사']):
        group = group.reset_index(drop=True)
        total_processed += len(group)
              
        to_drop = set()
        # Convert keywords into sets for comparison
        keyword_sets = [set(keywords.split(',')) for keywords in group['특성추출(가중치순 상위 50개)']]
        
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if j not in to_drop:
                    sim = jaccard_similarity(keyword_sets[i], keyword_sets[j])
                    if sim > threshold:
                        to_drop.add(i)
                        to_drop.add(j)
                        total_erasure +=1
        # Append non-duplicate rows
        clean_df = pd.concat([clean_df, group.loc[list(to_drop)]])

    print(f"Total erasure: {total_erasure}")
    print(f"Total rows processed: {total_processed}")
    return clean_df


df = pd.read_csv('20010301-20241025.csv')

cleaned_df = get_similar_news(df, threshold=0.8)
cleaned_df.to_csv('20010301-20241025_similar.csv', index=False)

print(len(df))
print(len(cleaned_df))
