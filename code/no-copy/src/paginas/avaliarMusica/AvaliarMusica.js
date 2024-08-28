import React, { useState }  from 'react';
import './style/AvaliarMusica.css';
import Header from '../../componentes/header/Header';
import { BoxUpload } from '../../componentes/boxUpload/BoxUpload';
import BotaoVerdeMeiaNoite from '../../componentes/botoes/BotaoVerdeMeiaNoite';
import BotaoVerdeSelva from '../../componentes/botoes/BotaoVerdeSelva';
import api from '../../api'

const AvaliarMusica = () => {
  async function enviar() {
        // alert('Funcionando')
        const fileInput = document.getElementById('audioFile');
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = async (e) => {
            const arrayBuffer = e.target.result;
            try {
                const response = await fetch('https://f6du96p34c.execute-api.us-east-1.amazonaws.com/v1/send-songs', {
                    method: 'POST',
                    body: arrayBuffer,
                    headers: {
                        'Content-Type': 'audio/mpeg', // Ensure this matches the expected MIME type
                    },
                });
                // alert(response)

                const result = await response.text(); // Get the response text

                if (response.ok) {
                    alert('Áudio enviado com sucesso!');
                } else {
                    alert(`Falha ao enviar o áudio. Código: ${response.status}. Mensagem: ${result}`);
                }
            } catch (error) {
                console.error('Erro ao enviar o áudio:', error); // Log the error
                // alert(`Ocorreu um erro ao enviar o áudio: ${error.message}`);
            }
        };

        reader.onerror = (error) => {
            console.error('Erro ao ler o arquivo:', error); // Log the error
            console.log(`Erro ao ler o arquivo: ${error.message}`);
        };
        reader.readAsArrayBuffer(file);
}
  return (
    <div className="avaliar-musica">
      <Header />
      <div className="content">
        <h1 className="title">Avaliar Música</h1>
        <BoxUpload/>
        <BotaoVerdeMeiaNoite tamanho="pequeno">Procurar seus arquivos</BotaoVerdeMeiaNoite>
        <div className="buttons" onClick={enviar}>
          <BotaoVerdeSelva  tamanho="medio">Avaliar</BotaoVerdeSelva>
        </div>
      </div>
    </div>
  );
};

export default AvaliarMusica;
