import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go

# read in each csv file collected from websites
df_zara = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/zara_clean.csv", index_col = "title")
df_hm = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/hm_clean.csv", index_col = "title")
df_uniqlo = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/uniqlo_clean.csv", index_col = "title")
df_tentree = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/tentree_clean.csv", index_col = "title")
df_thegoodtee = pd.read_csv(r"/Users/Claude/Desktop/GraduateStudy/Fall21/DSCI591/web_scrapping/thegoodtee_clean.csv", index_col = "title")

# make sure all the dataframe only contains these attributes: brand, color, composition, description, imageUrl, title, price, gender 
print(f"\nzara dataframe contains these columns: {df_zara.columns}")
print(f"\nhm dataframe contains these columns: {df_hm.columns}")
print(f"\nuniqlo dataframe contains these columns: {df_uniqlo.columns}")
print(f"\ntentree dataframe contains these columns: {df_tentree.columns}")
print(f"\nthegoodtee dataframe contains these columns: {df_thegoodtee.columns}")

# vertically stack them
df_lst = [df_zara, df_hm, df_uniqlo, df_tentree, df_thegoodtee]
df = pd.concat(df_lst)

# Replace all empty elements with 0s
df.fillna(0, inplace=True)

# create a column: Sum, which do the sanity check of sum up all different composition percentages
columns = df.columns.tolist()
composition_index = columns.index("composition")
materials_columns = columns[composition_index+1:]
print(materials_columns)

sum_lst = []
for idx, row in df.iterrows():
  sum = 0
  for material in materials_columns:
    sum += row[material]
  sum_lst.append(sum)
df["sum"] = sum_lst

# delete outlier rows which materials sum is not euqal to 100%
# print(df.shape)
df = df.loc[df["sum"] == 1]
# print(df.shape)

#plot_order1 = df["price"].groupby('price')['price'].sum().sort_values(ascending=True).index.values
g = sns.catplot("price", data=df, kind='count', height=10, aspect=1.5)
(g.set_axis_labels("Price", "Count")
  .set_titles("All data price distribution")
#   .set(ylim=(0, 1))
  .despine(left=True))  

# plot pie chart for all the materials
def plot_material_distribution(df, materials_columns, type):
  counts = []
  for material in materials_columns:
    counts.append(df[material].sum())
  fig = go.Figure(data=[go.Pie(labels=materials_columns, values = counts,
                                      title = f"T-shirts composition distribution - {type}")])
  fig.show()

# plot distribution of single material and multi-materials
df_men = df[df["gender"]=="men"]
df_women = df[df["gender"]=="women"]
plot_material_distribution(df, materials_columns, "all")
plot_material_distribution(df_men, materials_columns, "men")
plot_material_distribution(df_women, materials_columns, "women")



# save combined dataframe to local
df.to_csv("E-Weaver_data.csv")
