import pandas as pd
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(r"./data/zerum_tshirt_all_cleaned.csv")
print(df.columns)
df = df.drop(columns=["SN","cut","price_euro"])
df = df.rename(columns = {"material": "description", "price_usd": "price"})
print(df.columns)

# save the cleaned data as csv file
df.to_csv(r"./data/zerum_clean.csv")