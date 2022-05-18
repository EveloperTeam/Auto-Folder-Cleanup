import nltk
import ssl
import spacy
import pandas as pd
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

    data = pd.read_csv("data.csv")
    sen = data['trans'].values.tolist()  # data.csv의 [3]번째 열을 리스트로 변환
    df = pd.DataFrame(sen)
    df.columns = ['trans']

    # Generating sentence embedding from the text
    df['emb'] = df['trans'].apply(get_embeddings)
    emb_list = df['emb'].values.tolist()
    data['emb'] = emb_list
    data.to_csv("data.csv", index=False)

    return df