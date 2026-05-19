<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const cargando = ref(false)

onMounted(() => {
  if (route.query.sesion === 'expirada') {
    error.value = 'Tu sesión expiró o no es válida. Inicia sesión nuevamente.'
  }
})

async function handleLogin() {
  error.value = ''
  cargando.value = true
  try {
    await auth.login(email.value, password.value)
    router.push(auth.esAdmin ? '/admin' : '/mapa')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al iniciar sesión'
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="flex justify-center mt-16">
    <form @submit.prevent="handleLogin" class="bg-white p-8 rounded-lg shadow-md w-96">
      <h2 class="text-2xl font-bold mb-6 text-center">Iniciar Sesión</h2>
      <div v-if="error" class="bg-red-100 text-red-700 p-2 rounded mb-4 text-sm">{{ error }}</div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Email</label>
        <input v-model="email" type="email" required class="w-full border rounded px-3 py-2" />
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium mb-1">Contraseña</label>
        <input v-model="password" type="password" required class="w-full border rounded px-3 py-2" />
      </div>
      <button type="submit" :disabled="cargando" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-60">
        {{ cargando ? 'Ingresando...' : 'Ingresar' }}
      </button>
      <p class="mt-4 text-center text-sm">
        ¿No tienes cuenta?
        <router-link to="/registro" class="text-blue-600 hover:underline">Regístrate</router-link>
      </p>
    </form>
  </div>
</template>
