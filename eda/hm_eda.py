#%%
import pandas as pd
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")


# Load previously collected data in pandas dataframe
df = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/hm.csv", index_col = "title")
print("-"*90)

# Select targeted attributes
df = df[["gender", "price", "composition", "color", "imageUrl", "description"]]

# Clean price column
def delete_unit(x):
    x = x.replace("$", "")
    return(float(x))

# clean color column
# TODO: clean row if color value is only integer
def extract_color(x):
  if "/" in x:
    x = x.replace("/", " ")
  return x
df["color"] = df["color"].apply(extract_color)
print(df["color"].head())
print("-"*90)

df["price"] = df["price"].apply(delete_unit)
print("after cleaning price column:\n")
print(df["price"].head())
print("-"*90)

# Add new column of 'brand'
df["brand"] = "H&M"

# rearrange columns order
new_columns_order = ["description", "price", "color", "gender", "imageUrl", "brand", "composition"]
df = df[new_columns_order]

# extract each material out of composition column
materials_lst = []
for index, row in df.iterrows():
    composition = row["composition"].lower()
    matches = re.compile(r'(\w+)\s(\d+[%])').finditer(composition)
    for match in matches:
        materials_lst.append(match.group(1))

materials_lst = list(set(materials_lst))
print(materials_lst)
print("-"*90)

# create new columns based on materials list
for material in materials_lst:
    df[material] = ""

# adding value to each new material columns based on composition column value
for material in materials_lst:
    data = []
    for index, row in df.iterrows():
        composition = row["composition"].lower()
        tmp = re.findall(r'({})\s(\d+)[%]'.format(material), composition)
        if len(tmp) == 0:
            data.append(0)
        else:
            data.append(int(tmp[0][1])/100)
    df[material] = data

# Get statistic summary about price column
print("statistic summary about 'price' column:\n")
print(df["price"].describe())
print("-"*90)

# Show head of cleaned dataframe
print("Data cleaned!\n")
print(df.head())
print(df.columns)  # check all the column names
print("-"*90)

# EDA of cleaned data
#plot_order1 = df["price"].groupby('price')['price'].sum().sort_values(ascending=True).index.values
g = sns.catplot("price", data=df, kind='count', height=10, aspect=1.5)
(g.set_axis_labels("Price", "Count")
  .set_titles("H&M Price distribution")
#   .set(ylim=(0, 1))
  .despine(left=True))  
print("-"*90)
# %%



# save it in the current working directory
output_name = "hm_clean.csv"
df.to_csv(f"./{output_name}")
print(f"dataframe saved as {output_name} in the current path")
print("Done\n")
# %%
