// BoxAnalise.js
import React, { useState, useEffect } from 'react';
import './style/BoxAnalise.css';

const BoxAnalise = () => {
  const [progress, setProgress] = useState(0);
  const [text, setText] = useState("Analisando…");

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        const newProgress = prevProgress + 1;
        if (newProgress >= 100) {
          clearInterval(interval);
          setText("Análise Completa");
        }
        return newProgress;
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="box-analise">
      <h1>{text}</h1>
      <div className="barra-background">
        <div className="barra-progresso" style={{ width: `${progress}%` }}></div>
      </div>
      <div className="percentual">{progress.toFixed(2)}%</div>
    </div>
  );
};

export default BoxAnalise;
