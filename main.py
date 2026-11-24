from modules.dataLoader import load_movies
from modules.searchandfind import search_by_title

def main():
    movies = load_movies()
    # if movies is not None:
    # Since we made changes to dataLoader.py, failures raise exceptions rather than returning None
    # Since dataLoader.py never returns 'None', the 'if movies is not None:' line is not necessary
    
    
    query = input("Enter a movie title: ")
    results = search_by_title(movies, query)
    
    if results.empty:
        print("No matching movies found!")
        
    else:
        print(results[["id", "title", "release_year"]].head(20))   
    print("\nTotal movies: ", len(movies))
    print(movies.head())
    print(movies.columns.tolist())

if __name__ == "__main__":
    main()