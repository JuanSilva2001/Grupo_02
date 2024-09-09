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

api_key = 'AIzaSyCWObnv4njvm1AjwgzZUzh87RKTUW6D2CQ'
search_term = input("Prompt: ")
urls = get_video_urls(api_key, search_term, max_results=5000)

for url in urls:
    df_urls.append(url)

s3_client = boto3.client('s3')
sts = boto3.client('sts')
sts.get_caller_identity()

def baixar_e_enviar_para_s3(url, bucket_name):
    try:
        video = YouTube(url).streams.filter(only_audio=True).first()
        file_name = f"{video.title}.wav"
        local_path = os.path.join(os.getcwd(), file_name)

        # Baixar o áudio localmente
        video.download(filename=f"{video.title}.mp4")

        # Converter para WAV
        audio_segment = AudioSegment.from_file(f"{video.title}.mp4", format="mp4")
        audio_segment.export(local_path, format="wav")

        # Upload para o S3
        with open(local_path, 'rb') as data:
            s3_client.upload_fileobj(data, bucket_name, file_name, ExtraArgs={'ContentType': 'audio/wav'})

        print(f"{video.title} baixado, convertido para WAV e enviado para o bucket S3 com sucesso.")

        # Excluir arquivo local
        os.remove(local_path)
        os.remove(f"{video.title}.mp4")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o áudio: {e}")
    except NoCredentialsError:
        print("Credenciais da AWS não encontradas.")
    except PartialCredentialsError:
        print("Credenciais da AWS incompletas.")
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")

bucket_name = 'musics-raw'
for url in df_urls:
    baixar_e_enviar_para_s3(url, bucket_name)
