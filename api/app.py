from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from scipy.spatial.distance import cdist
import numpy as np

app = Flask(__name__)
CORS(app, origins='*')
nlp = spacy.load("en_core_web_sm")

def dbscan(D, eps, MinPts):
    labels = [0] * len(D)
    C = 0
    for P in range(len(D)):
        if labels[P] != 0:
            continue
        NeighborPts = regionQuery(D, P, eps)
        if len(NeighborPts) < MinPts:
            labels[P] = -1  # Noise
        else:
            C += 1
            growCluster(D, labels, P, NeighborPts, C, eps, MinPts)
    return labels

def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    labels[P] = C
    i = 0
    while i < len(NeighborPts):
        Pn = NeighborPts[i]
        if labels[Pn] == -1:
            labels[Pn] = C
        elif labels[Pn] == 0:
            labels[Pn] = C
            PnNeighborPts = regionQuery(D, Pn, eps)
            if len(PnNeighborPts) >= MinPts:
                NeighborPts += PnNeighborPts
        i += 1

def regionQuery(D, P, eps):
    return [Pn for Pn in range(len(D)) if np.linalg.norm(D[P] - D[Pn]) < eps]

@app.route('/cluster', methods=['POST'])
def cluster():
    texts = request.get_json().get('texts', [])
    vectors = [nlp(text).vector for text in texts]
    vectors = np.array(vectors)  # Convertendo lista de vetores para NumPy array
    # Calcular a matriz de distância de cosseno
    distance_matrix = cdist(vectors, vectors, metric='cosine')
    # Garantir que não haja valores negativos na matriz de distância
    distance_matrix[distance_matrix < 0] = 0
    # Aplicar o DBSCAN Python puro para clustering com a matriz de distância
    labels = dbscan(distance_matrix, eps=0.5, min_samples=2)
    return jsonify(labels)

if __name__ == '__main__':
    app.run(port=5004)
