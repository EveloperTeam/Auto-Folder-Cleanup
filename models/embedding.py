import nltk
import spacy
import pandas as pd
from nltk.cluster import KMeansClusterer
import numpy as np
from scipy.spatial import distance_matrix
import csv

#Load bert model


# Utility function for generating sentence embedding from the text
def get_embeddinngs(text):
    return nlp(text).vector

def embedding():
    nltk.download("popular")
    nlp = spacy.load("en_core_web_sm")

    csv_file = open("./data.csv", "r", encoding='ms932', errors="")
    sen = ['A big ship is anchored near here', 'They are sailing on a ship', 'That is an old boat.', 'Are you ready for your big date?', 'Are you sure?',
        'Are your grandparents doing well?', 'How is your family', 'I live with my parents.', 'Can you take my photo.', 'Can\'t you open the door?']
    data = pd.DataFrame(sen)
    data.columns = ['text']
    data

    # Generating sentence embedding from the text
    data['emb'] = data['text'].apply(get_embeddinngs)
    data

"""# Clustering Sentences"""


def clustering_question(data,NUM_CLUSTERS = 15):

    sentences = data['text']

    X = np.array(data['emb'].tolist())

    kclusterer = KMeansClusterer(
        NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance,
        repeats=25,avoid_empty_clusters=True)

    assigned_clusters = kclusterer.cluster(X, assign_clusters=True)

    data['cluster'] = pd.Series(assigned_clusters, index=data.index)
    data['centroid'] = data['cluster'].apply(lambda x: kclusterer.means()[x])

    return data, assigned_clusters

data, ac = clustering_question(data, 3)
# data

def distance_from_centroid(row):
    # type of emb and centroid is different, hence using tolist below
    return distance_matrix([row['emb']], [row['centroid'].tolist()])[0][0]

# Compute centroid distance to the data
data['distance_from_centroid'] = data.apply(distance_from_centroid, axis=1)

# data