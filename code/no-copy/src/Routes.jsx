import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from './paginas/home/home';
import Login from "./paginas/login/Login";
import Cadastro from './paginas/cadastro/Cadastro';
import AvaliarMusica from './paginas/avaliarMusica/AvaliarMusica';
import Analise from './paginas/analise/Analise';

function Rotas() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/cadastro" element={<Cadastro />} />
                <Route path="/Avaliar-Musica" element={<AvaliarMusica />} />
            </Routes>
        </BrowserRouter>
    );
}

export default Rotas;