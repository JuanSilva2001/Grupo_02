import axios from "axios";

const apiLogin = axios.create({
    baseURL : `http://localhost:5000/`//http://52.0.52.140:8080
})

export default apiLogin;