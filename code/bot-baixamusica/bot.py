import requests
import pandas as pd
from pytube import YouTube
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from pydub import AudioSegment
import io

df_urls = []

def get_video_urls(api_key, search_term, max_results=50):
    url = "https://www.googleapis.com/youtube/v3/search"
    video_urls = []
    next_page_token = ''
    
    while len(video_urls) < max_results:
        params = {
            'part': 'snippet',
            'q': search_term,
            'type': 'video',
            'key': api_key,
            'maxResults': 50,  # Máximo permitido por requisição
            'pageToken': next_page_token
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        for item in data.get('items', []):
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_urls.append(video_url)
            if len(video_urls) >= max_results:
                break
        
        next_page_token = data.get('nextPageToken', '')
        if not next_page_token:
            break
    
    return video_urls

# Exemplo de uso
api_key = 'AIzaSyCWObnv4njvm1AjwgzZUzh87RKTUW6D2CQ'  # Substitua pela sua chave de API
search_term = input("Prompt: ")
urls = get_video_urls(api_key, search_term, max_results=5000)  # Obtendo até 10 mil URLs

# Exibindo as URLs
for url in urls:
    df_urls.append(url)

# Configuração do cliente S3 usando credenciais locais
s3_client = boto3.client('s3')
sts = boto3.client('sts')
sts.get_caller_identity()

def baixar_e_enviar_para_s3(url, bucket_name):
    try:
        # Cria um objeto YouTube a partir da URL
        video = YouTube(url).streams.filter(only_audio=True).first()

        # URL do stream de áudio
        audio_url = video.url

        # Nome do arquivo no S3
        file_name = f"{video.title}.wav"

        # Faz o download do áudio e converte para WAV
        response = requests.get(audio_url, stream=True)
        response.raise_for_status()  # Lança um erro para status de resposta inválido
        
        # Cria um buffer de memória
        buffer = io.BytesIO()
        
        # Salva os dados no buffer em chunks
        for chunk in response.iter_content(chunk_size=8192):
            buffer.write(chunk)

        # Reinicia o buffer para leitura do início
        buffer.seek(0)

        # Converte o buffer para AudioSegment
        audio_segment = AudioSegment.from_file(buffer, format="mp4")  # `mp4` é usado para o áudio no YouTube

        # Cria um buffer para o arquivo WAV
        wav_buffer = io.BytesIO()
        audio_segment.export(wav_buffer, format="wav")

        # Reinicia o buffer para leitura do início
        wav_buffer.seek(0)

        # Faz o upload do buffer WAV para o S3
        s3_client.upload_fileobj(wav_buffer, bucket_name, file_name, ExtraArgs={'ContentType': 'audio/wav'})

        print(f"{video.title} baixado, convertido para WAV e enviado para o bucket S3 com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o áudio: {e}")
    except NoCredentialsError:
        print("Credenciais da AWS não encontradas.")
    except PartialCredentialsError:
        print("Credenciais da AWS incompletas.")
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")

# Processar cada URL
bucket_name = 'musics-raw'  # Substitua pelo nome do seu bucket S3
for url in df_urls:
    baixar_e_enviar_para_s3(url, bucket_name)
