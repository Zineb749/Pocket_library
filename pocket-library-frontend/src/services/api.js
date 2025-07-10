import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // adresse où tourne FastAPI
});

export default api;
