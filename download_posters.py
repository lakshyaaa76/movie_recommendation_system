import os
import re
import pickle
import pandas as pd
import requests
import time

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Poster folder
os.makedirs('posters', exist_ok=True)


# Fetch poster function
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=be469d5a581c16eb16df94ca14d21165&language=en-US'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"TMDb request failed for ID {movie_id}")
        return None

    data = response.json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None  # or use a placeholder image URL


# Download posters
for idx, row in movies.iterrows():
    movie_id = row['movie_id']
    title = row['title']

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f'posters/{safe_title}.jpg'

    if os.path.exists(filename):
        print(f"Already exists: {title}")
        continue

    try:
        poster_url = fetch_poster(movie_id)

        if poster_url:
            img_data = requests.get(poster_url).content
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded: {title}")
        else:
            print(f"No poster available: {title}")

        # Optional: small delay to avoid hitting TMDb rate limits
        time.sleep(0.1)

    except Exception as e:
        print(f"Failed to download {title}: {e}")
