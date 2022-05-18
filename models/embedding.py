import nltk
import ssl
import spacy
import pandas as pd
from nltk.cluster import KMeansClusterer
import numpy as np
from scipy.spatial import distance_matrix
# import csv
#Load bert model


# Utility function for generating sentence embedding from the text
def get_embeddings(text):
    return nlp(text).vector

def embedding():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download("popular")

    global nlp
    nlp = spacy.load("en_core_web_sm")

    # csv_file = open("./data.csv", "r", encoding='ms932', errors="")
    data = pd.read_csv("data.csv")
    print("data_file -->\n", data)
    # sen = data['trans'].values.tolist()  # data.csv의 [3]번째 열을 리스트로 변환
    # print("sen: ", sen)
    # data['embed'] = sen
    # sen = ['A big ship is anchored near here', 'They are sailing on a ship', 'That is an old boat.', 'Are you ready for your big date?', 'Are you sure?',
    #     'Are your grandparents doing well?', 'How is your family', 'I live with my parents.', 'Can you take my photo.', 'Can\'t you open the door?']
    # data = pd.DataFrame(sen)
    # data.columns = ['text']

    # Generating sentence embedding from the text
    data['emb'] = data['trans'].apply(get_embeddings)
    # data['emb'] = get_embeddinngs(data['trans']).to_string()
    print("here==>\n", data)
    # data.to_csv("data.csv", index=False)

    # data, ac = clustering_question(data, 3)

    # Compute centroid distance to the data
    # data['distance_from_centroid'] = data.apply(distance_from_centroid, axis=1)


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


def distance_from_centroid(row):
    # type of emb and centroid is different, hence using tolist below
    return distance_matrix([row['emb']], [row['centroid'].tolist()])[0][0]