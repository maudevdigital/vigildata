<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useIncidentesStore } from '../stores/incidentesStore'
import { regionesData } from '../utils/regiones'

const router = useRouter()
const store = useIncidentesStore()

const tipo = ref('')
const descripcion = ref('')
const latitud = ref('')
const longitud = ref('')
const region = ref('')
const comuna = ref('')
const error = ref('')
const exito = ref(false)
const ubicacionCargando = ref(false)

const tipos = ['Robo', 'Asalto', 'Vandalismo', 'Iluminación deficiente', 'Accidente', 'Otro']

const comunasDisponibles = computed(() => {
  if (!region.value) return []
  const reg = regionesData.find((r) => r.nombre === region.value)
  return reg ? reg.comunas : []
})

function onRegionChange() {
  comuna.value = ''
}

function solicitarUbicacion() {
  if (!navigator.geolocation) {
    return Promise.reject(new Error('Geolocalización no disponible en este navegador'))
  }

  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
    })
  })
}

async function handleObtenerUbicacion() {
  error.value = ''
  ubicacionCargando.value = true
  try {
    const pos = await solicitarUbicacion()
    latitud.value = pos.coords.latitude.toFixed(6)
    longitud.value = pos.coords.longitude.toFixed(6)
  } catch (e) {
    error.value = e.message || 'No se pudo obtener la ubicación'
  } finally {
    ubicacionCargando.value = false
  }
}

async function handleReportar() {
  error.value = ''
  exito.value = false
  try {
    if (!latitud.value || !longitud.value) {
      const pos = await solicitarUbicacion()
      latitud.value = pos.coords.latitude.toFixed(6)
      longitud.value = pos.coords.longitude.toFixed(6)
    }

    const lat = Number.parseFloat(latitud.value)
    const lon = Number.parseFloat(longitud.value)

    if (Number.isNaN(lat) || Number.isNaN(lon)) {
      throw new Error('Latitud y longitud deben ser números válidos')
    }

    await store.crear({
      tipo: tipo.value,
      descripcion: descripcion.value,
      latitud: lat,
      longitud: lon,
      region: region.value || null,
      comuna: comuna.value || null,
    })

    exito.value = true
    setTimeout(() => router.push('/mapa'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Error al reportar'
  }
}
</script>

<template>
  <div class="flex justify-center mt-10">
    <form @submit.prevent="handleReportar" class="bg-white p-8 rounded-lg shadow-md w-96">
      <h2 class="text-2xl font-bold mb-6 text-center">Reportar Incidente</h2>
      <div v-if="error" class="bg-red-100 text-red-700 p-2 rounded mb-4 text-sm">{{ error }}</div>
      <div v-if="exito" class="bg-green-100 text-green-700 p-2 rounded mb-4 text-sm">
        Incidente reportado. Redirigiendo al mapa...
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Tipo de incidente</label>
        <select v-model="tipo" required class="w-full border rounded px-3 py-2">
          <option value="" disabled>Selecciona un tipo</option>
          <option v-for="t in tipos" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium mb-1">Descripción</label>
        <textarea v-model="descripcion" required rows="3" class="w-full border rounded px-3 py-2"></textarea>
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Región</label>
        <select v-model="region" @change="onRegionChange" class="w-full border rounded px-3 py-2">
          <option value="" disabled>Selecciona una región</option>
          <option v-for="r in regionesData" :key="r.nombre" :value="r.nombre">{{ r.nombre }}</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Comuna</label>
        <select v-model="comuna" :disabled="!region" class="w-full border rounded px-3 py-2 disabled:bg-gray-100">
          <option value="" disabled>Selecciona una comuna</option>
          <option v-for="c in comunasDisponibles" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Latitud</label>
        <input
          v-model="latitud"
          type="number"
          step="0.000001"
          class="w-full border rounded px-3 py-2"
          placeholder="Ej: -33.45"
        />
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium mb-1">Longitud</label>
        <input
          v-model="longitud"
          type="number"
          step="0.000001"
          class="w-full border rounded px-3 py-2"
          placeholder="Ej: -70.65"
        />
      </div>
      <div class="mb-4">
        <button
          type="button"
          class="w-full border border-red-600 text-red-600 py-2 rounded hover:bg-red-50"
          :disabled="ubicacionCargando"
          @click="handleObtenerUbicacion"
        >
          {{ ubicacionCargando ? 'Obteniendo ubicación...' : 'Obtener ubicación automáticamente' }}
        </button>
      </div>
      <p class="text-xs text-gray-500 mb-4">
        La ubicación GPS puede completarse automáticamente o ingresarse manualmente.
      </p>
      <button type="submit" class="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700">
        Reportar
      </button>
    </form>
  </div>
</template>
