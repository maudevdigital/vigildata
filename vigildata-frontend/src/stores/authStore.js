import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { normalizarToken } from '../services/api'

function parsearUsuarioDesdeStorage() {
  try {
    const raw = localStorage.getItem('usuario')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function guardarToken(valor) {
  const limpio = normalizarToken(valor)
  if (!limpio) return ''
  localStorage.setItem('token', limpio)
  return limpio
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(normalizarToken(localStorage.getItem('token')))
  const usuario = ref(parsearUsuarioDesdeStorage())

  const estaAutenticado = computed(() => !!token.value)

  const esAdmin = computed(() => usuario.value?.rol === 'ANALISTA')

  async function verificarSesion() {
    if (!token.value) return false
    try {
      const res = await api.get('/auth/me')
      usuario.value = res.data
      localStorage.setItem('usuario', JSON.stringify(usuario.value))
      return true
    } catch {
      logout()
      return false
    }
  }

  async function login(email, password) {
    const res = await api.post('/auth/login', { email, password })
    token.value = guardarToken(res.data.access_token)
    usuario.value = res.data.usuario
    localStorage.setItem('usuario', JSON.stringify(usuario.value))
  }

  async function registro(email, password) {
<<<<<<< Updated upstream
    await api.post('/auth/registro', { email, password })
=======
    const res = await api.post('/auth/registro', { email, password })
    token.value = guardarToken(res.data.access_token)
    usuario.value = res.data.usuario
    localStorage.setItem('usuario', JSON.stringify(usuario.value))
>>>>>>> Stashed changes
  }

  function logout() {
    token.value = ''
    usuario.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
  }

  return { token, usuario, estaAutenticado, esAdmin, login, registro, logout, verificarSesion }
})
