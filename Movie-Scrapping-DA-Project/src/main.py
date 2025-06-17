import argparse
from scraping import scrape_imdb_top_250
from preprocessing import load_and_clean_data
import analysis
import visualization

def main():
    parser = argparse.ArgumentParser(description="IMDb Top 250 Movies Pipeline")
    parser.add_argument('--scrape', action='store_true', help="Scrape IMDb Top 250")
    parser.add_argument('--analyze', action='store_true', help="Analyze the data")
    parser.add_argument('--visualize', action='store_true', help="Generate visualizations")
    args = parser.parse_args()

    if args.scrape:
        print("Starting scraping...")
        scrape_imdb_top_250()

    if args.analyze:
        print("Starting analysis...")
        df = load_and_clean_data()
        analysis.summary_statistics(df)
        analysis.decade_analysis(df)
        analysis.find_outliers(df)
        analysis.rating_year_correlation(df)
        analysis.top_movies_per_decade(df)
        analysis.save_analysis_results(df)

    if args.visualize:
        print("Starting visualization...")
        df = load_and_clean_data()
        visualization.plot_rating_distribution(df)
        visualization.plot_movies_by_decade(df)
        visualization.plot_top_3_movies(df)

if __name__ == "__main__":
    main()
