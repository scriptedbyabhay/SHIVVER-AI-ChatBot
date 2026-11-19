from modules.dataLoader import load_movies

from modules.recommend import (
    prepare_movie_text,
    build_tfidf_matrix,
    recommend_movies
)


# Load enriched dataset
movies = load_movies()

# Prepare movie text
prepared_movies = prepare_movie_text(movies)

# Generate TF-IDF matrix
tfidf, tfidf_matrix = build_tfidf_matrix(prepared_movies)

# Ask user for a movie title
movie_title = input("\nEnter a horror movie: ")

# Generate recommendations
recommendations = recommend_movies(
    prepared_movies,
    tfidf_matrix,
    movie_title,
    limit=10
)

# Display results
if not recommendations.empty:

    print("\n--- RECOMMENDED MOVIES ---")

    for _, movie in recommendations.iterrows():

        print("\nTitle:", movie["title"])
        print("Release Year:", movie["release_year"])
        print("Rating:", movie["vote_average"])
        print("Director:", movie["director"])
        print("Similarity:", round(movie["similarity_score"], 4))