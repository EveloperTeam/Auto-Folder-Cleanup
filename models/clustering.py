from timeit import repeat
import spacy
from nltk.cluster import KMeansClusterer
import nltk
import numpy as np
import pandas as pd


def clustering_question(data, NUM_ClUSTERS):
    sentences = data['text']
    X = np.array(data['emb'].tolist())

    kclusterer = KMeansClusterer(
        NUM_ClUSTERS, distance = nltk.cluster.util.cosine_distance,
        repeats=25, avoid_empty_clusters=True
    )

    assigned_clusters = kclusterer.cluster(X, assign_clusters=True)

    data['cluster'] = pd.Series(assigned_clusters, index=data.index)
    data['centeroid'] = data['cluster'].apply(lambda x: kclusterer.means()[x])

    return data, assigned_clusters

def distance_from_centeroid(row):
    return distance_matrix([row['emb']], [row['centeroid'].tolist()])[0][0]



nlp = spacy.load("en_core_web_trf")

