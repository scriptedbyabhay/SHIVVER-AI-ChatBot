import pandas as pd

def search_by_title(movies, query):
    if not query or not query.strip():
        return pd.DataFrame()
    
    query = query.strip()
    # Get rid of whitspaces
    
    title_matches = movies["title"].astype(str).str.contains(
        query, case=False, na=False, regex=False
    )
    # case=False makes search case-insensitive
    # na=False prevents missing values from causing problems
    # regex=False treats special characters literally
    
    
    original_title_matches = movies["original_title"].fillna("").str.contains(
        query, case=False, na=False, regex=False
    )
    
    matching_movies = movies[title_matches | original_title_matches]
    return matching_movies


def search_by_cast(movies, star):
    if not isinstance(star, str) or not star.strip():
        return pd.DataFrame()
    
    star = star.strip()
    # Get rid of the whitspaces
    
    cast_matches = movies["top_5_cast"].fillna("").str.contains(
        star, case=False, na=False, regex=False
    )
    
    return movies[cast_matches]
    
    

def search_by_directors(movies, director):
    if not isinstance(director, str) or not director.strip():
        return pd.DataFrame()
    
    director = director.strip()
    
    director_matches = movies["director"].fillna("").str.contains(
        director, case=False, na=False, regex=False
    )
    
    return movies[director_matches]


def search_by_genre(movies, genre):
    if not isinstance(genre, str) or not genre.strip():
        return pd.DataFrame()
    
    genre = genre.strip()
    
    genre_matches = movies["genre_names"].fillna("").str.contains(
        genre, case=False, na=False, regex=False
    )
    
    return movies[genre_matches]