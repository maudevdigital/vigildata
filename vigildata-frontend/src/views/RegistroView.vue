<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const exito = ref(false)

async function handleRegistro() {
  error.value = ''
  try {
    await api.post('/auth/registro', { email: email.value, password: password.value })
    exito.value = true
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al registrarse'
  }
}
</script>

<template>
  <div class="flex justify-center mt-16">
    <form @submit.prevent="handleRegistro" class="bg-white p-8 rounded-lg shadow-md w-96">
      <h2 class="text-2xl font-bold mb-6 text-center">Crear Cuenta</h2>
      <div v-if="error" class="bg-red-100 text-red-700 p-2 rounded mb-4 text-sm">{{ error }}</div>
      <div v-if="exito" class="bg-green-100 text-green-700 p-2 rounded mb-4 text-sm">
        Cuenta creada. Redirigiendo...
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Email</label>
        <input v-model="email" type="email" required class="w-full border rounded px-3 py-2" />
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium mb-1">Contraseña</label>
        <input v-model="password" type="password" required minlength="6" class="w-full border rounded px-3 py-2" />
      </div>
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Registrarse
      </button>
      <p class="mt-4 text-center text-sm">
        ¿Ya tienes cuenta?
        <router-link to="/login" class="text-blue-600 hover:underline">Inicia sesión</router-link>
      </p>
    </form>
  </div>
</template>
