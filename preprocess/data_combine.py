#%%
import pandas as pd


# read in each csv file collected from websites
df_zara = pd.read_csv(r"./data/zara_clean.csv", index_col=[0])
df_hm = pd.read_csv(r"./data/hm_clean.csv", index_col=[0])
df_uniqlo = pd.read_csv(r"./data/uniqlo_clean.csv", index_col=[0])
df_tentree = pd.read_csv(r"./data/tentree_clean.csv", index_col=[0])
df_thegoodtee = pd.read_csv(r"./data/thegoodtee_clean.csv", index_col=[0])

# make sure all the dataframe only contains these attributes: brand, color, composition, description, imageUrl, title, price, gender 
print(f"\nzara dataframe contains these columns: {df_zara.columns}")
print(f"\nhm dataframe contains these columns: {df_hm.columns}")
print(f"\nuniqlo dataframe contains these columns: {df_uniqlo.columns}")
print(f"\ntentree dataframe contains these columns: {df_tentree.columns}")
print(f"\nthegoodtee dataframe contains these columns: {df_thegoodtee.columns}")

# vertically stack them
df_lst = [df_zara, df_hm, df_uniqlo, df_tentree, df_thegoodtee]
df = pd.concat(df_lst, ignore_index = True)

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

# save combined dataframe to local
df.to_csv(r"./data/E-Weaver_data.csv")

# %%
