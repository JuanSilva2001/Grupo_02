import React from 'react';
import './style/ResultadoAnalise.css';

const ResultadoAnalise = ({ similaridadeMelodica, similaridadeLirica }) => {
  const renderDonutChart = (percent, titulo) => {
    const radius = 80;
    const strokeWidth = 10;
    const viewBoxSize = radius * 2;

    const circumference = 2 * Math.PI * radius;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference * (1 - percent / 100);

    const fillColor = percent >= 50 ? '#DA3E52' : 'transparent';

    return (
      <div className="donut-container">
        <h2>{titulo}</h2>
        <svg width={viewBoxSize} height={viewBoxSize} viewBox={`0 0 ${viewBoxSize} ${viewBoxSize}`}>
          <circle
            className="donut-chart-background"
            cx={radius}
            cy={radius}
            r={radius - strokeWidth / 2}
            strokeWidth={strokeWidth}
            fill="transparent"
            stroke="#09BC8A"
          />
          <circle
            className="donut-chart-progress"
            cx={radius}
            cy={radius}
            r={radius - strokeWidth / 2}
            strokeWidth={strokeWidth}
            stroke={fillColor}
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            fill="transparent"
          />
          <text x={radius} y={radius} className="donut-chart-text">
            {percent}%
          </text>
        </svg>
      </div>
    );
  };

  return (
    <div className="resultado-analise">
      <div className="analise-container">
        <div className="similaridade">
          {renderDonutChart(similaridadeMelodica, 'Similaridade Melódica')}
        </div>
        <div className="similaridade">
          {renderDonutChart(similaridadeLirica, 'Similaridade Lírica')}
        </div>
      </div>
      <div className="analise-texto">
        <div className="analise-texto-item">
          <h3>Resultado da análise melódica</h3>
          <p>
            A uma similaridade de {similaridadeMelodica}% na melodia com a música: Segredo dos seus olhos, do artista Caio.
          </p>
          <p>
            Esse índice de similaridade indica que pode haver problemas com plágio.
          </p>
          <ul>
            <li>Segredo dos seus olhos - 70%</li>
            <li>Balada boa - 35%</li>
            <li>Celestial Waltz - 5%</li>
            <li>Danse des Étoiles - 5%</li>
            <li>Amar - 2%</li>
          </ul>
        </div>
        <div className="analise-texto-item">
          <h3>Resultado da análise lírica</h3>
          <p>
            A uma similaridade de {similaridadeLirica}% na lírica com a música Amanhã eu vou, da artista Luiza Lena.
          </p>
          <p>
            Esse índice de similaridade não indica nenhum possível problema com plágio.
          </p>
          <ul>
            <li>Amanhã eu vou - 5%</li>
            <li>Amiga Lu - 4%</li>
            <li>Susurros del Mar - 4%</li>
            <li>Amar - 3%</li>
            <li>Balada boa - 2%</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ResultadoAnalise;
