import pathlib
import warnings
import numpy as np
import librosa
import pandas as pd
import matplotlib.pyplot as plt
import boto3
import os
from io import BytesIO
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report
import joblib
from sklearn.pipeline import make_pipeline

warnings.filterwarnings('ignore', category=FutureWarning)

# DataFrame global para armazenar todas as músicas processadas
df_master_songs = pd.DataFrame()

s3_client = boto3.client('s3')
bucket_name = 'musics-raw'
model_name = 'predict_song_models.pkl'
model_path = 'no-copy-models/' + model_name

def download_file_from_s3(key, local_filename):
    print(f'Download do arquivo {key} para {local_filename}')
    s3_client.download_file(bucket_name, key, local_filename)

def upload_file_to_s3(local_filename, s3_key):
    print(f'Upload do arquivo {local_filename} para {s3_key}')
    s3_client.upload_file(local_filename, bucket_name, s3_key)

def delete_file(local_filename):
    if os.path.exists(local_filename):
        os.remove(local_filename)
        print(f'Arquivo {local_filename} excluído.')
    else:
        print(f'Arquivo {local_filename} não encontrado.')

def stft(song, number):
    global df_master_songs
    print(f'Processando arquivo {song}...')
    try:
        y, sr = librosa.load(song, sr=None, mono=True)
        
        S = librosa.stft(y, n_fft=2048, hop_length=512, win_length=1024)
        S = np.abs(S)

        max_indices = np.argwhere(S == np.max(S, axis=0))
        times = librosa.frames_to_time(max_indices[:, 1], sr=sr)
        frequencies = librosa.fft_frequencies(sr=sr)[max_indices[:, 0]]
        
        # Criação do DataFrame da música atual
        df_song = pd.DataFrame({'Frequencia': frequencies, 'Tempo': times})
        
        # Atribuir o valor de target para todas as linhas
        df_song['target'] = number
        
        # Concatenando no DataFrame global
        df_master_songs = pd.concat([df_master_songs, df_song], ignore_index=True)

        print(f"Processado {song} e adicionado ao DataFrame. Total de linhas no DataFrame: {len(df_master_songs)}")
        print(df_master_songs.head())  # Mostrar as primeiras linhas do DataFrame para verificação

    except Exception as e:
        print(f'Erro ao processar {song}: {e}')

    return df_master_songs

def training_model(data):
    if data.empty:
        print('DataFrame está vazio. Não é possível treinar o modelo.')
        return

    # Verificar se a coluna 'target' está presente
    if 'target' not in data.columns:
        print("A coluna 'target' não está presente no DataFrame.")
        return
    
    # Remover a coluna 'target' do conjunto de features
    target = data.pop('target')
    X = data
    y = target

    # Divisão entre treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Ajustar o scaler com os dados de treino
    scaler = StandardScaler()
    X_train_n = scaler.fit_transform(X_train)  # Ajustar e transformar os dados de treino
    X_test_n = scaler.transform(X_test)        # Transformar os dados de teste

    # Redução de dimensionalidade usando PCA
    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train_n)
    X_test_pca = pca.transform(X_test_n)

    # Converte as variáveis de target para inteiros
    y_train_int = y_train.astype(int)
    y_test_int = y_test.astype(int)

    # KNN    
    k_values = list(range(2, 15))
    metrics = []

    # Loop para encontrar o melhor valor de k
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_pca, y_train_int)
        
        y_test_int_pred = knn.predict(X_test_pca)
        test_accuracy = accuracy_score(y_test_int, y_test_int_pred)
        metrics.append({
            'k': k,
            'accuracy': test_accuracy,
            'classification_report': classification_report(y_test_int, y_test_int_pred, output_dict=True),
        })

    # Selecionar o melhor k
    best_metric = max(metrics, key=lambda m: m['accuracy'])
    knn_best = KNeighborsClassifier(n_neighbors=best_metric["k"])

    # Treinamento final do melhor KNN
    knn_best.fit(X_train_pca, y_train_int)

    # Criar o pipeline com o scaler ajustado e o modelo treinado
    pipe = make_pipeline(scaler, knn_best)

    # Salvar o pipeline treinado localmente
    joblib.dump(pipe, model_name)
    
    # Fazer upload do modelo para o bucket S3
    upload_file_to_s3(model_name, model_path)

    # Excluir o arquivo local
    delete_file(model_name)

    print('Treinamento realizado com sucesso e modelo enviado para o S3!')

def visualization(prediction):
    counts = np.bincount(prediction)
    labels = ['Audio', 'Dido Cover 1', 'Dido Cover 2', 'Leans']
    frequencies = counts[:len(labels)]

    plt.bar(labels, frequencies, color='blue')
    plt.xlabel('Valores')
    plt.ylabel('Frequência')
    plt.title('Frequência dos Valores')
    plt.show()

    return frequencies

def etl(song_key, type, number):
    local_filename = os.path.join('temp', pathlib.Path(song_key).name)
    print(f'Download do arquivo {song_key} para {local_filename}')
    download_file_from_s3(song_key, local_filename)

    if type == 'training':
        print(f'Iniciando processamento STFT para {local_filename}...')
        stft(local_filename, number)
        if not df_master_songs.empty:
            print('Base de músicas atualizada com sucesso!')
        else:
            print('Dados insuficientes/vazio...')
        # Excluir o arquivo local após processamento
        delete_file(local_filename)
    
    elif type == 'predict':
        print('Carregando modelo...')
        knn_from_joblib = joblib.load(model_name)
        song_stft = stft(local_filename, number)
        
        if not song_stft.empty:
            # Remover a coluna 'target' antes da predição
            song_stft_predict = song_stft.drop(columns=['target'])
            print('Fazendo predição...')
            prediction = knn_from_joblib.predict(song_stft_predict)
            viz = visualization(prediction)
            return viz
        else:
            print('Dados insuficientes para predição...')
        
        # Excluir o arquivo local após processamento
        delete_file(local_filename)

# -----------

# Crie um diretório temporário para baixar arquivos
os.makedirs('temp', exist_ok=True)

# Iterar sobre as músicas no bucket
print('Listando objetos no bucket...')
try:
    bucket_objects = s3_client.list_objects_v2(Bucket=bucket_name).get('Contents', [])
    if not bucket_objects:
        print('Nenhum objeto encontrado no bucket.')
    else:
        print(f'{len(bucket_objects)} objeto(s) encontrado(s) no bucket.')
        number = 0
        for obj in bucket_objects:
            key = obj['Key']
            # Processar apenas arquivos de áudio
            print(f'Processando arquivo: {key}')
            etl(key, 'training', number)
            number += 1
        # Verificar o DataFrame antes de treinar o modelo
        if df_master_songs.empty:
            print('DataFrame ainda está vazio após processar os arquivos.')
        else:
            print('Treinando modelo...')
            training_model(df_master_songs)

except Exception as e:
    print(f'Erro ao listar objetos no bucket: {e}')

# Excluir todos os arquivos temporários
for temp_file in os.listdir('temp'):
    delete_file(os.path.join('temp', temp_file))

# Excluir o diretório temporário
try:
    os.rmdir('temp')
except OSError as e:
    print(f'Erro ao excluir o diretório temporário: {e}')
