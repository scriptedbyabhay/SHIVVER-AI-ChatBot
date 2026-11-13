from pathlib import Path
import pandas as pd

f = Path("dataset")/"horror_movies.csv"
movies = pd.read_csv(f)

print("\n---TOTAL RECORDS---")
print(movies.shape[0])

print("\n---TOTAL COLUMNS---")
print(len(movies.columns.tolist()))

totalHorrorMovies = movies["genre_names"].str.contains("Horror")
print("\n---TOTAL 'HORROR' MOVIES---")
print(totalHorrorMovies.sum())
# What is the difference between len() and .sum()? If len() is used, the total number of MOVIES is printed but if .sum() is used, the total number of HORROR MOVIES is printed

print("\n---DUPLICATE ROWS---")
print(movies.duplicated().sum())

print("\n---DUPLICATE IDs---")
print(movies["id"].duplicated().sum())

print("\n---MISSING VALUES & TOTAL MISSING PERCENTAGE---")
summary = pd.DataFrame({
    "Missing Count": movies.isna().sum(),
    "Missing %": (movies.isna().mean() * 100).round(2)
})
print(summary)