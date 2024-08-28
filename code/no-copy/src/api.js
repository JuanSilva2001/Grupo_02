import axios from "axios";

const apiLogin = axios.create({
    baseURL : `https://f6du96p34c.execute-api.us-east-1.amazonaws.com/v1`//http://52.0.52.140:8080
})

export default apiLogin;