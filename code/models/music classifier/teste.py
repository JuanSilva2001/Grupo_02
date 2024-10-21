import librosa
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import StandardScaler

# Função para carregar áudio e aplicar STFT
def load_audio(file_path):
    y, sr = librosa.load(file_path)
    stft = librosa.stft(y)
    return stft, sr

# Função para limpar os dados e verificar se há NaNs ou Infs
def clean_features(feature):
    feature = np.nan_to_num(feature, nan=0.0, posinf=0.0, neginf=0.0)
    return feature

# Função para normalizar as características
def normalize_features(features):
    scaler = StandardScaler()
    return scaler.fit_transform(features.T).T

def extract_features(stft):
    try:
        mfcc = librosa.feature.mfcc(S=librosa.power_to_db(np.abs(stft)**2), n_mfcc=13)
        energy = np.sum(librosa.feature.rms(S=librosa.power_to_db(np.abs(stft)**2)), axis=1)
        mfcc = np.abs(mfcc)  # Corrigir valores negativos no MFCC
        entropy = -np.sum(mfcc * np.log(mfcc + 1e-10), axis=1)  # Evitar log(0) adicionando 1e-10
    except Exception as e:
        print(f"Erro ao extrair características: {e}")
        return None, None, None

    mfcc = clean_features(mfcc)
    energy = clean_features(energy)
    entropy = clean_features(entropy)

    # Normalizar os MFCCs e a energia
    mfcc = normalize_features(mfcc)
    energy = normalize_features(energy.reshape(1, -1))

    return mfcc, energy, entropy

# Função para ajustar o tamanho das características (cortar ou preencher com zeros)
def pad_features(feature, target_length):
    feature = clean_features(feature)
    if feature.shape[1] < target_length:
        pad_width = target_length - feature.shape[1]
        padded_feature = np.pad(feature, ((0, 0), (0, pad_width)), mode='constant')
        return padded_feature
    else:
        return feature[:, :target_length]

# Função para calcular a distância Euclidiana
def calculate_distance(features_a, features_b):
    if any(f is None for f in features_a) or any(f is None for f in features_b):
        print("Erro: uma ou mais características não puderam ser extraídas.")
        return None, None, None

    target_length = min(features_a[0].shape[1], features_b[0].shape[1])
    mfcc_a = pad_features(features_a[0], target_length)
    mfcc_b = pad_features(features_b[0], target_length)

    try:
        mfcc_distance = euclidean(mfcc_a.flatten(), mfcc_b.flatten())
        energy_distance = euclidean(features_a[1].flatten(), features_b[1].flatten())
        entropy_distance = euclidean(features_a[2], features_b[2])
    except Exception as e:
        print(f"Erro ao calcular a distância: {e}")
        return None, None, None

    return mfcc_distance, energy_distance, entropy_distance

# Função principal para comparar músicas
def compare_songs(song_a_path, song_b_path, threshold):
    stft_a, sr_a = load_audio(song_a_path)
    stft_b, sr_b = load_audio(song_b_path)

    features_a = extract_features(stft_a)
    features_b = extract_features(stft_b)

    distances = calculate_distance(features_a, features_b)
    if distances is None:
        print("Erro durante a comparação das músicas.")
        return

    print("Distâncias (MFCC, Energia, Entropia):", distances)

    if all(d is not None and d < threshold for d in distances):
        print("Evidências de plágio detectadas!")
    else:
        print("Sem evidências de plágio.")

# Exemplo de uso com limiar ajustado
song_a = './Under Pressure (Remastered 2011).mp3'  # Caminho da música A
song_b = './Vanilla Ice - Ice Ice baby (Single edit).mp3'  # Caminho da música B
limiar = 500  # Ajuste do limiar de similaridade

compare_songs(song_a, song_b, limiar)
