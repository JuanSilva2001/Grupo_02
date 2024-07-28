import React, { useState }  from 'react';
import './style/AvaliarMusica.css';
import Header from '../../componentes/header/Header';
import { BoxUpload } from '../../componentes/boxUpload/BoxUpload';
import BotaoVerdeMeiaNoite from '../../componentes/botoes/BotaoVerdeMeiaNoite';
import BotaoVerdeSelva from '../../componentes/botoes/BotaoVerdeSelva';
import api from '../../api'

const AvaliarMusica = () => {
  const [file, setFile] = useState(null);
  async function enviar(e) {
    setFile(document.getElementById('Arquivo').files[0]);
    const formData = new FormData();
    formData.append('file', file);
    var codigo = sessionStorage.getItem('Codigo')
    console.log(codigo)
    e.preventDefault();
    api.post(`/upload/${codigo}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
    });
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
