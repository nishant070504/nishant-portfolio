
# src/scraping.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_imdb_top_250():
    url = "https://www.imdb.com/chart/top"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Primary selector for movie containers
    movies = soup.select('li.ipc-metadata-list-summary-item')
    
    if not movies:
        print("No movies found with primary selector. Trying fallback.")
        movies = soup.find_all('div', class_=lambda x: x and 'cli-children' in x)
    
    if not movies:
        print("No movies found. Check HTML selectors or page structure.")
        print("Dumping first 1000 characters of HTML for debugging:")
        print(soup.prettify()[:1000])
        return

    print(f"Found {len(movies)} movie elements")

    movie_data = []
    for movie in movies:
        try:
            # Extract title (includes rank)
            title_elem = movie.find('h3', class_=lambda x: x and 'ipc-title__text' in x)
            title_text = title_elem.text.strip() if title_elem else None
            if not title_text:
                print("Skipping movie: No title found")
                continue
            rank = title_text.split('.')[0].strip()
            name = title_text.split('. ')[1].strip() if '. ' in title_text else title_text

            # Extract year
            metadata = movie.find_all('span', class_=lambda x: x and 'cli-title-metadata-item' in x)
            year = metadata[0].text.strip() if metadata else None

            # Extract rating
            rating_elem = movie.find('span', class_=lambda x: x and 'ipc-rating-star' in x)
            if rating_elem and rating_elem.get('aria-label'):
                # Parse aria-label like "IMDb rating 9.2"
                rating_text = rating_elem.get('aria-label')
                rating = rating_text.split()[-1]  # Take last word (e.g., 9.2)
            else:
                rating = None
                print(f"Skipping movie {name}: No rating found")

            if not all([rank, name, year, rating]):
                print(f"Skipping incomplete data for movie: {title_text}")
                continue

            try:
                movie_data.append({
                    'rank': int(rank),
                    'name': name,
                    'year': int(year) if year else None,
                    'rating': float(rating) if rating else None
                })
            except ValueError as e:
                print(f"Error processing movie {name}: {e}")
                continue

        except (AttributeError, IndexError) as e:
            print(f"Error processing movie: {e}")
            continue

    if not movie_data:
        print("No valid data extracted. CSV will be empty.")
        return

    df = pd.DataFrame(movie_data)
    df.to_csv('data/imdb_top_250_movies.csv', index=False)
    print(f"Scraped {len(movie_data)} movies and saved to 'data/imdb_top_250_movies.csv'")

if __name__ == "__main__":
    scrape_imdb_top_250()
