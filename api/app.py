from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import spacy

app = Flask(__name__)
CORS(app, origins='*')
nlp = spacy.load("en_core_web_sm")

def cosine_similarity(vectors):
    """Calcula a matriz de similaridade de cosseno entre os vetores."""
    norms = np.linalg.norm(vectors, axis=1)
    return np.dot(vectors, vectors.T) / np.outer(norms, norms)

def simple_dbscan(vectors, eps=0.5, min_samples=2):
    n = len(vectors)
    visited = set()
    clusters = []
    noise = set()
    
    def region_query(p):
        return [i for i in range(n) if 1 - distance_matrix[p][i] <= eps]
    
    def expand_cluster(p, neighbors):
        cluster = [p]
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                local_neighbors = region_query(neighbor)
                if len(local_neighbors) >= min_samples:
                    neighbors.extend(local_neighbors)
                if not any(neighbor in cl for cl in clusters):
                    cluster.append(neighbor)
        return cluster

    distance_matrix = 1 - cosine_similarity(vectors)
    distance_matrix[distance_matrix < 0] = 0
    
    for i in range(n):
        if i not in visited:
            visited.add(i)
            P_neighbors = region_query(i)
            if len(P_neighbors) >= min_samples:
                new_cluster = expand_cluster(i, P_neighbors)
                clusters.append(new_cluster)
            else:
                noise.add(i)

    labels = [-1] * n
    for idx, cluster in enumerate(clusters):
        for i in cluster:
            labels[i] = idx
    return labels

@app.route('/cluster', methods=['POST'])
def cluster():
    data = request.get_json()
    if not data or 'vectors' not in data:
        return jsonify({"error": "Invalid request"}), 400

    vectors = np.array(data['vectors'])
    labels = simple_dbscan(vectors)
    return jsonify(labels)

if __name__ == '__main__':
    app.run(port=5004)
