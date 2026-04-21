<script setup>
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'

const auth = useAuthStore()
const router = useRouter()

function cerrarSesion() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-blue-700 text-white px-6 py-3 flex items-center justify-between">
      <router-link to="/" class="text-xl font-bold">VigilData</router-link>

      <div class="flex items-center space-x-4 text-sm">
        <template v-if="auth.estaAutenticado">
          <router-link to="/mapa" class="hover:underline">Mapa</router-link>
          <router-link to="/reportar" class="hover:underline">Reportar</router-link>
          <router-link v-if="auth.esAdmin" to="/admin" class="hover:underline font-semibold text-yellow-300">
            Panel Admin
          </router-link>
          <span class="text-blue-200">{{ auth.usuario?.email }}</span>
          <button @click="cerrarSesion" class="bg-blue-900 hover:bg-blue-800 px-3 py-1 rounded">
            Salir
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="hover:underline">Ingresar</router-link>
          <router-link to="/registro" class="bg-white text-blue-700 px-3 py-1 rounded font-medium hover:bg-blue-50">
            Registrarse
          </router-link>
        </template>
      </div>
    </nav>
    <RouterView />
  </div>
</template>
