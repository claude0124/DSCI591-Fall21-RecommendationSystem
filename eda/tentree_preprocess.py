import pandas as pd
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/tentree.csv")

# NOTE: image_url might not be complete
# Select targeted attributes
df = df[["gender", "price", "materials", "color", "image_url", "description", "name"]]

# rename column names to match column names of HM
df = df.rename(columns = {"name": "title", "materials": "composition", "image_url": "imageUrl"})

# add brand column
df["brand"] = "tentree"

# rearrange columns order
new_columns_order = ["title", "description", "price", "color", "gender", "imageUrl", "brand", "composition"]
df = df[new_columns_order]

# extract each material out of composition column
materials_lst = []
for index, row in df.iterrows():
    # pattern found in Tentree's composition columns
    composition = row["composition"].replace("Recycled ", "").replace("TENCEL ", "").replace("Organic ", "").lower()
    matches = re.compile(r'(\d+[%])\s(\w+)').finditer(composition)
    for match in matches:
        materials_lst.append(match.group(2))

materials_lst = list(set(materials_lst))

print(materials_lst)

# create new columns based on materials list
for material in materials_lst:
    df[material] = ""

# adding value to each new material columns based on composition column value
for material in materials_lst:
    data = []
    for index, row in df.iterrows():
        composition = row["composition"].replace("Recycled ", "").replace("TENCEL ", "").replace("Organic ", "").lower()
        tmp = re.findall(r'(\d+)[%]\s({})'.format(material), composition)
        if len(tmp) == 0:
            data.append(0)
        else:
            data.append(int(tmp[0][0])/100)
    df[material] = data


# set title column as index
# df.set_index("title", inplace = True)

# modify gender column value
df['gender'] = df['gender'].map({"mens": "men", "womens": "women"})



print(df.columns)  # check all the column names
print(df.head())

# save the cleaned data as csv file
df.to_csv("./tentree_clean.csv")
