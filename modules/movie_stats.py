import pandas as pd

def get_top_rated_movies(movies, limit=10, min_votes=100):
    filtered_movies = movies[
        movies["vote_count"] >= min_votes
    ]
    
    # min_votes = 100 because Movie A might have a rating of 9.8 but with 3 votes whereas, Movie B might have a rating of 8.9 with 15000+ votes
    
    top_movies = filtered_movies.sort_values(
        # sort_values() allows us to sort records by a column
        # In the above case, sorting is with regards to the 'vote_average' column
        by = "vote_average",
        ascending = False
        # Highest values are listed first
    )
    
    return top_movies.head(limit)


def get_most_popular_movies(movies, limit=10):
    popular_movies = movies.sort_values(
        by = "popularity",
        ascending = False
    )
    
    return popular_movies.head(limit)


def get_average_rating(movies):
    return movies["vote_average"].mean()


def get_average_runtime(movies):
    # return movies["runtime"].fillna("").mean() -> BAD CODE
    # In pandas, .mean() automatically ignores missing (NaN) values by default, so you do not need .fillna() at all
    
    return movies["runtime"].mean()


def get_movies_by_year(movies):
    movies_per_year = movies["release_year"].value_counts(
        dropna = True
        # Excludes records with missing release years
    )
    
    movies_per_year = movies_per_year.sort_index()
    return movies_per_year


def get_movies_by_decade(movies):
    valid_movies = movies.dropna(subset=["release_year"]).copy()
    
    valid_movies["decade"] = (
        valid_movies["release_year"].astype(int) // 10
    ) * 10
    
    # True Division (/). This operator always produces a decimal (float) result. Even if the numbers divide evenly. 
    # Floor Division (//). This operator drops the fractional part by rounding down toward negative infinity. For negative numbers, -7 // 2 evaluates to -4 rather than -3. If either input is a float (such as 7.0 // 2), the output remains a float (3.0).
    
    movies_per_decade = valid_movies["decade"].value_counts().sort_index()
    return movies_per_decade



def get_common_genres(movies, limit=10):
    genres = movies["genre_names"].dropna()
    genre_list = genres.str.split(",")
    
    all_genres = genre_list.explode()
    all_genres = all_genres.str.strip()
    
    genre_counts = all_genres.value_counts()
    
    return genre_counts.head(limit)