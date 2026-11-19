from modules.dataLoader import load_movies
from modules.movie_stats import (
    get_movies_by_year,
    get_movies_by_decade,
    get_common_genres
)

movies = load_movies()

print("\n--- MOVIES PER YEAR ---")
print(get_movies_by_year(movies).tail(10))

print("\n--- MOVIES PER DECADE ---")
print(get_movies_by_decade(movies))

print("\n--- MOST COMMON GENRES ---")
print(get_common_genres(movies))