
# ! pip install nltk

import nltk
nltk.download("popular")

## Install libraries
# ! python -m pip install --upgrade pip --quiet
# ! pip install spacy --quiet
# ! pip3 install spacy-transformers --quiet
# ! python -m spacy download en_core_web_sm --quiet

import spacy
#Load bert model
nlp = spacy.load("en_core_web_sm")

# Utility function for generating sentence embedding from the text
def get_embeddinngs(text):
    return nlp(text).vector

import pandas as pd
sen = ['A big ship is anchored near here', 'They are sailing on a ship', 'That is an old boat.', 'Are you ready for your big date?', 'Are you sure?',
       'Are your grandparents doing well?', 'How is your family', 'I live with my parents.', 'Can you take my photo.', 'Can\'t you open the door?']
data = pd.DataFrame(sen)
data.columns = ['text']
data

# Generating sentence embedding from the text
data['emb'] = data['text'].apply(get_embeddinngs)
data

"""# Clustering Sentences"""

from nltk.cluster import KMeansClusterer
import numpy as np

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
data

from scipy.spatial import distance_matrix
def distance_from_centroid(row):
    # type of emb and centroid is different, hence using tolist below
    return distance_matrix([row['emb']], [row['centroid'].tolist()])[0][0]

# Compute centroid distance to the data
data['distance_from_centroid'] = data.apply(distance_from_centroid, axis=1)

data