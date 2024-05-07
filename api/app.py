from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import numpy as np

app = Flask(__name__)
CORS(app, origins='*')
nlp = spacy.load("en_core_web_sm")

def k_means(data, k):
    centroids = data[np.random.choice(range(len(data)), k, replace=False)]
    while True:
        clusters = [[] for _ in range(k)]
        for datapoint in data:
            distances = [np.linalg.norm(datapoint - centroid) for centroid in centroids]
            closest_centroid = np.argmin(distances)
            clusters[closest_centroid].append(datapoint)
        new_centroids = np.array([np.mean(cluster, axis=0) for cluster in clusters if cluster])  # adiciona verificação se cluster não está vazio
        if np.array_equal(centroids, new_centroids):
            break
        centroids = new_centroids
    return centroids, clusters

@app.route('/cluster', methods=['POST'])
def cluster():
    try:
        texts = request.get_json().get('texts', [])
        k = request.get_json().get('k', 3)  # Default k to 3 if not provided
        if not texts:
            return jsonify({"error": "Lista de textos vazia."}), 400
        if k <= 0:
            return jsonify({"error": "O valor de k deve ser maior que zero."}), 400
        
        vectors = [nlp(text).vector for text in texts]
        if len(vectors) < k:
            return jsonify({"error": "Número insuficiente de textos para o número de clusters solicitados."}), 400
        
        vectors = np.array(vectors)
        centroids, clusters = k_means(vectors, k)
        clusters_response = {}
        for index, cluster in enumerate(clusters):
            clusters_response[f"Cluster {index+1}"] = [texts[i] for i in range(len(texts)) if vectors[i] in cluster]
        return jsonify(clusters_response)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5004)
