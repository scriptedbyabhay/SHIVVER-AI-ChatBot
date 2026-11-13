from modules.dataLoader import load_movies

def main():
    movies = load_movies()
    # if movies is not None:
    # Since we made changes to dataLoader.py, failures raise exceptions rather than returning None
    # Since dataLoader.py never returns 'None', the 'if movies is not None:' line is not necessary   
    print("\nTotal movies: ", len(movies))
    print(movies.head())
    print(movies.columns.tolist())

if __name__ == "__main__":
    main()