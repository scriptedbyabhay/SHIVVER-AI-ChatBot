import pandas as pd

def handle_missing_values(movies):
    cleaned_movies = movies.copy()
    
    cleaned_movies["overview"] = cleaned_movies["overview"].fillna("")
    
    cleaned_movies["tagline"] = cleaned_movies["tagline"].fillna("")
    
    return cleaned_movies


def standardize_text(movies):
    cleaned_movies = movies.copy()
    
    text_columns = [
        "title",
        "original_title",
        "overview",
        "tagline",
        "genre_names"
    ]
    
    for column in text_columns:
        cleaned_movies[column] = cleaned_movies[column].str.strip()
        # For every entry in those columns, it removes any accidental leading or trailing whitespace (spaces, tabs, or newlines at the very beginning or end of the text). For example, "  Inception " becomes "Inception"
        
        # The .lower() function is not used so as to preserve the presentation of movie names
        
    cleaned_movies["original_language"] = (
        cleaned_movies["original_language"].str.strip().str.lower()
    )
    # It targets the original_language column separately because language codes need stricter formatting
    
    return cleaned_movies


def process_date(movies):
    cleaned_movies = movies.copy()
    
    cleaned_movies["release_date"] = pd.to_datetime(
        cleaned_movies["release_date"], 
        errors="coerce"
    )
    
    cleaned_movies["release_year"] = (
        cleaned_movies["release_date"].dt.year.astype("Int64")
        # Unlike ordinary int64, Pandas' nullable Int64 (capital I) supports missing values
    )
    
    return cleaned_movies


def clean_dataset(movies):
    cleaned_movies = handle_missing_values(movies)
    
    cleaned_movies = standardize_text(cleaned_movies)
    
    cleaned_movies = process_date(cleaned_movies)
    
    return cleaned_movies

def validate_dataset(movies):
    print("\n--- DATASET VALIDATION REPORT ---")
    print("Total records:", len(movies))
    print("Duplicate IDs:", movies["id"].duplicated().sum())
    print("Duplicate rows:", movies.duplicated().sum())
    print("Missing titles:", movies["title"].isna().sum())
    print("Missing overviews:", movies["overview"].isna().sum())
    print("Missing taglines:", movies["tagline"].isna().sum())
    print("Missing release years:", movies["release_year"].isna().sum())
    print("Missing posters:", movies["poster_path"].isna().sum())
    print("\nData types:")
    print(movies.dtypes)