import numpy as np
from PIL import Image
import requests
import pandas as pd
import os
from tqdm import tqdm

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)"
}

data_path = r"./data/image_data"
if not os.path.isdir(data_path):
    os.makedirs(data_path)

df = pd.read_csv(r"./data/E-Weaver_data.csv", index_col=[0])

# A list of image urls for checking duplicates
img_url_lst = []

n = df.shape[0]
with tqdm(total = n) as pbar:
    for idx, row in df.iterrows():
        pbar.update(1)
       
        brand = row["brand"]
        img_url = row["imageUrl"]
        id = row["id"]
        color = row["color"]
        # To prevent the dupliate image urld
        if img_url in img_url_lst:
            continue
        else:
            img_url_lst.append(img_url)
            if img_url.startswith("//"):
                img_url = "http://" + img_url.replace("//", "", 1)

            response = requests.get(img_url, headers = headers)

            # file_name = str(idx) + "_" + color + "_" + brand + ".png"
            file_name = str(id) + ".png"
            try:
                with open(os.path.join(data_path, file_name), "wb") as f:
                    f.write(response.content)

            except: 
                print("There is FileNotFoundError for:", file_name, brand)