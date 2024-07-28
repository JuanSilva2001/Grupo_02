import axios from "axios";

const apiLogin = axios.create({
    baseURL : `http://50.16.152.183:5000/`//http://52.0.52.140:8080
})

export default apiLogin;