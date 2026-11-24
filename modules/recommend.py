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
        "top_5_cast"
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
    feature_columns = [
        "overview",
        "genre_names",
        "tagline",
        "director",
        "top_5_cast",
        "title"
    ]
    
    feature_matrices = {}
    
    for column in feature_columns:
        movie_text = (
            prepared_movies[column]
            .fillna("")
            .astype(str)
        )
    
        tfidf = TfidfVectorizer(
            stop_words = "english",
            max_features = 20000,
            ngram_range = (1, 2),
            min_df = 1,
            max_df = 0.95
        )
        try:
            tfidf_matrix = tfidf.fit_transform(movie_text)
        # The above line of code is equivalent to 
        # tfidf.fit(movie_text)
        # tfidf_matrix = tfidf.transform(movie_text)
            feature_matrices[column] = tfidf_matrix
        
        except ValueError:
            feature_matrices[column] = None
    
    return feature_matrices

# STUDY THIS FUNCTION
def calculate_similarity(feature_matrices, movie_index, limit=10):
    feature_weights = {
        "overview": 3.0,
        "genre_names": 3.0,
        "tagline": 1.5,
        "director": 1.5,
        "top_5_cast": 1.0,
        "title": 0.5
    }
    
    weighted_scores = None
    total_weight = 0
    
    for feature, weight in feature_weights.items():
        tfidf_matrix = feature_matrices.get(feature)
        
        # Skips unavailable feature matrices
        if tfidf_matrix is None:
            continue
        
        # Skip features with no text for the selected movie
        movie_vector = tfidf_matrix[movie_index]
        if movie_vector.nnz == 0:
            continue
        
        # Calculate cosine similarity 
        similarity_scores = cosine_similarity(
            movie_vector,
            tfidf_matrix
        ).flatten()
    
        if weighted_scores is None:
            weighted_scores = similarity_scores * weight
            
        else:
            weighted_scores += similarity_scores * weight
        total_weight += weight
    
    if weighted_scores is None or total_weight == 0:
        return []   
    
    # Calculate final weighted similarity
    final_scores = weighted_scores/total_weight
    
    similar_indices = final_scores.argsort()[::-1]
    recommendations = []
    
    for index in similar_indices:
        if index == movie_index:
            continue
        
        recommendations.append(
            (int(index), float(final_scores[index]))
        )
        
        if len(recommendations) == limit:
            break
        
    return recommendations
    

def recommend_movies(movies, feature_matrices, movie_title, limit=10):
    matching_movies = movies[
        movies["title"].str.casefold() == movie_title.strip().casefold()
    ]
    
    if matching_movies.empty:
        print("Movie not found!")
        return pd.DataFrame()
    
    movie_index = matching_movies.index[0]
    
    recommendations = calculate_similarity(
        feature_matrices,
        movie_index,
        limit
    )
    
    if not recommendations:
        return pd.DataFrame()
    
    recommended_indices = [
        index for index, score in recommendations
    ]
    
    recommended_movies = movies.iloc[
        recommended_indices
    ].copy()
    
    recommended_movies["similarity_score"] = [
        score for index, score in recommendations
    ]
    
    return recommended_movies