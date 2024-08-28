import React from 'react';
import './style/Login.css';
import Header from '../../componentes/header/Header';
import BoxLogin from '../../componentes/login/BoxLogin';
import BotaoVerdeSelva from '../../componentes/botoes/BotaoVerdeSelva';
import BotaoViridiano from '../../componentes/botoes/BotaoViridiano';

const Login = () => {
  return (
    <div className="login">
      <Header />
      <div className="content">
        <h1 className="logar">Logar</h1>
        <BoxLogin />
        <div className="buttons">
          <BotaoVerdeSelva tamanho="medio">Logar</BotaoVerdeSelva>
          <BotaoViridiano tamanho="medio">Cadastrar-se</BotaoViridiano>
        </div>
      </div>
    </div>
  );
};

export default Login;
