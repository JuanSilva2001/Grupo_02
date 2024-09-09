import React from 'react';
import CampoTexto from '../campoTexto/CampoTexto';
import './style/BoxCadastro.css'; // Importe o arquivo CSS com os estilos

const BoxCadastro = () => {
  return (
    <div className="box-cadastro">
      <form>
        <label>Nome</label>
        <CampoTexto id="nome" label="Nome" type="text" placeholder="Digite seu nome"required />
        <label>Sobrenome</label>
        <CampoTexto id="sobrenome" label="Sobrenome" placeholder="Digite seu sobrenome" type="text" required />
        <label>Data de nascimento</label>
        <CampoTexto id="data-nascimento" label="Data de Nascimento" placeholder="dia/mês/ano" type="date" required />
        <label>E-mail</label>
        <CampoTexto id="email" label="E-mail" type="email" placeholder="Digite seu e-mail" required />
        <label>Confirmação do E-mail</label>
        <CampoTexto id="confirmar-email" label="Confirmação do E-mail" type="email" placeholder="Digite a confirmação do seu e-mail" required />
        <label>Senha</label>
        <CampoTexto id="senha" label="Senha" type="password" placeholder="Digite sua senha " required />
        <label>Confirmação da Senha</label>
        <CampoTexto id="confirmar-senha" label="Confirmação da Senha" type="password" placeholder="Digite confirmação da sua senha" required />
      </form>
    </div>
  );
};

export default BoxCadastro;
