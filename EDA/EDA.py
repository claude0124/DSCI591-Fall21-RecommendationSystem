# %%
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

    # plt.figure(0)
    sizes.plot.scatter(x='width', y='height')
    plt.title('Image Sizes (pixels) | {}'.format(brand))
    plt.xlabel("width")
    plt.ylabel("height")
    plt.savefig(f"./EDA/imageSizes_scatter_{brand}.png")
    plt.show()

    # plt.figure(1)

    sizes.plot.bar(x="h_w", y="count")
    plt.title('Image Sizes Counts (pixels) | {}'.format(brand))
    plt.xlabel("image sizes")
    plt.ylabel("count")
    for i, v in enumerate(list(sizes["count"])):
        plt.text(i, v + 3, str(v), color='blue', fontweight='bold')
    plt.xticks(rotation=45)
    plt.savefig(f"./EDA/imageSizes_bar_{brand}.png")
    plt.show()


def plot_material_distribution(df, materials_columns, type):
    counts = []
    for material in materials_columns:
        counts.append(df[material].sum())

    material_df = pd.DataFrame(np.array([counts]), columns=materials_columns)
    material_majority_dict ={}
    material_majority_dict["others"] = 0
    material_minority_dict = {}
    for material in materials_columns:
        percent = material_df[material][0]
        # Include every material that is less than 1% among all 
        if percent < int(material_df.sum(axis=1)*0.01):
            material_majority_dict['others'] += percent
            material_minority_dict[material] = percent
        else:
            material_majority_dict[material] = percent

    # Create two new dataframe that consist major and minor materials
    material_majority_df = pd.DataFrame(data=material_majority_dict, index=[0])
    material_minority_df = pd.DataFrame(data=material_minority_dict, index=[0])
    majority_columns = material_majority_df.columns.tolist()
    minority_columns = material_minority_df.columns.tolist()

    fig = go.Figure(data=[go.Pie(labels=majority_columns, values = list(material_majority_df.iloc[0]),
                                        title = f"T-shirts composition distribution - {type}: majority")])
    fig.update_layout(legend = dict(font = dict(family = "Courier", size = 20, color = "black")),
                    legend_title = dict(font = dict(family = "Courier", size = 20, color = "blue")),
                    title = dict(font=dict(size=20)))
    fig.write_image(f"./EDA/composition_distribution_{type}_majority.png")
    fig.show()

    fig = go.Figure(data=[go.Pie(labels=minority_columns, values = list(material_minority_df.iloc[0]),
                                        title = f"T-shirts composition distribution - {type}: below 1%")])
    fig.update_layout(legend = dict(font = dict(family = "Courier", size = 20, color = "black")),
                    legend_title = dict(font = dict(family = "Courier", size = 20, color = "blue")),
                    title = dict(font=dict(size=20)))
    fig.write_image(f"./EDA/composition_distribution_{type}_minority.png")
    fig.show()


if __name__ == "__main__":

    df = pd.read_csv("./data/E-Weaver_data.csv", index_col = [0])

    # Statistical description for datatypes 
    print(df.info())
    print("-"*50)
    print(df.dtypes)
    print("-"*50)
    print(df.describe().T)
    print("-"*50)

    # Checking the number of rows having null values
    print(df[df.columns[df.isnull().any()]].isnull().sum())
    print("-"*50)

    # How many unique colors in dataset
    print(len(df["color"].unique()))

    # Price columns' distribution in bar plot
    df['price'].value_counts().head(10).plot.bar()
    plt.title("Price counts in descending order")
    plt.xlabel("price($)")
    plt.ylabel("counts")
    plt.savefig(f"./EDA/price_histogram.png")
    plt.show()

    # Outlier analysis of price column
    price_df = df["price"]
    ax = sns.boxplot(data = price_df, palette = "Set2")
    plt.title("Outlier analysis of price attribute")
    plt.savefig(f"./EDA/price_outlier.png")
    plt.show()

    # Correlation analysis between numerical value attributes
    columns = df.columns.tolist()
    composition_index = columns.index("composition")
    materials_columns = columns[composition_index+1:-1]

    numerical_columns = materials_columns+["price"]
    numerical_df = df[numerical_columns]
    
    colormap = plt.cm.RdBu
    plt.figure(figsize=(15,15))
    plt.title("Pearson correlation of numerical features", y = 1.05, size = 15)
    sns.heatmap(numerical_df.astype(float).corr(), annot = True)
    plt.savefig(f"./EDA/numerical_feature_heatmap.png")
    plt.show()

    brand_lst = list(df.brand.unique())
    # for brand in brand_lst:
    #     # Create wordcloud for each indivicual brand
    #     tmp_df = df[df["brand"]==brand]
    #     make_wordcloud(tmp_df, brand)

    #     # Create visualization for images'size distribution
    #     if brand == "tentree":
    #         continue
    #     imagePath_lst = [os.path.join("data/image_data", f) for f in os.listdir("data/image_data/") if brand in f]
    #     dim_df = pd.DataFrame([get_dims(imagePath) for imagePath in imagePath_lst], columns = ["height", "width"])
    #     dim_df = dim_df[dim_df.height != 0]
    #     plot_image_distribution(dim_df, brand)

    # Create wordcloud for all data
    make_wordcloud(df, "all")

    # Create visualization for all images's size
    imagePath_lst = [os.path.join("data/image_data", f) for f in os.listdir("data/image_data/")]
    dim_df = pd.DataFrame([get_dims(imagePath) for imagePath in imagePath_lst], columns = ["height", "width"])
    
    # Get rid of image failed to download which only has 1 channel only
    dim_df = dim_df[dim_df.height != 0]
    plot_image_distribution(dim_df, "all")

    # Create visualization for price column
    # plot_order1 = df["price"].groupby('price')['price'].sum().sort_values(ascending=True).index.values
    g = sns.catplot("price", data=df, kind='count', height=10, aspect=1.5)
    (g.set_axis_labels("Price", "Count").set_titles("All data price distribution").despine(left=True))  

    # Create visualization for all the composition materials
    df_men = df[df["gender"]=="men"]
    df_women = df[df["gender"]=="women"]

    plot_material_distribution(df, materials_columns, "all")
    # Create visualization for each gender's composition materials
    # plot_material_distribution(df_men, materials_columns, "men")
    # plot_material_distribution(df_women, materials_columns, "women")
    # Create visualization for each brand's composition materials
    # for brand in brand_lst:
    #     tmp_df = df[df["brand"]==brand]
    #     plot_material_distribution(tmp_df, materials_columns, brand)


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





    

# %%
()