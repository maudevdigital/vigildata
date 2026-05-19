<script setup>
import { onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useIncidentesStore } from '../stores/incidentesStore'
<<<<<<< Updated upstream
import { parseFechaIncidenteGmt4 } from '../utils/fechaIncidente'

const incidentesStore = useIncidentesStore()
const mapContainer = ref(null)
=======
import { regionesData } from '../utils/regiones'
import IncidenteResumen from '../components/IncidenteResumen.vue'

const incidentesStore = useIncidentesStore()
const mapContainer = ref(null)
const region = ref('')
const comuna = ref('')
const nivelRiesgo = ref('')
const fechaInicio = ref('')
const fechaFin = ref('')
const cargando = ref(false)
const error = ref('')
let map = null
let markersLayer = null

const regionesOrdenadas = computed(() => {
  return [...regionesData].sort((a, b) => a.nombre.localeCompare(b.nombre))
})

const comunasDisponibles = computed(() => {
  if (!region.value) return []
  const reg = regionesData.find((r) => r.nombre === region.value)
  return reg ? [...reg.comunas].sort((a, b) => a.localeCompare(b)) : []
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

function obtenerIconoRiesgo(nivel) {
  let color = '#22c55e' // Default / Bajo (verde)
  if (nivel === 'Medio') color = '#eab308' // amarillo
  else if (nivel === 'Alto') color = '#ef4444' // rojo
  
  const svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${color}" width="32" height="32" stroke="white" stroke-width="1.5" style="filter: drop-shadow(0px 2px 2px rgba(0,0,0,0.5));">
    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
  </svg>`;

  return L.divIcon({
    className: 'custom-div-icon',
    html: svgIcon,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  })
}

function actualizarMarcadores(incidentes) {
  if (!markersLayer) return
  markersLayer.clearLayers()
  incidentes.forEach((inc) => {
    if (inc.estado !== 'aprobado') return

    const regionTexto = inc.region || 'Sin región'
    const comunaTexto = inc.comuna || 'Sin comuna'
    const fechaTexto = inc.fecha ? new Date(inc.fecha).toLocaleString() : 'Sin fecha'
    const riesgoTexto = inc.nivel_riesgo ? `Riesgo: ${inc.nivel_riesgo}` : 'Riesgo: No especificado'

    L.marker([inc.latitud, inc.longitud], { icon: obtenerIconoRiesgo(inc.nivel_riesgo) })
      .addTo(markersLayer)
      .bindPopup(
        `<strong>${inc.tipo}</strong><br>${riesgoTexto}<br>${inc.descripcion}<br><small>${fechaTexto}</small><br><small>${regionTexto} - ${comunaTexto}</small>`
      )
  })
}

async function cargarIncidentes(params = {}) {
  cargando.value = true
  error.value = ''
  try {
    await Promise.all([
      incidentesStore.cargar(params),
      incidentesStore.cargarResumen(params),
    ])
    actualizarMarcadores(incidentesStore.incidentes)
  } catch (e) {
    error.value = e.response?.data?.detail || 'No se pudieron cargar los incidentes'
  } finally {
    cargando.value = false
  }
}

function construirFiltros() {
  const params = { estado: 'aprobado' }
  if (region.value) {
    params.region = region.value
  }
  if (comuna.value) {
    params.comuna = comuna.value
  }
  if (nivelRiesgo.value) {
    params.nivel_riesgo = nivelRiesgo.value
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
  nivelRiesgo.value = ''
  fechaInicio.value = ''
  fechaFin.value = ''
  await cargarIncidentes()
}
>>>>>>> Stashed changes

onMounted(async () => {
  const map = L.map(mapContainer.value).setView([-33.45, -70.65], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map)

  await incidentesStore.cargar()

  incidentesStore.incidentes.forEach((inc) => {
    L.marker([inc.latitud, inc.longitud])
      .addTo(map)
      .bindPopup(
          `<strong>${inc.tipo}</strong><br>${inc.descripcion}` +
            (inc.comuna ? `<br><em>${inc.comuna}</em>` : '') +
            `<br><small>${parseFechaIncidenteGmt4(inc.fecha).toLocaleString('es-CL')}</small>`,
        )
  })
})
</script>

<template>
<<<<<<< Updated upstream
  <div ref="mapContainer" class="w-full" style="height: calc(100vh - 56px)"></div>
=======
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
            <option v-for="r in regionesOrdenadas" :key="r.nombre" :value="r.nombre">{{ r.nombre }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium mb-1">Comuna</label>
          <select v-model="comuna" :disabled="!region" class="w-full border rounded px-3 py-2 text-sm disabled:bg-gray-100">
            <option value="">Todas las comunas</option>
            <option v-for="c in comunasDisponibles" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium mb-1">Nivel de riesgo</label>
          <select v-model="nivelRiesgo" class="w-full border rounded px-3 py-2 text-sm">
            <option value="">Todos los niveles</option>
            <option value="Bajo">Bajo</option>
            <option value="Medio">Medio</option>
            <option value="Alto">Alto</option>
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
    <IncidenteResumen :resumen="incidentesStore.resumen" :cargando="cargando" />
  </div>
>>>>>>> Stashed changes
</template>
