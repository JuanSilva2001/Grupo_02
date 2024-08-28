import React, { useState } from 'react';
import './style/Header.css';

function Header({ imagemAvatar }) {
  const [activeMenuItem, setActiveMenuItem] = useState('#home');
  var usuario = sessionStorage.getItem('Codigo')
  console.log(Number(usuario))
  if (Number(usuario) == 0){
    usuario = 'Login'
  }
  else{
    usuario = sessionStorage.getItem('Nome')
  }
  const handleMenuClick = (href) => {
    setActiveMenuItem(href);
  };

  const avatarStyle = {
    background: imagemAvatar 
      ? `url(${imagemAvatar}) lightgray 50% / cover no-repeat` 
      : 'var(--Azura-web, #E4F1F1)',
  };

  return (
    <header className="header">
      <div className="logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="232" height="42" viewBox="0 0 232 42" fill="none">
          <path d="M2 35V12.0169C2 8.96051 6.03614 7.86143 7.5858 10.4959L19.1191 30.1025C20.3417 32.1809 23.3926 32.0407 24.4194 29.8588L38 1M132 35H108C106.343 35 105 33.6569 105 32V10C105 8.34315 106.343 7 108 7H132M184 41V29M184 29V10C184 8.34315 185.343 7 187 7H199.524C202.228 7 203.552 10.2982 201.597 12.1679L184 29ZM205 41L217.5 24M230 7L217.5 24M217.5 24L211 7M171.429 25.9071L161.403 38.0823C160.175 39.5736 157.878 39.5322 156.704 37.9975L147.394 25.8224C146.571 24.7467 146.571 23.2533 147.394 22.1777L156.704 10.0025C157.878 8.4678 160.175 8.42636 161.403 9.91773L171.429 22.0929C172.342 23.2006 172.342 24.7994 171.429 25.9071ZM48.2629 7H67.1577C69.1094 7 70.5415 8.83417 70.0681 10.7276L64.5681 32.7276C64.2342 34.0631 63.0343 35 61.6577 35H41.9772C39.9841 35 38.5451 33.0923 39.0926 31.1758L45.3783 9.17584C45.7463 7.88793 46.9235 7 48.2629 7Z" stroke="#09BC8A" stroke-width="3"/>
          <circle cx="224.5" cy="38.5" r="2.5" fill="#09BC8A"/>
        </svg>
      </div>
      <nav className="menu">
        <a href="/" className={`menu-item ${activeMenuItem === '#home' ? 'active' : ''}`} onClick={() => handleMenuClick('#home')}>Home</a>
        <a href="/Avaliar-Musica" className={`menu-item ${activeMenuItem === '#avaliarLetra' ? 'active' : ''}`} onClick={() => handleMenuClick('#avaliarLetra')}>Avaliar Música</a>
        {!imagemAvatar && (
          <a href="/login" className={`menu-item ${activeMenuItem === '#logar' ? 'active' : ''}`} onClick={() => handleMenuClick('#logar')}>{usuario}</a>
        )}
        {imagemAvatar && (
          <>
            <div className="avatar" style={avatarStyle}></div>
            <a href="#sair" className={`menu-item ${activeMenuItem === '#sair' ? 'active' : ''}`} onClick={() => handleMenuClick('#sair')}>Sair</a>
          </>
        )}
      </nav>
    </header>
  );
}

export default Header;