# TO CHECK ONE MOVIE
# import os
# import requests

# # Store your key as an environment variable rather than hardcoding it
# TMDB_API_KEY = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY")
# TEST_MOVIE_ID = 760161  # Orphan: First Kill


# def fetch_movie_credits(movie_id: int, api_key: str) -> dict:
#   url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
#   response = requests.get(url, params={"api_key": api_key}, timeout=10)
#   response.raise_for_status()
#   data = response.json()

#   # Extract top 5 billed cast members (sorted by billing order)
#   cast_sorted = sorted(data.get("cast", []), key=lambda x: x.get("order", 999))
#   top_cast = [person["name"] for person in cast_sorted[:5]]

#   # Extract director(s) from the crew list
#   directors = [
#       person["name"]
#       for person in data.get("crew", [])
#       if person.get("job") == "Director"
#   ]

#   return {
#       "id": movie_id,
#       "top_5_cast": ", ".join(top_cast),
#       "director": ", ".join(directors),
#       "total_cast_count": len(data.get("cast", [])),
#   }


# # Run the single-movie smoke test
# result = fetch_movie_credits(TEST_MOVIE_ID, TMDB_API_KEY)
# print(result)



# TO CHECK MULTIPLE MOVIES
# import os
# import time
# import pandas as pd
# import requests

# # Read API key from environment variable (with fallback to your key)
# API_KEY = os.getenv("TMDB_API_KEY", "6de85f1aaae91a9c605218bad8301028")

# # 1. Load your CSV and take just the first 20 rows to test
# df = pd.read_csv("dataset/cleaned_movies.csv")
# small_df = df.head(20).copy()

# # 2. Create empty lists to store our new data
# cast_list = []
# director_list = []

# # 3. Loop through each movie ID one by one
# for movie_id in small_df["id"]:
#   # FIXED: Added 'api.' subdomain and '/3/movie/' path before {movie_id}
#   url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

#   # IMPROVED: Passed api_key via params and added a 10-second timeout
#   response = requests.get(url, params={"api_key": API_KEY}, timeout=10)

#   # Check if the movie was found (status code 200 means success)
#   if response.status_code == 200:
#     data = response.json()

#     # Get the top 5 actors safely using .get()
#     actors = [person["name"] for person in data.get("cast", [])[:5]]
#     cast_list.append(", ".join(actors))

#     # Find the director(s) safely using .get()
#     directors = [
#         person["name"]
#         for person in data.get("crew", [])
#         if person.get("job") == "Director"
#     ]
#     director_list.append(", ".join(directors))
#   else:
#     # If the movie wasn't found, add blank text so our lists stay the right length
#     print(f"Warning: Movie ID {movie_id} returned status {response.status_code}")
#     cast_list.append("")
#     director_list.append("")

#   print(f"Finished movie ID: {movie_id}")
#   time.sleep(0.1)  # Pause slightly so we don't overwhelm the website

# # 4. Add the new lists as columns to your table
# small_df["top_5_cast"] = cast_list
# small_df["director"] = director_list

# # 5. Save the test result to a new CSV so you can open it in Excel
# small_df.to_csv("test_20_movies.csv", index=False)
# print("Done! Open 'test_20_movies.csv' to check your results.")

