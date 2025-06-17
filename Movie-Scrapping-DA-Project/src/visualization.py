
# src/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from preprocessing import load_and_clean_data

# Ensure output directory exists
os.makedirs('output/charts', exist_ok=True)

def plot_rating_distribution(df):
    print("Generating rating distribution plot...")
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x='rating', bins=8, kde=True)
    plt.title('IMDb Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Density')
    plt.savefig('output/charts/rating_distribution.png')
    plt.close()
    print("Saved rating_distribution.png")

def plot_movies_by_decade(df):
    print("Generating movies by decade plot...")
    decade_counts = df['decade'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=decade_counts.index, y=decade_counts.values)
    plt.title('Number of Top Movies by Decade')
    plt.xlabel('Decade')
    plt.ylabel('Number of Movies')
    plt.savefig('output/charts/movies_by_decade.png')
    plt.close()
    print("Saved movies_by_decade.png")

def plot_top_3_movies(df):
    print("Generating top 3 movies plot...")
    top3 = df.nlargest(3, 'rating')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='rating', y='name', data=top3)
    plt.title('Top 3 Highest Rated Movies')
    plt.xlabel('Rating')
    plt.ylabel('Movie Name')
    plt.savefig('output/charts/top3_rated.png')
    plt.close()
    print("Saved top3_rated.png")

if __name__ == "__main__":
    try:
        df = load_and_clean_data()
        print(f"Loaded DataFrame with {len(df)} rows")
        if df.empty:
            print("Error: DataFrame is empty")
            exit(1)
        plot_rating_distribution(df)
        plot_movies_by_decade(df)
        plot_top_3_movies(df)
    except Exception as e:
        print(f"Error in visualization.py: {e}")
