import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from pathlib import Path
from PIL import Image
import os
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings("ignore")


def make_wordcloud(df, brand):

    text = " ".join(t.lower() for t in df.description)

    print(f"There are {len(text.split())} words in {brand}'s description")

    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["short", "t", "shirt", "neck", "sleeve", "uniqlo"])

    # Create and generate a word cloud image:
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"wordcloud for {brand} data")
    plt.show()

    wordcloud.to_file(f"./EDA/title_EDA_{brand}.png")


def get_dims(file):
    """
    return dimensions for an RBG image
    """
    try:
        im = Image.open(file)
    except:
        print("cannot open file:", file)
        return 0, 0
    arr = np.array(im)
    try:
        h,w,d = arr.shape
    except:
        print("not three channel for:", file)
        h, w = arr.shape
    return h, w


def plot_image_distribution(dim_df, brand):
    sizes = dim_df.groupby(['height', 'width']).size().reset_index().rename(columns={0:'count'})
    try:
        sizes['h_w'] = sizes.apply(lambda row: str(row.height) + "X" + str(row.width), axis=1)
    except:
        print(brand)

    plt.figure(0)
    sizes.plot.scatter(x='width', y='height')
    plt.title('Image Sizes (pixels) | {}'.format(brand))
    plt.xlabel("width")
    plt.ylabel("height")
    plt.show()
    plt.savefig(f"./EDA/imageSizes_scatter_{brand}.png")

    plt.figure(1)
    sizes.plot.bar(x="h_w", y="count")
    plt.title('Image Sizes Counts (pixels) | {}'.format(brand))
    plt.xlabel("image sizes")
    plt.ylabel("count")
    for i, v in enumerate(list(sizes["count"])):
        plt.text(i, v + 3, str(v), color='blue', fontweight='bold')
    plt.savefig(f"./EDA/imageSizes_bar_{brand}.png")
    plt.show()


def plot_material_distribution(df, materials_columns, type):
    counts = []
    for material in materials_columns:
        counts.append(df[material].sum())
    fig = go.Figure(data=[go.Pie(labels=materials_columns, values = counts,
                                        title = f"T-shirts composition distribution - {type}")])
    fig.show()
    fig.write_image(f"./EDA/composition_distribution_{type}.png")


if __name__ == "__main__":

    df = pd.read_csv("./data/E-Weaver_data.csv", index_col = [0])

    brand_lst = list(df.brand.unique())
    for brand in brand_lst:
        # Create wordcloud for each indivicual brand
        tmp_df = df[df["brand"]==brand]
        make_wordcloud(tmp_df, brand)

        # Create visualization for images'size distribution
        if brand == "tentree":
            continue
        imagePath_lst = [os.path.join("data/image_data", f) for f in os.listdir("data/image_data/") if brand in f]
        dim_df = pd.DataFrame([get_dims(imagePath) for imagePath in imagePath_lst], columns = ["height", "width"])
        dim_df = dim_df[dim_df.height != 0]
        plot_image_distribution(dim_df, brand)

    # Create wordcloud for all data
    make_wordcloud(df, "all")

    # Create visualization for price column
    # plot_order1 = df["price"].groupby('price')['price'].sum().sort_values(ascending=True).index.values
    g = sns.catplot("price", data=df, kind='count', height=10, aspect=1.5)
    (g.set_axis_labels("Price", "Count").set_titles("All data price distribution").despine(left=True))  

    # Create visualization for all the composition materials
    df_men = df[df["gender"]=="men"]
    df_women = df[df["gender"]=="women"]
    columns = df.columns.tolist()
    composition_index = columns.index("composition")
    materials_columns = columns[composition_index+1:-1]
    plot_material_distribution(df, materials_columns, "all")
    # Create visualization for each gender's composition materials
    plot_material_distribution(df_men, materials_columns, "men")
    plot_material_distribution(df_women, materials_columns, "women")
    # Create visualization for each brand's composition materials
    for brand in brand_lst:
        tmp_df = df[df["brand"]==brand]
        plot_material_distribution(tmp_df, materials_columns, brand)

    # Create distribution of numbers of materials in a t-shirt
    # first get boolean value for all the numbers value in all materials sub-dataset, True for any number and False for 0
    df_boolean = df[materials_columns].select_dtypes(include=['number']) != 0
    count_lst = []
    for idx, row in df_boolean.iterrows():
        count = 0
        for material in materials_columns:
            if row[material] == True:
                count += 1 
        count_lst.append(count)
    count_dict = dict(Counter(count_lst))
    # rename the keys
    count_dict = dict((str(key)+" material(s)", value) for (key, value) in count_dict.items())
    # print(count_dict)

    fig = go.Figure(data=[go.Pie(labels=list(count_dict.keys()), values = list(count_dict.values()),
                                        title = f"material composition count")])
    fig.show()
    fig.write_image("./EDA/material_composition_count.png")





    
