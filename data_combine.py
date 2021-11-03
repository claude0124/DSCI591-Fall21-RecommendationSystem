import pandas as pd
import seaborn as sns

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
print(df.head())

#plot_order1 = df["price"].groupby('price')['price'].sum().sort_values(ascending=True).index.values
g = sns.catplot("price", data=df, kind='count', height=10, aspect=1.5)
(g.set_axis_labels("Price", "Count")
  .set_titles("All data price distribution")
#   .set(ylim=(0, 1))
  .despine(left=True))  

# save combined dataframe to local
df.to_csv("E-Weaver_data.csv")