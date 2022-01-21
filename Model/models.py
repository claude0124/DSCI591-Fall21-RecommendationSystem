# import libraries
from numpy import integer, unique, where, argmax
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt

from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder



def categorical_encoding(df, col_name):
    """
    This function converts categorical data in 
    dataframe to numerical values to fit in ML models
    """
    # Preprocess categorical columns
    col_np = df[[col_name]].to_numpy().ravel()

    # Integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(col_np)

    # Binary encode
    one_hot_encoder = OneHotEncoder(sparse = False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    one_hot_encoded = one_hot_encoder.fit_transform(integer_encoded)

    # print(one_hot_encoded.shape)

    return one_hot_encoded


def gen_features(df):
    """
    This function generate features from E-Weaver_data.csv's selected columns.
    Columns include: color, gender, brand, price, and each materials columns.
    """
    # Convert categorical features into numerical values
    for col_name in ['color', 'gender', 'brand']:
        if 'features' not in locals():
            features = categorical_encoding(df, col_name)
        else:
            tmp = categorical_encoding(df, col_name)
            features = np.concatenate((features, tmp),axis=1) 

    # Get the column names for each materials
    columns = df.columns.tolist()
    composition_index = columns.index("composition")
    materials_columns = columns[composition_index+1:-1]

    # Convert material-dataframe to numpy array
    materials_np = df[materials_columns].to_numpy()
    price_np = df[['price']].to_numpy()

    # Add the rest of numerical features of 'price' and each individual materials
    features = np.concatenate((features, price_np), axis=1)
    features = np.concatenate((features, materials_np), axis=1)

    # Save the features as csv file
    np.savetxt('./data/features.csv', features, delimiter=',')

    return features



if __name__ == "__main__":

    # Load dataset
    df = pd.read_csv("./data/E-Weaver_data.csv", index_col = [0])

    # Loading features 
    features = gen_features(df)

    print(features)
    #NOTE: use only one of the scaler method below
    # # Rescale data - useful for algorithms that use distance measures like K-Nearest Neighbors.
    # scaler = MinMaxScaler(feature_range=(0,1))
    # X_MinMaxScaled = scaler.fit_transform(X)

    # # Standardize Data
    # scaler = StandardScaler().fit(features)
    # X_standardized = scaler.transform(features)

    # # Normalize Data - useful for sparse datasets (a lot of zeroes)
    # scaler = Normalizer().fit(X)
    # X_normalized = scaler.transform(X)

    # # Summarize transformed data
    # np.set_printoptions(precision=3)
    # print(X_normalized[:5, :])

    #NOTE: tryout different clustering ml models (interested: K-nearest neighboring models)
    # Define the model
    # model = KNeighborsClassifier(n_neighbors=5, metric = 'minkowski', p = 2)

    # # Fit the model
    # model.fit(X_train, y_train)

    # # Assign a cluster to each example
    # yhat = model.prediction(X)

    # # Retrieve unique clusters
    # clusters = unique(yhat)

    #NOTE: try visualize our result, the below code might not work, use as reference
    # Create scatter plot for each example from each cluster
    # for cluster in clusters:
        # Get each example index for this cluster
    #     row_index = where(yhat == cluster)
    #     # Create scatter plot of these samples after performing PCA
    #     plt.scatter(X[row_index, 0], X[row_index, 1])
    # plt.show()