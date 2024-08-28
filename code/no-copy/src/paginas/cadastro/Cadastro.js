import React from 'react';
import './style/Cadastro.css';
import Header from '../../componentes/header/Header';
import BoxCadastro from '../../componentes/cadastro/BoxCadastro';
import BotaoViridiano from '../../componentes/botoes/BotaoViridiano';

const Cadastro = () => {
  return (
    <div className="cadastro">
      <Header />
      <div className="content">
        <h1 className="title">Cadastrar-se</h1>
        <BoxCadastro />
        <div className="buttons">
          <BotaoViridiano tamanho="grande">Cadastrar</BotaoViridiano>
        </div>
      </div>
    </div>
  );
};

export default Cadastro;
