import pandas as pd
import seaborn as sns


df = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/tentree.csv")

# NOTE: image_url might not be complete
# Select targeted attributes
df = df[["gender", "price", "materials", "color", "image_url", "description", "name"]]

# rename column names to match column names of HM
df = df.rename(columns = {"name": "title", "materials": "composition", "image_url": "imageUrl"})

# add brand column
df["brand"] = "tentree"


# set title column as index
df.set_index("title", inplace = True)

# modify gender column value
df['gender'] = df['gender'].map({"mens": "men", "womens": "women"})

print(df.columns)  # check all the column names
print(df.head())

# save the cleaned data as csv file
df.to_csv("./tentree_clean.csv")