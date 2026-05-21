<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import api from '../services/api'

const auth = useAuthStore()
const stats = ref({ total: 0, por_comuna: [], por_tipo: [] })
const cargando = ref(true)

onMounted(async () => {
  try {
    const r = await api.get('/incidentes/resumen', { params: { estado: 'todos' } })
    stats.value = r.data
  } catch {
    /* sin datos */
  } finally {
    cargando.value = false
  }
})
</script>

<template>
  <div class="min-h-[calc(100vh-64px)]">
    <!-- Hero -->
    <section
      class="relative overflow-hidden bg-gradient-to-br from-blue-700 via-blue-600 to-indigo-700 text-white"
    >
      <div class="absolute inset-0 opacity-20 pointer-events-none" aria-hidden="true">
        <svg class="w-full h-full" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
          <circle cx="100" cy="120" r="3" fill="#fff"/>
          <circle cx="300" cy="80" r="4" fill="#fff"/>
          <circle cx="600" cy="200" r="5" fill="#fff"/>
          <circle cx="500" cy="450" r="3" fill="#fff"/>
          <circle cx="200" cy="500" r="4" fill="#fff"/>
          <circle cx="700" cy="380" r="3" fill="#fff"/>
          <path d="M100 120 L300 80 L600 200 L500 450 L200 500 Z" stroke="#fff" stroke-width="1" fill="none" stroke-dasharray="4 6"/>
        </svg>
      </div>

      <div class="relative max-w-5xl mx-auto px-4 sm:px-6 py-12 sm:py-20 text-center">
        <span class="inline-block bg-white/15 backdrop-blur px-3 py-1 rounded-full text-xs font-medium tracking-wide uppercase mb-4">
          Seguridad ciudadana colaborativa
        </span>
        <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight">
          VigilData
        </h1>
        <p class="mt-4 text-base sm:text-xl text-blue-50 max-w-2xl mx-auto">
          Reporta, visualiza y comprende los incidentes de tu comuna en un mapa colaborativo en tiempo real.
        </p>

        <div class="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
          <router-link
            to="/mapa"
            class="bg-white text-blue-700 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition touch-target shadow-lg"
          >
            Ver mapa
          </router-link>
          <router-link
            v-if="!auth.estaAutenticado"
            to="/login"
            class="bg-blue-900/60 backdrop-blur border border-white/30 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-900 transition touch-target"
          >
            Iniciar sesión
          </router-link>
          <router-link
            v-else
            to="/reportar"
            class="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition touch-target shadow-lg"
          >
            Reportar incidente
          </router-link>
        </div>

        <!-- Mini stats -->
        <div class="mt-10 grid grid-cols-3 gap-3 max-w-2xl mx-auto">
          <div class="bg-white/10 backdrop-blur rounded-lg px-3 py-4">
            <div class="text-2xl sm:text-3xl font-bold">{{ cargando ? '…' : stats.total }}</div>
            <div class="text-xs text-blue-100 mt-1">Incidentes registrados</div>
          </div>
          <div class="bg-white/10 backdrop-blur rounded-lg px-3 py-4">
            <div class="text-2xl sm:text-3xl font-bold">{{ cargando ? '…' : stats.por_comuna.length }}</div>
            <div class="text-xs text-blue-100 mt-1">Comunas con reportes</div>
          </div>
          <div class="bg-white/10 backdrop-blur rounded-lg px-3 py-4">
            <div class="text-2xl sm:text-3xl font-bold">{{ cargando ? '…' : stats.por_tipo.length }}</div>
            <div class="text-xs text-blue-100 mt-1">Tipos de incidente</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <h2 class="text-2xl sm:text-3xl font-bold text-center text-gray-800 mb-2">
        ¿Cómo funciona?
      </h2>
      <p class="text-center text-gray-500 mb-10 text-sm sm:text-base">
        Tres pasos para que tu comuna sea más segura.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition">
          <div class="w-12 h-12 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
          </div>
          <h3 class="font-semibold text-lg mb-2">1. Reporta</h3>
          <p class="text-sm text-gray-600">
            Toca el mapa donde ocurrió el incidente, elige tipo y nivel de riesgo, y describe lo que viste.
          </p>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition">
          <div class="w-12 h-12 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
          </div>
          <h3 class="font-semibold text-lg mb-2">2. Validamos</h3>
          <p class="text-sm text-gray-600">
            Un modelo BERT detecta reportes repetidos y los consolida automáticamente. Los analistas revisan el resto.
          </p>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition">
          <div class="w-12 h-12 rounded-lg bg-green-100 text-green-700 flex items-center justify-center mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
          </div>
          <h3 class="font-semibold text-lg mb-2">3. Visualiza</h3>
          <p class="text-sm text-gray-600">
            Filtra por comuna, fecha y nivel de riesgo. Ve los resúmenes y entiende dónde concentrarte.
          </p>
        </div>
      </div>
    </section>

    <!-- Top comunas -->
    <section v-if="!cargando && stats.por_comuna.length" class="max-w-6xl mx-auto px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 class="font-semibold text-lg mb-4 text-gray-800">Top comunas con reportes</h3>
        <div class="space-y-3">
          <div
            v-for="(c, i) in stats.por_comuna.slice(0, 5)"
            :key="c.etiqueta"
            class="flex items-center gap-3"
          >
            <span class="w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-xs flex items-center justify-center font-bold">{{ i + 1 }}</span>
            <span class="flex-1 text-sm text-gray-700 truncate">{{ c.etiqueta }}</span>
            <div class="flex-1 max-w-[200px] h-2 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-blue-500 to-indigo-500" :style="{ width: (c.total / stats.por_comuna[0].total * 100) + '%' }"></div>
            </div>
            <span class="text-sm font-medium text-gray-600 w-8 text-right">{{ c.total }}</span>
          </div>
        </div>
        <router-link to="/mapa" class="mt-4 inline-block text-sm text-blue-600 hover:underline">
          Ver detalle completo en el mapa →
        </router-link>
      </div>
    </section>

    <!-- Footer mini -->
    <footer class="border-t border-gray-200 bg-white">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-6 text-xs text-gray-500 flex flex-col sm:flex-row justify-between gap-2">
        <span>VigilData · Proyecto Ingeniería de Software · UNAB 2026</span>
        <span>Hito 2 · Sprint 3</span>
      </div>
    </footer>
  </div>
</template>
