import React from 'react';
import CampoTexto from '../campoTexto/CampoTexto';
import './style/BoxLogin.css'; // Arquivo CSS para estilização da box de login
import api from '../../api';
import { useState } from 'react';

function BoxLogin() {
  const [funcData, setFuncData] = useState({
    email: "",
    senha: ""
})
  async function enviar() {
    funcData.email = document.getElementById("idEmail").value;
    funcData.senha = document.getElementById("idSenha").value;
    console.log(funcData);
    if(funcData.email=="adm@bp.com" && funcData.senha=="Senha123"){
        // Swal.fire(
        //     'Login efetuado',
        //     'Vamos lá!',
        //     'success'
        //   );
        // redirecionar("DashboardMapa")
    }
    else{
      api.post("/login", {
        email: funcData.email,
        senha: funcData.senha
    }).then((resposta) => {
        console.log("post ok", resposta);
        console.log("Codigo: ",resposta.data.codigo)
        sessionStorage.setItem("Codigo", resposta.data.codigo);
        sessionStorage.setItem("Nome", resposta.data.nome)
        redirecionar(); 
    }).catch((resposta) =>{
            console.log( resposta);
            document.getElementById("idEmail").style="border: 2px solid red";
            document.getElementById("idSenha").style="border: 2px solid red";
        })
  }
}

document.addEventListener('keydown', function (event) {
    if (event.code === 'Enter'){
        enviar()
    }
});

  return (
    <div className="box-login">
      <form>
        <label>E-mail</label>
        <CampoTexto id="idEmail" label="username" tipo="text" placeholder="Digite seu email" />
        <label>Senha</label> 
        <CampoTexto id="idSenha" label="password" tipo="password" placeholder="Digite sua senha" />
      </form>
    </div>
  );
}

export default BoxLogin;
function redirecionar() {
  window.location.href = `http://localhost:3000/`;
}