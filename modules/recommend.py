import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def prepare_movie_text(movies):
    prepared_movies = movies.copy()
    
    text_columns = [
        "title",
        "overview",
        "tagline",
        "genre_names",
        "director",
        "top_5_Cast"
    ]
    
    for column in text_columns:
        if column not in prepared_movies.columns:
            prepared_movies[column] = ""
            
        prepared_movies[column] = (
            prepared_movies[column].fillna("").astype(str).str.strip()
    )
        
    prepared_movies["combined_features"] = (
        prepared_movies[text_columns].agg(" ".join, axis=1)
    )
    
    return prepared_movies

# STUDY THIS FUNCTION
def build_tfidf_matrix(prepared_movies):
    movie_text = prepared_movies["combined_features"].fillna("")
    
    tfidf = TfidfVectorizer(
        stop_words = "english",
        max_features = 30000,
        ngram_range = (1, 2),
        min_df = 2,
        max_df = 0.95
    )
    
    tfidf_matrix = tfidf.fit_transform(movie_text)
    # The above line of code is equivalent to 
    # tfidf.fit(movie_text)
    # tfidf_matrix = tfidf.transform(movie_text)
    
    return tfidf, tfidf_matrix

# STUDY THIS FUNCTION
def calculate_similarity(tfidf_matrix, movie_index, limit=10):
    similarity_scores = cosine_similarity(tfidf_matrix[movie_index], tfidf_matrix).flatten()
    
    similar_indices = similarity_scores.argsort()[::-1]
    
    recommendations = []
    
    for index in similar_indices:
        if index == movie_index:
            continue
        
        recommendations.append(
            (int(index), float(similarity_scores[index]))
        )
        
        if len(recommendations) == limit:
            break
        
    return recommendations


def recommend_movies(movies, tfidf_matrix, movie_title, limit=10):
    matching_movies = movies[
        movies["title"].str.casefold() == movie_title.strip().casefold()
    ]
    
    if matching_movies.empty:
        print("Movie not found!")
        return pd.DataFrame()
    
    movie_index = matching_movies.index[0]
    
    recommendations = calculate_similarity(
        tfidf_matrix,
        movie_index,
        limit
    )
    
    recommended_indices = [
        index for index, score in recommendations
    ]
    
    recommended_movies = movies.iloc[recommended_indices].copy()
    
    recommended_movies["similarity_score"] = [
        score for index, score in recommendations
    ]
    
    return recommended_movies