from flask import Flask, request, jsonify
import joblib
import pickle
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import chain
import librosa
import numpy as np
import os

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

# NLTK downloads
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))
wnet = nltk.WordNetLemmatizer()

genres = ['Country', 'Rap', 'Rock']
loaded_models = {genre: joblib.load(f'./models/{genre}_model.joblib') for genre in genres}
vectorize = joblib.load('./models/tfidf_vectorizer.joblib')
scaler = joblib.load('./models/scaler.pkl')
knn_model = joblib.load('./models/knn_model.pkl')

with open("./models/vectorize.pkl", "rb") as f:
    vectorize_model = pickle.load(f)

# with open("./models/songs.pkl", "rb") as f:
#     songs, vectors = pickle.load(f)

def preprocess_text(text):
    df = pd.DataFrame({'lyrics': [text]})
    tokenized = [word_tokenize(lyr) for lyr in df['lyrics'].astype(str)]
    stop_vec = [[w for w in tok if w not in stop_words] for tok in tokenized]
    clean_vec = [[word for word in lyr if word.isalpha()] for lyr in stop_vec]
    lem = [[wnet.lemmatize(w) for w in lyr] for lyr in clean_vec]
    
    lyrics_tay = [' '.join(lyr) for lyr in lem]

    return vectorize.transform(lyrics_tay)

def prever_musicas_parecidas(letra_nova, num_resultados=3):
    letra_nova_vector = vectorize_model.transform([letra_nova])
    similaridade = cosine_similarity(letra_nova_vector, vectors).flatten()
    indices_similares = similaridade.argsort()[::-1][:num_resultados]

    musicas_parecidas = songs.iloc[indices_similares]
    similaridade_mais_parecida = similaridade[indices_similares].max()
    musica_mais_parecida = musicas_parecidas.iloc[0]['SName']

    resultado = {
        'musica_mais_parecida': musica_mais_parecida,
        'similaridade': similaridade_mais_parecida * 100,
        'musicas': musicas_parecidas[['SName', 'Lyric']].to_dict(orient='records')
    }

    return resultado


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    lyrics = data.get('lyrics', '')

    vectorized_text = preprocess_text(lyrics)
    s_e = vectorized_text.todense().tolist()

    probabilities = {genre: loaded_models[genre].predict_proba(s_e)[0][1] for genre in genres}

    return jsonify(probabilities)

@app.route('/predict_lyric', methods=['POST'])
def predict_lyric():
    data = request.get_json(force=True)
    lyrics = data.get('lyrics', '')

    vectorized_text = preprocess_text(lyrics)
    s_e = vectorized_text.todense().tolist()
    probabilities = {genre: loaded_models[genre].predict_proba(s_e)[0][1] for genre in genres}

    similar_songs = prever_musicas_parecidas(lyrics)

    result = {
        'probabilities': probabilities,
        'similar_songs': similar_songs
    }

    return jsonify(result)

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    avg_frequency = np.mean(spectral_centroid)

    duration = librosa.get_duration(y=y, sr=sr)

    return [avg_frequency, duration]

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400

    file = request.files['file']

    temp_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(temp_path)

    print(f"Arquivo salvo em: {temp_path}")

    features = extract_features(temp_path)
    print(f"Características extraídas: {features}")

    features_scaled = scaler.transform([features])
    print(f"Características escaladas: {features_scaled}")

    prediction = knn_model.predict(features_scaled)
    print(f"Previsão: {prediction[0]}")

    os.remove(temp_path)

    result = {
        'previsao': int(prediction[0])
    }

    return jsonify(result)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
