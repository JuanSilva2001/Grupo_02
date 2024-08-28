import React from 'react';
import './style/BotaoVariavel.css'; // Importe o arquivo CSS com as classes de tamanho
import './style/BotaoViridiano.css'; // Importe o arquivo CSS com as classes de tamanho


function BotaoViridiano({ children, tamanho }) {
  let classeBotao = 'botao-medio'; // Tamanho padrão é médio

  if (tamanho === 'pequeno') {
    classeBotao = 'botao-pequeno';
  } else if (tamanho === 'grande') {
    classeBotao = 'botao-grande';
  }

  return (
    <button className={`botao-viridiano ${classeBotao}`} onClick={()=>redirecionar("cadastro")}>
      {children}
    </button>
  );
}

export default BotaoViridiano;
function redirecionar(pagina) {
  window.location.href = 'http://localhost:3000/' + pagina;
}