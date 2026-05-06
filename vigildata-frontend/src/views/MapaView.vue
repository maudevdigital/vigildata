<script setup>
import { onMounted, ref, computed } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useIncidentesStore } from '../stores/incidentesStore'
import { regionesData } from '../utils/regiones'

const incidentesStore = useIncidentesStore()
const mapContainer = ref(null)
const region = ref('')
const comuna = ref('')
const fechaInicio = ref('')
const fechaFin = ref('')
const cargando = ref(false)
const error = ref('')
let map = null
let markersLayer = null

const comunasDisponibles = computed(() => {
  if (!region.value) return []
  const reg = regionesData.find((r) => r.nombre === region.value)
  return reg ? reg.comunas : []
})

function onRegionChange() {
  comuna.value = ''
}

function normalizarFechaInicio(valor) {
  if (!valor) return null
  return `${valor}T00:00:00`
}

function normalizarFechaFin(valor) {
  if (!valor) return null
  return `${valor}T23:59:59`
}

function actualizarMarcadores(incidentes) {
  if (!markersLayer) return
  markersLayer.clearLayers()
  incidentes.forEach((inc) => {
    const regionTexto = inc.region || 'Sin región'
    const comunaTexto = inc.comuna || 'Sin comuna'
    const fechaTexto = inc.fecha ? new Date(inc.fecha).toLocaleString() : 'Sin fecha'
    L.marker([inc.latitud, inc.longitud])
      .addTo(markersLayer)
      .bindPopup(
        `<strong>${inc.tipo}</strong><br>${inc.descripcion}<br><small>${fechaTexto}</small><br><small>${regionTexto} - ${comunaTexto}</small>`
      )
  })
}

async function cargarIncidentes(params = {}) {
  cargando.value = true
  error.value = ''
  try {
    await incidentesStore.cargar(params)
    actualizarMarcadores(incidentesStore.incidentes)
  } catch (e) {
    error.value = e.response?.data?.detail || 'No se pudieron cargar los incidentes'
  } finally {
    cargando.value = false
  }
}

function construirFiltros() {
  const params = {}
  if (region.value) {
    params.region = region.value
  }
  if (comuna.value) {
    params.comuna = comuna.value
  }
  const inicio = normalizarFechaInicio(fechaInicio.value)
  const fin = normalizarFechaFin(fechaFin.value)
  if (inicio) params.fecha_inicio = inicio
  if (fin) params.fecha_fin = fin
  return params
}

async function aplicarFiltros() {
  await cargarIncidentes(construirFiltros())
}

async function limpiarFiltros() {
  region.value = ''
  comuna.value = ''
  fechaInicio.value = ''
  fechaFin.value = ''
  await cargarIncidentes()
}

onMounted(async () => {
  map = L.map(mapContainer.value).setView([-35.6751, -71.543], 5)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)

  await cargarIncidentes()
})
</script>

<template>
  <div class="relative w-full" style="height: calc(100dvh - 56px); min-height: 360px">
    <div ref="mapContainer" class="w-full h-full"></div>
    <div
      class="absolute z-[1000] top-4 right-4 w-[calc(100%-4rem)] md:w-96 bg-white/95 backdrop-blur rounded-lg shadow p-4"
    >
      <h3 class="font-semibold text-sm mb-3">Filtrar incidentes</h3>
      <div v-if="error" class="bg-red-100 text-red-700 p-2 rounded mb-3 text-xs">{{ error }}</div>
      <div class="grid grid-cols-1 gap-3">
        <div>
          <label class="block text-xs font-medium mb-1">Región</label>
          <select v-model="region" @change="onRegionChange" class="w-full border rounded px-3 py-2 text-sm">
            <option value="">Todas las regiones</option>
            <option v-for="r in regionesData" :key="r.nombre" :value="r.nombre">{{ r.nombre }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium mb-1">Comuna</label>
          <select v-model="comuna" :disabled="!region" class="w-full border rounded px-3 py-2 text-sm disabled:bg-gray-100">
            <option value="">Todas las comunas</option>
            <option v-for="c in comunasDisponibles" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium mb-1">Fecha inicio</label>
            <input v-model="fechaInicio" type="date" class="w-full border rounded px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Fecha fin</label>
            <input v-model="fechaFin" type="date" class="w-full border rounded px-3 py-2 text-sm" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <button
            type="button"
            class="w-full bg-red-600 text-white py-2 rounded text-sm hover:bg-red-700 disabled:opacity-60"
            :disabled="cargando"
            @click="aplicarFiltros"
          >
            {{ cargando ? 'Aplicando...' : 'Aplicar filtros' }}
          </button>
          <button
            type="button"
            class="w-full border border-gray-300 text-gray-700 py-2 rounded text-sm hover:bg-gray-50"
            :disabled="cargando"
            @click="limpiarFiltros"
          >
            Limpiar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
