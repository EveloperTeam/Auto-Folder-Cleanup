from timeit import repeat
import spacy
from nltk.cluster import KMeansClusterer
from sklearn.cluster import KMeans
import nltk
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def elbow(x): # x = emb
    wcss = []
    for i in range(2, 6):
        kmodel = KMeans(n_clusters=i, random_state=0)
        try:
            kmodel.fit(x)
        except:
            print("Value error")
            break
        wcss.append(kmodel.inertia_)
    
    min_wcss = 2147483647
    for j in wcss:
        if j < min_wcss: min_wcss = j
    
    return wcss.index(min_wcss) + 2


def clustering_question(data, NUM_ClUSTERS):
    # sentences = data['trans']
    X = np.array(data['emb'].tolist())
    # X = np.array(data)

    kclusterer = KMeansClusterer(
        NUM_ClUSTERS, distance = nltk.cluster.util.cosine_distance,
        repeats=25, avoid_empty_clusters=True
    )

    assigned_clusters = kclusterer.cluster(X, assign_clusters=True)

    data['cluster'] = pd.Series(assigned_clusters, index=data.index)
    # print(pd.Series.describe(data['cluster']))
    data['centeroid'] = data['cluster'].apply(lambda x: kclusterer.means()[x])

    return data, assigned_clusters


def distance_from_centeroid(row):
    return distance_matrix([row['emb']], [row['centeroid'].tolist()])[0][0]


# Compute centroid distance to the data
