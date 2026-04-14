import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const usuario = ref(null)

  const estaAutenticado = computed(() => !!token.value)

  async function login(email, password) {
    const res = await api.post('/auth/login', { email, password })
    token.value = res.data.access_token
    localStorage.setItem('token', token.value)
  }

  function logout() {
    token.value = ''
    usuario.value = null
    localStorage.removeItem('token')
  }

  return { token, usuario, estaAutenticado, login, logout }
})
