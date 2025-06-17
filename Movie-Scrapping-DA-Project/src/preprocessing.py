# src/preprocessing.py

import pandas as pd

def load_and_clean_data(path='data/imdb_top_250_movies.csv'):
    df = pd.read_csv(path)

    # Checking for nulls
    if df.isnull().sum().sum() > 0:
        df.dropna(inplace=True)

    # Feature Engineering: Decade
    df['decade'] = (df['year'] // 10) * 10

    return df

if __name__ == "__main__":
    df_cleaned = load_and_clean_data()
    print(df_cleaned.head())
