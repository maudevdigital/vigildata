<script setup>
import { ref } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'

const auth = useAuthStore()
const router = useRouter()
const menuAbierto = ref(false)

function cerrarSesion() {
  auth.logout()
  menuAbierto.value = false
  router.push('/login')
}

function navegar(ruta) {
  menuAbierto.value = false
  router.push(ruta)
}
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-blue-700 text-white relative" style="padding-top: env(safe-area-inset-top)">
      <div class="px-4 sm:px-6 py-3 flex items-center justify-between gap-2">
        <router-link to="/" class="text-lg sm:text-xl font-bold shrink-0">VigilData</router-link>

        <!-- Desktop -->
        <div class="hidden md:flex items-center space-x-4 text-sm">
          <template v-if="auth.estaAutenticado">
            <router-link to="/mapa" class="hover:underline">Mapa</router-link>
            <!-- <router-link to="/reportar" class="hover:underline">Reportar</router-link> -->
            <router-link v-if="auth.esAdmin" to="/admin" class="hover:underline font-semibold text-yellow-300">
              Panel Admin
            </router-link>
            <span class="text-blue-200 max-w-[180px] truncate">{{ auth.usuario?.email }}</span>
            <button @click="cerrarSesion" class="bg-blue-900 hover:bg-blue-800 px-3 py-1 rounded touch-target">
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

        <!-- Burger -->
        <button
          class="md:hidden touch-target px-2 -mr-2 text-white"
          aria-label="Abrir menu"
          @click="menuAbierto = !menuAbierto"
        >
          <svg v-if="!menuAbierto" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
          <svg v-else width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Drawer mobile -->
      <transition name="nav-fade">
        <div
          v-if="menuAbierto"
          class="md:hidden absolute left-0 right-0 top-full bg-blue-700 border-t border-blue-600 shadow-lg z-[2100]"
        >
          <template v-if="auth.estaAutenticado">
            <div class="px-4 py-3 text-xs text-blue-200 truncate">{{ auth.usuario?.email }}</div>
            <button @click="navegar('/mapa')" class="block w-full text-left px-4 py-3 hover:bg-blue-800 touch-target">Mapa</button>
            <!-- <button @click="navegar('/reportar')" class="block w-full text-left px-4 py-3 hover:bg-blue-800 touch-target">Reportar</button> -->
            <button v-if="auth.esAdmin" @click="navegar('/admin')" class="block w-full text-left px-4 py-3 hover:bg-blue-800 font-semibold text-yellow-300 touch-target">Panel Admin</button>
            <button @click="cerrarSesion" class="block w-full text-left px-4 py-3 bg-blue-900 hover:bg-blue-800 touch-target">Salir</button>
          </template>
          <template v-else>
            <button @click="navegar('/login')" class="block w-full text-left px-4 py-3 hover:bg-blue-800 touch-target">Ingresar</button>
            <button @click="navegar('/registro')" class="block w-full text-left px-4 py-3 bg-white text-blue-700 font-medium touch-target">Registrarse</button>
          </template>
        </div>
      </transition>
    </nav>
    <RouterView />
  </div>
</template>

<style scoped>
.nav-fade-enter-active, .nav-fade-leave-active { transition: opacity .15s ease; }
.nav-fade-enter-from, .nav-fade-leave-to { opacity: 0; }
</style>
