#%%
import pandas as pd
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(r"./data/zara.csv", index_col = "title")

# Select targeted attributes
df = df[["gender", "price", "composition", "color", "imageUrl", "description"]]

# clean price column
def delete_USD(x):
    x = x.replace("USD", "")
    return(float(x))
df["price"] = df["price"].apply(delete_USD)
print(df["price"].head())
print("-"*90)

# clean color column
# TODO: clean row if color value is only integer
def extract_color(x):
  x = x.split("|")[0]
  if "Color" in x:
    x = x.replace("Color", "")
  if "/" in x:
    x = x.replace("/ ", "")
  return x
df["color"] = df["color"].apply(extract_color)
print(df["color"].head())
print("-"*90)

# Add new column of 'brand'
df["brand"] = "Zara"

# rearrange columns order
new_columns_order = ["description", "price", "color", "gender", "imageUrl", "brand", "composition"]
df = df[new_columns_order]

# clean composition column
def extract_composition(x):
    material = [i for i in x.split(",") if "%" in i and ":" not in i][0]
    return material
df["composition"] = df["composition"].apply(extract_composition)

# extract each material out of composition column
materials_lst = []
for index, row in df.iterrows():
    composition = row["composition"].lower()
    matches = re.compile(r'(\d+[%])\s(\w+)').finditer(composition)
    for match in matches:
        materials_lst.append(match.group(2))

materials_lst = list(set(materials_lst))
materials_lst.remove("of")  # there is only one outlier of 'of' material

print(materials_lst)

# create new columns based on materials list
for material in materials_lst:
    df[material] = ""

# adding value to each new material columns based on composition column value
for material in materials_lst:
    data = []
    for index, row in df.iterrows():
        composition = row["composition"].lower()
        tmp = re.findall(r'(\d+)[%]\s({})'.format(material), composition)
        if len(tmp) == 0:
            data.append(0)
        else:
            data.append(int(tmp[0][0])/100)
    df[material] = data
print("-"*90)

# drop rows with no title info
df = df.reset_index()
df = df.dropna(subset=['title'])
# df = df.set_index("title")

# get statistic summary about price column
print(df["price"].describe())

print(df.head())
print("\nData cleaned!")

print("\n###### EDA ######")
#plot_order1 = df["price"].groupby('price')['price'].sum().sort_values(ascending=True).index.values
g = sns.catplot("price", data=df, kind='count', height=10, aspect=1.5)
(g.set_axis_labels("Price", "Count")
  .set_titles("Zara Price distribution")
#   .set(ylim=(0, 1))
  .despine(left=True))  


# save it in the current working directory
output_name = r"./data/zara_clean.csv"
df.to_csv(f"./{output_name}")
print(f"dataframe saved as {output_name} in the current path")
print("Done\n")

# %%
