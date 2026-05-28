import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const http = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const auth = useAuthStore()
      try {
        const { data } = await axios.post('/api/v1/auth/refresh', {
          refresh_token: auth.refreshToken,
        })
        auth.setTokens(data.access_token, data.refresh_token)
        originalRequest.headers.Authorization = `Bearer ${data.access_token}`
        return http(originalRequest)
      } catch {
        auth.logout()
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default http
