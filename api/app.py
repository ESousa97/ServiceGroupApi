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
        new_centroids = np.array([np.mean(cluster, axis=0) for cluster in clusters if cluster])
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    return centroids, clusters

@app.route('/cluster', methods=['POST'])
def cluster():
    if not request.json or not isinstance(request.json, dict):
        return jsonify({"error": "Invalid JSON format"}), 400

    texts = request.json.get('texts', [])
    k = request.json.get('k', 3)

    if not texts or not isinstance(texts, list) or not all(isinstance(text, str) for text in texts):
        return jsonify({"error": "Invalid 'texts' format or empty list"}), 400

    if k <= 0 or not isinstance(k, int):
        return jsonify({"error": "Invalid 'k' value, it must be an integer greater than zero"}), 400

    try:
        vectors = [nlp(text).vector for text in texts]
        if len(vectors) < k:
            return jsonify({"error": "Insufficient number of texts for the requested number of clusters"}), 400
        
        vectors = np.array(vectors)
        centroids, clusters = k_means(vectors, k)
        clusters_response = {f"Cluster {index+1}": [texts[i] for i in cluster] for index, cluster in enumerate(clusters)}
        return jsonify(clusters_response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5004)
