import React from 'react';
import Header from '../../componentes/header/Header';
import BotaoVerdeSelva from '../../componentes/botoes/BotaoVerdeSelva';
import BotaoViridiano from '../../componentes/botoes/BotaoViridiano'; // Corrigido para BotaoViridiano conforme necessário
import './style/Home.css';

const Home = () => {
  return (
    <div className="home">
      <Header />
      <div className="content">
        <div className="text-and-image">
          <div className="text">
            <div className="welcome-text">
              <p>Bem-vindo ao <span className="no-copy">No Copy.</span>!</p>
            </div>
            <div className="description">
              <p>
                No Copy. é um projeto dedicado a investigar e avaliar a presença de plágio em produções musicais. Seja nas composições originais ou nas melodias, nossa missão é garantir a integridade artística e proteger os direitos autorais dos criadores.
                <br /><br />
                Se você é um músico preocupado com a originalidade de suas criações ou um profissional da indústria interessado em garantir a autenticidade das produções, o No Copy está aqui para ajudar.
              </p>
            </div>
          </div>
          <div className="image-container"></div>
        </div>
        <div className="buttons">
          <BotaoVerdeSelva tamanho="grande">Avaliar Música</BotaoVerdeSelva>
          <BotaoViridiano tamanho="grande">Cadastrar-se</BotaoViridiano>
        </div>
      </div>
    </div>  
  );
};

export default Home;

