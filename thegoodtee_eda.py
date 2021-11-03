import pandas as pd
import seaborn as sns


df = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/thegoodtee2.csv")

# NOTE: materials and gender info are missing
# Select targeted attributes
df = df[[ "price", "color_name", "image_url", "description", "item_name", "sex", "material"]]

# rename column names to match column names of HM
df = df.rename(columns = {"item_name": "title", "image_url": "imageUrl", "color_name": "color", "sex": "gender", "material": "composition"})

# add brand column
df["brand"] = "thegoodtee"

# clean color column
# TODO: clean row if color value is only integer
def extract_color(x):
  x = x.strip()
  if "-" in x:
    x = x.replace("-", " ")
  return x
df["color"] = df["color"].apply(extract_color)
print(df["color"].head())
print("-"*90)

# modify gender column value
df['gender'] = df['gender'].map({"mens": "men", "womens": "women"})

# set title column as index
df.set_index("title", inplace = True)
print(df.columns)  # check all the column names
print(df.head())

# save the cleaned data as csv file
df.to_csv("./thegoodtee_clean.csv")