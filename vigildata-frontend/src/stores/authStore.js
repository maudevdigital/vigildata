import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

function parsearUsuarioDesdeStorage() {
  try {
    const raw = localStorage.getItem('usuario')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const usuario = ref(parsearUsuarioDesdeStorage())

  const estaAutenticado = computed(() => !!token.value)
  const esAdmin = computed(() => usuario.value?.rol === 'ANALISTA')

  async function login(email, password) {
    const res = await api.post('/auth/login', { email, password })
    token.value = res.data.access_token
    usuario.value = res.data.usuario
    localStorage.setItem('token', token.value)
    localStorage.setItem('usuario', JSON.stringify(usuario.value))
  }

  async function registro(email, password) {
    await api.post('/auth/registro', { email, password })
  }

  function logout() {
    token.value = ''
    usuario.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
  }

  return { token, usuario, estaAutenticado, esAdmin, login, registro, logout }
})
