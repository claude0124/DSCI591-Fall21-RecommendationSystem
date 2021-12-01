import pandas as pd
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv(r"./data/livingcraft_tshirt_all_cleaned.csv")
print(df.columns)
df = df.drop(columns=["SN","review","rating","price_euro","color"])
df = df.rename(columns = {"basic_color": "color", "price_usd": "price"})
print(df.columns)

# save the cleaned data as csv file
df.to_csv(r"./data/livingcraft_clean.csv")