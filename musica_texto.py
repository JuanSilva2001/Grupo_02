import whisper
import os
modelo = whisper.load_model("medium")
caminho = os.getcwd()
caminhoMusica = f'{caminho}\\Musicas'
caminhoTextos = f'{caminho}\\Texto'
for diretorio,subpasta, arquivos in os.walk(caminhoMusica):
    if diretorio==caminhoMusica:
        for arquivo in arquivos:
            resposta = modelo.transcribe(f'{caminhoMusica}/{arquivo}')
            nome_arquivo = arquivo.split('.')[0]
            open(f"{caminhoTextos}/{nome_arquivo}.txt",'w').write(resposta['text'])
            os.rename(f'{caminhoMusica}/{arquivo}', f'{caminhoMusica}/PRO/{arquivo}')