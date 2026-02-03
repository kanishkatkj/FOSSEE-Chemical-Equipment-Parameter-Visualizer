import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
});

// Add interceptor for auth if needed later
// api.interceptors.request.use((config) => { ... });

export default api;
