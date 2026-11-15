import pandas as pd 

def filter_movies(
    movies,
    min_rating = None, 
    min_votes = None, 
    start_year = None,
    end_year = None,
    min_runtime = None,
    max_runtime = None
):
    filtered_movies = movies.copy()
    
    if min_rating is not None:
        filtered_movies = filtered_movies[
            filtered_movies["vote_average"] >= min_rating
    ]

    if min_votes is not None:
        filtered_movies = filtered_movies[
            filtered_movies["vote_count"] >= min_votes
    ]
    
    if start_year is not None:
        filtered_movies = filtered_movies[
            filtered_movies["release_year"] >= start_year
    ]
        
    if end_year is not None:
        filtered_movies = filtered_movies[
            filtered_movies["release_year"] <= end_year
    ]
        
    if min_runtime is not None:
        filtered_movies = filtered_movies[
            filtered_movies["runtime"] >= min_runtime
    ]
        
    if max_runtime is not None:
        filtered_movies = filtered_movies[
            filtered_movies["runtime"] <= max_runtime
    ]
    
    return filtered_movies    
