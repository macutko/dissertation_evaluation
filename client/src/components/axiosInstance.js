import axios from "axios";
import config from "../config";

const axiosInstance = axios.create({
    baseURL: config.baseURL,
});

axiosInstance.defaults.timeout = 10000;

export default axiosInstance;
