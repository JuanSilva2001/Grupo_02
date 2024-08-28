import React from 'react';
import './style/BotaoVariavel.css';
import './style/BotaoVerdeMeiaNoite.css';
 // Importe o arquivo CSS com as classes de tamanho


function BotaoVerdeMeiaNoite({ children, tamanho }) {
  // 'tamanho' é uma propriedade opcional para definir o tamanho do botão
  let classeBotao = 'botao-medio'; // Tamanho padrão é médio

  if (tamanho === 'pequeno') {
    classeBotao = 'botao-pequeno';
  } else if (tamanho === 'grande') {
    classeBotao = 'botao-grande';
  }

  return (
    <button className={`botao-verde-meia-noite ${classeBotao}`}>
      {children}
    </button>
  );
}

export default BotaoVerdeMeiaNoite;
