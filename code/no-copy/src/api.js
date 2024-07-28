import axios from "axios";

const apiLogin = axios.create({
    baseURL : `http://127.0.0.1:5000/`//http://52.0.52.140:8080
})

export default apiLogin;