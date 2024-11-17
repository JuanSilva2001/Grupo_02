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

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

# NLTK downloads
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words('english'))
wnet = nltk.WordNetLemmatizer()

genres = ['Country', 'Rap', 'Rock']
loaded_models = {genre: joblib.load(f'./models/{genre}_model.joblib') for genre in genres}
vectorize = joblib.load('./models/tfidf_vectorizer.joblib')

with open("./models/vectorize_model.pkl", "rb") as f:
    vectorize_model = pickle.load(f)

with open("./models/songs.pkl", "rb") as f:
    songs, vectors = pickle.load(f)

def preprocess_text(text):
    df = pd.DataFrame({'lyrics': [text]})
    tokenized = [word_tokenize(lyr) for lyr in df['lyrics'].astype(str)]
    stop_vec = [[w for w in tok if w not in stop_words] for tok in tokenized]
    clean_vec = [[word for word in lyr if word.isalpha()] for lyr in stop_vec]
    lem = [[wnet.lemmatize(w) for w in lyr] for lyr in clean_vec]
    
    # Create a list of cleaned lyrics from the lemmatized words
    lyrics_tay = [' '.join(lyr) for lyr in lem]

    # Make sure to return a list of strings
    return vectorize.transform(lyrics_tay)

def prever_musicas_parecidas(letra_nova, num_resultados=3):
    # Transform the new lyrics using the same vectorizer
    letra_nova_vector = vectorize_model.transform([letra_nova])  # Wrap in a list
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
