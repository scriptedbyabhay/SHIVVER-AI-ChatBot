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