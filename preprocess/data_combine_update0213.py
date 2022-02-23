#%%
import pandas as pd


# read in each csv file collected from websites
#@@ by 12-02-2021
df_zara = pd.read_csv(r"./data/zara_clean.csv", index_col=[0])
df_hm = pd.read_csv(r"./data/hm_clean.csv", index_col=[0])
df_uniqlo = pd.read_csv(r"./data/uniqlo_clean.csv", index_col=[0])
df_tentree = pd.read_csv(r"./data/tentree_clean.csv", index_col=[0])
df_thegoodtee = pd.read_csv(r"./data/thegoodtee_clean.csv", index_col=[0])
df_dedicated = pd.read_csv(r"./data/dedicated_clean.csv", index_col=[0])
df_outlanddenim = pd.read_csv(r"./data/outlanddenim_clean.csv", index_col=[0])
df_thestandardstitch = pd.read_csv(r"./data/thestandardstitch_clean.csv", index_col=[0])
df_fairIndigo = pd.read_csv(r"./data/fairindigo_clean.csv", index_col=[0])
df_zerum = pd.read_csv(r"./data/zerum_clean.csv", index_col=[0])
df_livingCraft = pd.read_csv(r"./data/livingCraft_clean.csv", index_col=[0])

#@@ by 02-13-2022
df_chnge = pd.read_csv(r"./data/chnge_tshirt_all_cleaned.csv", index_col=[0])
df_dorsu = pd.read_csv(r"./data/dorsu_tshirt_all_cleaned.csv", index_col=[0])
df_etiko = pd.read_csv(r"./data/etiko_tshirt_all_cleaned.csv", index_col=[0])
df_mate = pd.read_csv(r"./data/mate_tshirt_all_cleaned.csv", index_col=[0])
df_lyb = pd.read_csv(r"./data/LittleYellowBird_tshirt_all_cleaned.csv", index_col=[0])
df_rapanui = pd.read_csv(r"./data/Rapanui_tshirt_all_cleaned.csv", index_col=[0])
df_bws = pd.read_csv(r"./data/BrothersWeStand_tshirt_all_cleaned.csv", index_col=[0])
df_njeans = pd.read_csv(r"./data/NudieJeans_tshirt_all_cleaned.csv", index_col=[0])
df_kuyichi = pd.read_csv(r"./data/kuyichi_tshirt_all_cleaned.csv", index_col=[0])
df_bleed = pd.read_csv(r"./data/bleed_tshirt_all_cleaned.csv", index_col=[0])
df_aagnels = pd.read_csv(r"./data/armedangels_tshirt_all_cleaned.csv", index_col=[0])
df_classic = pd.read_csv(r"./data/theclassictshirt_tshirt_all_cleaned.csv", index_col=[0])

# @@ by 12-02-2021
print(f"\nzara dataframe contains these columns: {df_zara.columns}")
print(f"\nhm dataframe contains these columns: {df_hm.columns}")
print(f"\nuniqlo dataframe contains these columns: {df_uniqlo.columns}")
print(f"\ntentree dataframe contains these columns: {df_tentree.columns}")
print(f"\nthegoodtee dataframe contains these columns: {df_thegoodtee.columns}")
print(f"\ndedicated dataframe contains these columns: {df_dedicated.columns}")
print(f"\noutlanddenim dataframe contains these columns: {df_outlanddenim.columns}")
print(f"\nthestandardstitch dataframe contains these columns: {df_thestandardstitch.columns}")
print(f"\nfairIndigo dataframe contains these columns: {df_fairIndigo.columns}")
print(f"\nzerum dataframe contains these columns: {df_zerum.columns}")
print(f"\nlivingCraft dataframe contains these columns: {df_livingCraft.columns}")

#@@ by 02-13-2022
print(f"\nChnge dataframe contains these columns: {df_chnge.columns}")
print(f"\nDorsu dataframe contains these columns: {df_dorsu.columns}")
print(f"\nEtiko dataframe contains these columns: {df_etiko.columns}")
print(f"\nMate dataframe contains these columns: {df_mate.columns}")
print(f"\nLittleYellowBird dataframe contains these columns: {df_lyb.columns}")
print(f"\nRapanui dataframe contains these columns: {df_rapanui.columns}")
print(f"\nBrothersWeStand dataframe contains these columns: {df_bws.columns}")
print(f"\nNudieJeans dataframe contains these columns: {df_njeans.columns}")
print(f"\nKiyuchi dataframe contains these columns: {df_kuyichi.columns}")
print(f"\nBleed dataframe contains these columns: {df_bleed.columns}")
print(f"\nArmedAngels dataframe contains these columns: {df_aagnels.columns}")
print(f"\nTheClassicTshirts dataframe contains these columns: {df_classic.columns}")


# vertically stack them
df_lst = [df_zara, df_hm, df_uniqlo, df_tentree, df_thegoodtee, df_dedicated, df_outlanddenim, df_thestandardstitch, 
          df_fairIndigo, df_zerum, df_livingCraft, df_chnge, df_dorsu, df_etiko, df_mate, df_lyb, df_rapanui, df_bws,
          df_njeans, df_kuyichi, df_bleed, df_aagnels, df_classic]
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

# delete outlier in description which has 0 as value
df = df.loc[df["description"] != 0]

# remove duplicated imageUrl
print("Total duplicates are:", df.imageUrl.duplicated().sum())
df.drop_duplicates(subset=["imageUrl"], inplace=True)

# save combined dataframe to local
df.to_csv(r"./data/E-Weaver_data.csv")

# %%