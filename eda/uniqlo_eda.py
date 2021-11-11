import pandas as pd
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/tshirt_info_all_uniqlo.csv")

# Select targeted attributes
df = df[["group", "price", "materials", "color", "thumb_link", "details", "name"]]

# rename column names to match column names of HM
df = df.rename(columns = {"name": "title", "group": "gender", "materials": "composition", "thumb_link": "imageUrl", "details": "description"})

# add brand column
df["brand"] = "uniqlo"

# set title column as index
df.set_index("title", inplace = True)

# clean price column
def delete_USD(x):
    x = x.replace("$", "")
    return(float(x))
df["price"] = df["price"].apply(delete_USD)

# rearrange columns order
new_columns_order = ["description", "price", "color", "gender", "imageUrl", "brand", "composition"]
df = df[new_columns_order]

# extract each material out of composition column
materials_lst = []
for index, row in df.iterrows():
    composition = row["composition"].split("/")[0].replace("Body: ", "").lower()
    matches = re.compile(r'(\d+[%])\s(\w+)').finditer(composition)
    for match in matches:
        materials_lst.append(match.group(2))

materials_lst = list(set(materials_lst))
materials_lst.remove("uses")
# there is only one outlier of 'Uses' material
print(materials_lst)

# create new columns based on materials list
for material in materials_lst:
    df[material] = ""

# adding value to each new material columns based on composition column value
for material in materials_lst:
    data = []
    for index, row in df.iterrows():
        composition = row["composition"].split("/")[0].replace("Body: ", "").lower()
        tmp = re.findall(r'(\d+)[%]\s({})'.format(material), composition)
        if len(tmp) == 0:
            data.append(0)
        else:
            data.append(int(tmp[0][0])/100)
    df[material] = data
        
# print(df.columns)  # check all the column names
print(df.head())


# save the cleaned data as csv file
df.to_csv("./uniqlo_clean.csv")