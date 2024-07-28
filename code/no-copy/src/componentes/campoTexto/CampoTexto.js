import React, { useState } from 'react';
import './style/CampoTexto.css'; // Arquivo CSS para estilização do campo de texto

function CampoTexto(props, { placeholder })
{
  const [texto, setTexto] = useState('');

  const handleChange = (e) => {
    setTexto(e.target.value);
  };
  console.log(props.tipo) 
  return (
    <input
      type={props.tipo}
      id={props.id}
      className="campo-texto"
      placeholder={placeholder}
      value={texto}
      onChange={handleChange}
      style={{ color: texto ?  'var(--azura-web, #E4F1F1)' : '#ADB5BD' }}
    />
  );
}

export default CampoTexto;
