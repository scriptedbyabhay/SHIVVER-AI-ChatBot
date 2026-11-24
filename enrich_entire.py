import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


# 1. CONFIGURATION

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("Missing TMDB_API_KEY. Check your .env file.")

INPUT_PATH = Path("dataset") / "cleaned_movies.csv"
OUTPUT_PATH = Path("dataset") / "enriched_movies.csv"


CHECKPOINT_INTERVAL = 100
REQUEST_DELAY = 0.25
MAX_RETRIES = 5
BATCH_SIZE = 5000

URL = "https://api.themoviedb.org/3/movie/{}/credits"

session = requests.Session()


# 2. FETCH CREDITS FOR ONE MOVIE
def fetch_credits(movie_id):

    for attempt in range(MAX_RETRIES):

        try:
            response = session.get(
                URL.format(movie_id),
                params={"api_key": API_KEY},
                timeout=20
            )

            # Handle rate limiting
            if response.status_code == 429:
                wait_time = float(
                    response.headers.get("Retry-After", 2 ** attempt)
                )
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            # Movie does not exist in TMDB
            if response.status_code == 404:
                return "", "", "not_found"

            # Stop if authentication or another HTTP error occurs
            response.raise_for_status()

            data = response.json()

            # Extract first five cast members
            actors = [
                person.get("name")
                for person in data.get("cast", [])[:5]
                if person.get("name")
            ]

            # Extract all directors
            directors = list(dict.fromkeys(
                person.get("name")
                for person in data.get("crew", [])
                if person.get("job") == "Director"
                and person.get("name")
            ))

            return (
                "; ".join(directors),
                "; ".join(actors),
                "success"
            )

        except requests.exceptions.HTTPError as error:

            status_code = error.response.status_code

            if status_code in (401, 403):
                raise RuntimeError(
                    f"TMDB authentication/permission error: {error}"
                )

            if status_code < 500:
                print(f"Movie {movie_id}: HTTP error {status_code}")
                return "", "", "error"

        except requests.exceptions.RequestException as error:

            print(f"Movie {movie_id}: Network error: {error}")

        # Exponential backoff before retrying
        if attempt < MAX_RETRIES - 1:
            time.sleep(2 ** attempt)

    return "", "", "error"


# 3. LOAD DATASET AND PREPARE OUTPUT

movies = pd.read_csv(INPUT_PATH)

if OUTPUT_PATH.exists():

    enriched_movies = pd.read_csv(OUTPUT_PATH)

    if not enriched_movies["id"].equals(movies["id"]):
        raise ValueError(
            "Existing enriched dataset does not match the input dataset."
        )

    print("Existing progress found. Resuming enrichment.")

else:

    enriched_movies = movies.copy()

    enriched_movies["director"] = ""
    enriched_movies["top_5_cast"] = ""
    enriched_movies["credits_status"] = "pending"


# 4. PROCESS THE NEXT BATCH

total_movies = len(enriched_movies)

# Find movies that are still pending
pending_indices = enriched_movies.index[
    enriched_movies["credits_status"] == "pending"
][:BATCH_SIZE]

# If there is room in this batch, retry previously failed records
remaining_slots = BATCH_SIZE - len(pending_indices)

error_indices = enriched_movies.index[
    enriched_movies["credits_status"] == "error"
][:remaining_slots]

# Combine the records to process
batch_indices = list(pending_indices) + list(error_indices)

print("\n--- BATCH PROCESSING ---")
print("Total movies:", total_movies)
print("Movies in this batch:", len(batch_indices))

processed = 0

for index in batch_indices:

    row = enriched_movies.loc[index]
    movie_id = row["id"]

    director, cast, status = fetch_credits(movie_id)

    enriched_movies.at[index, "director"] = director
    enriched_movies.at[index, "top_5_cast"] = cast
    enriched_movies.at[index, "credits_status"] = status

    processed += 1

    print(
        f"Processed {processed}/{len(batch_indices)} | "
        f"Movie ID: {movie_id} | Status: {status}"
    )

    # Save progress every 100 movies
    if processed % CHECKPOINT_INTERVAL == 0:
        enriched_movies.to_csv(OUTPUT_PATH, index=False)
        print("Checkpoint saved!")

    time.sleep(REQUEST_DELAY)


# Save the completed batch
enriched_movies.to_csv(OUTPUT_PATH, index=False)

print("\n--- BATCH COMPLETED ---")
print("Movies processed in this session:", processed)

print("\n--- OVERALL PROGRESS ---")
print(
    "Successfully enriched:",
    (enriched_movies["credits_status"] == "success").sum()
)
print(
    "Not found:",
    (enriched_movies["credits_status"] == "not_found").sum()
)
print(
    "Pending:",
    (enriched_movies["credits_status"] == "pending").sum()
)
print(
    "Errors:",
    (enriched_movies["credits_status"] == "error").sum()
)

print("\nSaved to:", OUTPUT_PATH)

session.close()

# 5. FINAL SAVE

enriched_movies.to_csv(OUTPUT_PATH, index=False)

print("\n--- ENRICHMENT COMPLETED ---")
print("Total records:", total_movies)
print("Successfully enriched:",
      (enriched_movies["credits_status"] == "success").sum())
print("Not found:",
      (enriched_movies["credits_status"] == "not_found").sum())
print("Errors:",
      (enriched_movies["credits_status"] == "error").sum())

print("\nSaved to:", OUTPUT_PATH)

session.close()