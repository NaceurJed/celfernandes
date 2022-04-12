#This .py constructs a KMeans clustering of this dataframe into N clusters

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def clustering_article(number_of_clusters)
    # Configuring the parameters of the clustering algorithm
    articles = pd.read_csv('../data/articles_feature_engineered.csv')

    #remove the index, as it would bias the clustering
    articles_no_id = articles.drop('article_id',1)

    # Define the clustering algorithm
    KMeans_cluster = KMeans(n_clusters=number_of_clusters)
    # Fitting the clustering algorithm
    KMeans_cluster.fit(articles_no_id)
    # Adding the results to a new column in the dataframe
    articles["cluster_KNN"] = KMeans_cluster.labels_

def articles_with_clusters():
    return articles[['article_id','cluster_KNN']]

def clusters