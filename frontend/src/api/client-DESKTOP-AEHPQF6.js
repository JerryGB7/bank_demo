// single shared Axios instance that every component uses to talk to the fastapi backend

import axios from 'axios'

//axios.create is a function that builds a reusable pre-configured client
const apiClient = axios.create({
    // fastapi endpoint
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
})

// the request interceptor is needed to check every outgoing request
// and checks if a token is sitting in localstorage. 
// then it attaches it as the authorization automatically
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('bankToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config
});


export default apiClient;