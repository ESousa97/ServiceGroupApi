from flask import Flask, request, jsonify
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/cluster', methods=['POST'])
def cluster():
    vectors = request.get_json().get('vectors', [])
    # Calcular a matriz de similaridade de cosseno
    cosine_sim = cosine_similarity(vectors)
    # Transformar similaridade em distância
    distance_matrix = 1 - cosine_sim
    # Garantir que não haja valores negativos na matriz de distância
    distance_matrix[distance_matrix < 0] = 0
    clustering = DBSCAN(eps=0.5, min_samples=2, metric='precomputed')
    labels = clustering.fit_predict(distance_matrix).tolist()  # Convertendo para lista
    return jsonify(labels)

if __name__ == '__main__':
    app.run(port=5004)
