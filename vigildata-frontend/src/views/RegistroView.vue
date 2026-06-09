<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { obtenerIdTokenGoogle } from '../services/googleAuth'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const exito = ref(false)
const cargando = ref(false)

async function handleRegistro() {
  error.value = ''
  cargando.value = true
  try {
    await auth.registro(email.value, password.value)
    exito.value = true
    setTimeout(() => router.push('/mapa'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al registrarse'
  } finally {
    cargando.value = false
  }
}

async function handleGoogle() {
  error.value = ''
  cargando.value = true
  try {
    const idToken = await obtenerIdTokenGoogle()
    await auth.loginConGoogle(idToken)
    router.push(auth.esAdmin ? '/admin' : '/mapa')
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'No se pudo registrar con Google'
  } finally {
    cargando.value = false
  }
}

// Al volver del callback de Google (la URL trae #access_token=...) completamos
// el alta/ingreso automaticamente sin que el usuario tenga que volver a tocar.
onMounted(() => {
  if (window.location.hash.includes('access_token')) handleGoogle()
})
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
      <button type="submit" :disabled="cargando" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-60">
        {{ cargando ? 'Registrando...' : 'Registrarse' }}
      </button>
      <div class="my-4 flex items-center gap-2 text-xs text-gray-400">
        <span class="flex-1 h-px bg-gray-200"></span>
        <span>o</span>
        <span class="flex-1 h-px bg-gray-200"></span>
      </div>
      <button
        type="button"
        class="w-full border border-gray-300 bg-white text-gray-700 py-2 rounded hover:bg-gray-50 disabled:opacity-60 touch-target flex items-center justify-center gap-2"
        :disabled="cargando"
        @click="handleGoogle"
      >
        <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true">
          <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.4 29.3 35.5 24 35.5c-6.4 0-11.5-5.1-11.5-11.5S17.6 12.5 24 12.5c2.9 0 5.6 1.1 7.6 2.9l5.7-5.7C33.6 6.3 29 4.5 24 4.5 13.2 4.5 4.5 13.2 4.5 24S13.2 43.5 24 43.5 43.5 34.8 43.5 24c0-1.2-.1-2.3-.3-3.5z"/>
          <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 16 19 12.5 24 12.5c2.9 0 5.6 1.1 7.6 2.9l5.7-5.7C33.6 6.3 29 4.5 24 4.5 16.3 4.5 9.7 8.9 6.3 14.7z"/>
          <path fill="#4CAF50" d="M24 43.5c5 0 9.5-1.9 12.9-5l-6-4.9c-2 1.5-4.4 2.4-6.9 2.4-5.3 0-9.7-3.4-11.3-8.1l-6.6 5.1C9.6 39 16.2 43.5 24 43.5z"/>
          <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.5l6 4.9c-.4.4 6.3-4.6 6.3-14.4 0-1.2-.1-2.3-.3-3.5z"/>
        </svg>
        Registrarse con Google
      </button>
      <p class="mt-4 text-center text-sm">
        ¿Ya tienes cuenta?
        <router-link to="/login" class="text-blue-600 hover:underline">Inicia sesión</router-link>
      </p>
    </form>
  </div>
</template>
