import pickle
import numpy as np
import os

BASE = os.path.dirname(__file__)

# LOAD MODELS
df = pickle.load(open(os.path.join(BASE, "models/df.pkl"), "rb"))
tfidf_matrix = pickle.load(open(os.path.join(BASE, "models/tfidf_matrix.pkl"), "rb"))
indices = pickle.load(open(os.path.join(BASE, "models/indices.pkl"), "rb"))

# normalize mapping
def build_map(idx):
    return {str(k).lower(): int(v) for k, v in idx.items()}

TITLE_MAP = build_map(indices)

def recommend(title, top_n=10):
    title = title.lower()

    if title not in TITLE_MAP:
        return []

    idx = TITLE_MAP[title]

    scores = (tfidf_matrix @ tfidf_matrix[idx].T).toarray().ravel()
    order = np.argsort(-scores)

    results = []
    for i in order:
        if i == idx:
            continue
        results.append({
            "title": df.iloc[i]["title"],
            "score": float(scores[i])
        })
        if len(results) >= top_n:
            break

    return results