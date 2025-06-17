import pandas as pd
from preprocessing import load_and_clean_data

def summary_statistics(df):
    stats = df.describe()
    print("Summary Statistics:\n", stats)
    return stats

def decade_analysis(df):
    result = df.groupby('decade')['rating'].agg(['mean', 'count'])
    print("\nDecade-wise Analysis:\n", result)
    return result

def find_outliers(df):
    q1 = df['rating'].quantile(0.25)
    q3 = df['rating'].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df['rating'] < q1 - 1.5 * iqr) | (df['rating'] > q3 + 1.5 * iqr)]
    print(f"\nFound {len(outliers)} outliers")
    return outliers

def rating_year_correlation(df):
    corr = df['year'].corr(df['rating'])
    print(f"\nCorrelation between year and rating: {corr:.2f}")
    return corr

def top_movies_per_decade(df, top_n=5):
    top_decade = df.groupby('decade').apply(lambda x: x.nlargest(top_n, 'rating')).reset_index(drop=True)
    print(f"\nTop {top_n} movies per decade:")
    print(top_decade[['decade', 'name', 'rating']])
    return top_decade

def save_analysis_results(df):
    summary_statistics(df).to_csv('output/summary_statistics.csv')
    decade_analysis(df).to_csv('output/decade_analysis.csv')
    find_outliers(df).to_csv('output/outliers.csv')
    top_movies_per_decade(df).to_csv('output/top_movies_per_decade.csv')
    print("Saved analysis results to 'output/' folder")

if __name__ == "__main__":
    df = load_and_clean_data()
    summary_statistics(df)
    decade_analysis(df)
    find_outliers(df)
    rating_year_correlation(df)
    top_movies_per_decade(df)
    save_analysis_results(df)
