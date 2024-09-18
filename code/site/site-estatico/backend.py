from flask import Flask, request, jsonify
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import chain

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words('english'))
wnet = nltk.WordNetLemmatizer()

genres = ['Country', 'Rap', 'Rock']
loaded_models = {genre: joblib.load(f'./models/{genre}_model.joblib') for genre in genres}
vectorize = joblib.load('./models/tfidf_vectorizer.joblib')

def preprocess_text(text):
    df = pd.DataFrame({'lyrics': [text]})
    tokenized = [word_tokenize(lyr) for lyr in df['lyrics'].astype(str)]
    stop_vec = [[w for w in tok if w not in stop_words] for tok in tokenized]
    clean_vec = [[word for word in lyr if word.isalpha()] for lyr in stop_vec]
    lem = [[wnet.lemmatize(w) for w in lyr] for lyr in clean_vec]
    lyrics_tay = [' '.join(lyr) for lyr in lem]
    return vectorize.transform(lyrics_tay)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    lyrics = data.get('lyrics', '')

    vectorized_text = preprocess_text(lyrics)
    s_e = vectorized_text.todense().tolist()

    probabilities = {genre: loaded_models[genre].predict_proba(s_e)[0][1] for genre in genres}

    return jsonify(probabilities)

if __name__ == '__main__':
    app.run(debug=True)
