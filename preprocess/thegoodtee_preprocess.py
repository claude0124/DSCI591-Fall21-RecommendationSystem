import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(r"./data/thegoodtee2.csv")

# NOTE: materials and gender info are missing
# Select targeted attributes
df = df[[ "price", "color_name", "image_url", "description", "item_name", "sex", "material"]]

# rename column names to match column names of HM
df = df.rename(columns = {"item_name": "title", "image_url": "imageUrl", "color_name": "color", "sex": "gender", "material": "composition"})

# add brand column
df["brand"] = "thegoodtee"

# rearrange columns order
new_columns_order = ["title", "description", "price", "color", "gender", "imageUrl", "brand", "composition"]
df = df[new_columns_order]

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
df['gender'] = df['gender'].map({"mens": "men", "womens": "women", "unisex":"unisex"})

# create a new column of cotton with same value of 100% that reflects composition column
df['cotton'] = 1
df["composition"] = r"100% Cotton"

# set title column as index
# df.set_index("title", inplace = True)


print(df.columns)  # check all the column names
print(df.head())

# save the cleaned data as csv file
df.to_csv(r"./data/thegoodtee_clean.csv")
