import whisper
import os
import boto3

# Configurações AWS
S3_BUCKET = 'ml-models-sprint2'
AWS_ACCESS_KEY = 'ASIAUPKCN4FTSPELH4SY'
AWS_SECRET_KEY = 'EtHwwTotaak9ifl4MHa1aGyuxb7xijqppkRUpyOe'
AWS_SESSION_KEY = 'IQoJb3JpZ2luX2VjEKD//////////wEaCXVzLXdlc3QtMiJHMEUCIB/UyzJWO0/6xaM4x+Y/CuvW/YXPdsRoJf50lxV+SYRmAiEA32kunbJQ2+eeaxjgoF4wG0JygQKfv+3aY0q0Ee80c0EqtAIISRABGgwzMDc3NjYzNTQyNzkiDHpxj9SH1y8rIfZMqSqRAnv9/KAFl6wpkfQV4LFdpY69SJ58LYg/F4Z0CBLR9RST+9foq5RrUS5LGgYqhtaB+FoC934+BVHeKRcOxC+OEeixY+RC7Vnlih0U7nEiUzL9jjB8paPa1SXj5UOW4xfxxYts5gp53ea4pxDMnjEa4ykjAXHhcRq2U8Db0N5iY9a2FfzJUY8XgaUK/aM9Z2VCov7azKhf9VAkVecz9NcE/RbXiiSpI/7qMnxQCCJ/6EwO4d6/aiUicfz+tiGyu2IY3AJkHXX4SsDewNi4WJCm03xMg+9VWetsxDGKY7kSLW9syt3jiwe/JxNNfIWprOb6s8UAdg/4Ztp8h27JZuESkBtQMjezepVnSdd8cIfVgv7+pDDfo9GzBjqdAWJHndpaTJ35YFMxUnenV2OCGiXdv59JPxaoONGIKPNvsGmKmMlSfgUUX33P+nlY0Gr65elvI0I727vFbokLMmOYaE+wdNx6Wf8I8Vh0k+gIHxgDzT68QtYGRelnbTDSY5Bh8wE5pYHI/wYIZqF4lMt/6xmjIl2Q5AcH3m4Ey0v5EPP34WRuaUW/u6bkvk5VjfAFWITefubO4VRK4Ew='

s3_client = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  aws_session_token=AWS_SESSION_KEY)
modelo = whisper.load_model("medium")
caminho = os.getcwd()
s3_bucket = 'ml-models-sprint2'
caminhoMusica = f'{caminho}\\musics'
caminhoTextos = f'{caminho}\\text'
for diretorio,subpasta, arquivos in os.walk(caminhoMusica):
    if diretorio==caminhoMusica:
        for arquivo in arquivos:
            resposta = modelo.transcribe(f'{caminhoMusica}/{arquivo}')
            nome_arquivo = arquivo.split('.')[0]
            open(f"lyric_1.txt",'w').write(resposta['text'])
            s3_client.upload_file('lyric_1.txt', s3_bucket, 'lyric_1.txt')
            os.rename(f'{caminhoMusica}/{arquivo}', f'{caminhoMusica}/PRO/{arquivo}')