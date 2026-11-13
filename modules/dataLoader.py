from pathlib import Path
import pandas as pd

def load_movies():
    f = Path("dataset")/"cleaned_movies.csv"
    
    if not f.is_file():
        raise FileNotFoundError("Data absent.")
    
    # try:
    #     movies = pd.read_csv(f)
    #     return movies
    # except pd.errors.ParserError:
    #     raise
    #     # The 'raise' keyword is used so that the message is passed up to the code that called the function
    #     # If 'main.py' calls load_movies() and loading fails, 'main.py' should know that it failed rather than receiving None and treating it like a valid DataFrame
    # except PermissionError:
    #     raise
   
    # We can remove both the 'except' blocks because Python automatically propagates unhandled exceptions
    # You don't need to catch an exception just to raise it again
    
    
    
    
    # SIMPLIFIED VERSION
    movies = pd.read_csv(f)
    return movies
        
