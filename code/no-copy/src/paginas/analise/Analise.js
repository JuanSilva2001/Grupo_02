import React from 'react';
import './style/Analise.css';
import Header from '../../componentes/header/Header';
import ResultadoAnalise from '../../componentes/resultadoAnalise/ResultadoAnalise';

const Analise = () => {
  return (
    <div className="analise">
      <Header />
      <div className="content">
        <h1 className="title">Análise</h1>
        <ResultadoAnalise  similaridadeMelodica = '70' similaridadeLirica = '30'/>
      </div>
    </div>
  );
};

export default Analise;
