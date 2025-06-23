import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
})

export function setToken(token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export function clearToken() {
  delete api.defaults.headers.common['Authorization']
}

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);