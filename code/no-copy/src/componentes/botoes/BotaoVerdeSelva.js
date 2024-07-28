import React from 'react';
import './style/BotaoVariavel.css';
import './style/BotaoVerdeSelva.css'; // Importe o arquivo CSS com as classes de tamanho
// import '../typography.css';

function BotaoVerdeSelva({ children, tamanho }) {
  let classeBotao = 'botao-medio'; // Tamanho padrão é médio

  if (tamanho === 'pequeno') {
    classeBotao = 'botao-pequeno';
  } else if (tamanho === 'grande') {
    classeBotao = 'botao-grande';
  }

  return (
    <button className={`botao-verde-selva ${classeBotao}`}>
      {children}
    </button>
  );
}

export default BotaoVerdeSelva;
