import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

export function normalizarToken(token) {
  if (!token || typeof token !== 'string') return ''
  let limpio = token.trim()
  if (limpio.toLowerCase().startsWith('bearer ')) {
    limpio = limpio.slice(7).trim()
  }
  return limpio
}

function obtenerToken() {
  return normalizarToken(localStorage.getItem('token'))
}

api.interceptors.request.use((config) => {
  const token = obtenerToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || ''
    const esAuthPublico = url.includes('/auth/login') || url.includes('/auth/registro')
    if (error.response?.status === 401 && !esAuthPublico) {
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login?sesion=expirada'
      }
    }
    return Promise.reject(error)
  }
)

export default api
