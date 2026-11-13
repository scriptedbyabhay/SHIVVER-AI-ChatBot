from pathlib import Path
import pandas as pd

filePath = Path("dataset")/"horror_movies.csv"
movies = pd.read_csv(filePath)

# READING THE EXCEL SHEET
# print("\n---DATASET DIMENSIONS---")
# print(movies.shape)

# print("\n---COLUMN NAMES---")
# print(movies.columns.tolist())

# print("\n---FIRST FIVE RECORDS---")
# print(movies.head())

# print("\n---DATASET INFO---")
# movies.info()




# NUMBER OF MISSING DATA ITEMS
# print(movies.isna().sum())




# What is the difference between shape[0] and len?
# print(movies.shape[0])
# print(len(movies))



# # MISSING PERCENTAGE
# datalist = movies.isna().sum()
# total = len(movies)

# # for colname, misscount in datalist.items():
# #     p = (misscount/total)*100
# #     print(f"{colname}: {p:.2f} % missing")
# # COMMENTED AS IT IS REDUNDANT; TAKE A LOOK AT THE LOGIC THOUGH

# tableForm = pd.DataFrame({
#     "Missing Count": datalist,
#     "Missing %": ((datalist/total)*100).round(2)
# })

# print(tableForm)

# summary = pd.DataFrame({
#     "Missing Count": movies.isna().sum(),
#     "Missing %": (movies.isna().mean() * 100).round(2)
# })

# # Optional: Sort from highest missing percentage to lowest
# summary = summary.sort_values(by="Missing %")

# print(summary)


# print(movies["genre_names"].value_counts().head(20))

# horror_movies = pd.DataFrame({
    
# })

# totalHorrorGenre = movies["genre_names"].str.contains("Horror")
# # print(totalHorrorGenre)

# # print(totalHorrorGenre.sum())


# horror_movies = movies[totalHorrorGenre]

# print("-----HORROR DATASET DIMENSIONS-----")
# print(horror_movies.shape)

# print("-----FIRST FIVE RECORDS-----")
# print(horror_movies.head())


# RESOLVING DUPLICATES
# print(movies.duplicated().sum())
print(movies["id"].duplicated().sum())



# After FUNCTION COMPOSITION, the dataset "horror_movies.csv" is to be cleaned
# The 'clean_dataset' and 'validate_dataset' functions are used from the 'dataCleaner.py' file located in the 'modules' folder
from modules.dataCleaner import clean_dataset, validate_dataset

# cleaned = clean_dataset(movies)
# validate_dataset(cleaned)

# output_Path = Path("dataset")/"cleaned_movies.csv"

# cleaned.to_csv(output_Path, index=False)
# print("\nCleaned dataset saved successfully!")
 

# # BEFORE & AFTER CLEANING MISSING VALUES
# print("Original missing overviews: ", movies["overview"].isna().sum())
# print("Cleaned missing overviews: ", cleaned["overview"].isna().sum())

# print("Original missing tagline: ", movies["tagline"].isna().sum())
# print("Cleaned missing tagline: ", cleaned["tagline"].isna().sum())

# print("Missing posters: ", cleaned["poster_path"].isna().sum())




# # STANDARDIZING TEXT
# standardized_movies = standardize_text(cleaned)
# print(standardized_movies[["title", "original_title", "original_language", "genre_names"]].head())



# # EXTRACTING DATE & YEAR
# date_processed_movies = process_date(standardized_movies)
# print(date_processed_movies[
#     ["title", "release_date", "release_year"]
# ].head())

# print("\n---RELEASE YEAR DATA TYPE---")
# print(date_processed_movies["release_year"].dtype)

# print("\n---INVALID OR MISSING DATES---")
# print(date_processed_movies["release_date"].isna().sum())

