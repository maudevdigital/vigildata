<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'
import { useIncidentesStore } from '../stores/incidentesStore'
import { useAuthStore } from '../stores/authStore'
import { regionesData } from '../utils/regiones'
import IncidenteResumen from '../components/IncidenteResumen.vue'
import api from '../services/api'

const route = useRoute()
const auth = useAuthStore()
const incidentesStore = useIncidentesStore()

const tipos = ['Robo', 'Asalto', 'Vandalismo', 'Iluminación deficiente', 'Accidente', 'Otro']
const niveles = ['Bajo', 'Medio', 'Alto']

const modalAbierto = ref(false)
const enviando = ref(false)
const errorModal = ref('')
const nuevo = ref({ lat: 0, lon: 0, tipo: '', nivel_riesgo: 'Bajo', descripcion: '', region: '', comuna: '' })
const comunasNuevo = computed(() => {
  const r = regionesData.find((x) => x.nombre === nuevo.value.region)
  return r ? [...r.comunas].sort() : []
})

function abrirModalReporte(latlng) {
  if (!auth.estaAutenticado) {
    error.value = 'Tenés que iniciar sesión para reportar un incidente.'
    return
  }
  nuevo.value = { lat: latlng.lat, lon: latlng.lng, tipo: '', nivel_riesgo: 'Bajo', descripcion: '', region: '', comuna: '' }
  errorModal.value = ''
  modalAbierto.value = true
}

async function enviarReporte() {
  errorModal.value = ''
  enviando.value = true
  try {
    await incidentesStore.crear({
      tipo: nuevo.value.tipo,
      descripcion: nuevo.value.descripcion,
      latitud: nuevo.value.lat,
      longitud: nuevo.value.lon,
      region: nuevo.value.region || null,
      comuna: nuevo.value.comuna || null,
      nivel_riesgo: nuevo.value.nivel_riesgo,
    })
    modalAbierto.value = false
    await cargarIncidentes(construirFiltros())
    map.flyTo([nuevo.value.lat, nuevo.value.lon], Math.max(map.getZoom(), 15), { duration: 1.2 })
  } catch (e) {
    errorModal.value = e.response?.data?.detail || e.message || 'No se pudo crear el reporte'
  } finally {
    enviando.value = false
  }
}
const mapContainer = ref(null)
const region = ref('')
const comuna = ref('')
const nivelRiesgo = ref('')
const fechaInicio = ref('')
const fechaFin = ref('')
const cargando = ref(false)
const error = ref('')
const resumen = ref({ total: 0, por_comuna: [], por_tipo: [] })
let map = null
let markersLayer = null
let heatLayer = null
const heatmapActivo = ref(false)

const ICONOS_TIPO = {
  'Robo': '💰',
  'Asalto': '⚠️',
  'Vandalismo': '🔨',
  'Iluminación deficiente': '💡',
  'Accidente': '🚗',
  'Otro': '❗',
}

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

function obtenerIconoIncidente(tipo, nivel) {
  let color = '#22c55e'
  if (nivel === 'Medio') color = '#eab308'
  else if (nivel === 'Alto') color = '#ef4444'

  const emoji = ICONOS_TIPO[tipo] || '❗'
  const html = `
    <div style="position:relative;width:38px;height:46px;filter:drop-shadow(0 2px 3px rgba(0,0,0,0.4));">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 30" width="38" height="46" style="position:absolute;top:0;left:0;">
        <path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 18 12 18s12-9 12-18c0-6.6-5.4-12-12-12z" fill="${color}" stroke="white" stroke-width="1.5"/>
        <circle cx="12" cy="12" r="8" fill="white"/>
      </svg>
      <div style="position:absolute;top:3px;left:0;width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:18px;line-height:1;">${emoji}</div>
    </div>`

  return L.divIcon({
    className: 'vigildata-marker',
    html,
    iconSize: [38, 46],
    iconAnchor: [19, 46],
    popupAnchor: [0, -42],
  })
}

function actualizarHeatmap(incidentes) {
  if (!map) return
  if (heatLayer) {
    map.removeLayer(heatLayer)
    heatLayer = null
  }
  if (!heatmapActivo.value) return
  const pesos = { 'Bajo': 0.4, 'Medio': 0.7, 'Alto': 1.0 }
  const puntos = incidentes
    .filter((i) => i.estado !== 'rechazado')
    .map((i) => [i.latitud, i.longitud, pesos[i.nivel_riesgo] || 0.6])
  heatLayer = L.heatLayer(puntos, { radius: 35, blur: 25, maxZoom: 17 }).addTo(map)
}

function toggleHeatmap() {
  heatmapActivo.value = !heatmapActivo.value
  actualizarHeatmap(incidentesStore.incidentes)
}

function reportarEnCentro() {
  if (!map) return
  const c = map.getCenter()
  abrirModalReporte({ lat: c.lat, lng: c.lng })
}

function actualizarMarcadores(incidentes) {
  if (!markersLayer) return
  markersLayer.clearLayers()
  incidentes.forEach((inc) => {
    // Los rechazados no se muestran, aunque ya debería filtrarlos el backend
    if (inc.estado === 'rechazado') return

    const regionTexto = inc.region || 'Sin región'
    const comunaTexto = inc.comuna || 'Sin comuna'
    const fechaTexto = inc.fecha ? new Date(inc.fecha).toLocaleString() : 'Sin fecha'
    const riesgoTexto = inc.nivel_riesgo ? `Riesgo: ${inc.nivel_riesgo}` : 'Riesgo: No especificado'
    
    let estadoTexto = ''
    if (!inc.estado || inc.estado === 'pendiente') {
      estadoTexto = '<span style="color: #d97706; font-weight: bold;">(Pendiente de revisión)</span>'
    } else if (inc.estado === 'aprobado') {
      estadoTexto = '<span style="color: #16a34a; font-weight: bold;">(Aprobado)</span>'
    }

    L.marker([inc.latitud, inc.longitud], { icon: obtenerIconoIncidente(inc.tipo, inc.nivel_riesgo) })
      .addTo(markersLayer)
      .bindPopup(
        `<strong>${inc.tipo}</strong> ${estadoTexto}<br>${riesgoTexto}<br>${inc.descripcion}<br><small>${fechaTexto}</small><br><small>${regionTexto} - ${comunaTexto}</small>`
      )
  })
  actualizarHeatmap(incidentes)
}

async function cargarResumen(params = {}) {
  try {
    const res = await api.get('/incidentes/resumen', { params })
    resumen.value = res.data
  } catch (e) {
    resumen.value = { total: 0, por_comuna: [], por_tipo: [] }
  }
}

async function cargarIncidentes(params = {}) {
  cargando.value = true
  error.value = ''
  try {
    await Promise.all([
      incidentesStore.cargar(params),
      cargarResumen(params),
    ])
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

onMounted(async () => {
  map = L.map(mapContainer.value).setView([-35.6751, -71.543], 5)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)

  map.on('click', (e) => abrirModalReporte(e.latlng))

  await cargarIncidentes()

  const lat = Number.parseFloat(route.query.lat)
  const lon = Number.parseFloat(route.query.lon)
  if (Number.isFinite(lat) && Number.isFinite(lon)) {
    const zoom = Number.parseInt(route.query.zoom, 10) || 16
    map.flyTo([lat, lon], zoom, { duration: 1.2 })
  }
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
    <IncidenteResumen :resumen="resumen" :cargando="cargando" />

    <button
      type="button"
      class="absolute z-[1100] top-4 left-4 bg-white/95 backdrop-blur rounded-lg shadow px-3 py-2 text-sm font-medium hover:bg-white"
      @click="toggleHeatmap"
      :title="heatmapActivo ? 'Ocultar zonas calientes' : 'Mostrar zonas calientes'"
    >
      🔥 {{ heatmapActivo ? 'Ocultar heatmap' : 'Ver heatmap' }}
    </button>

    <button
      type="button"
      class="absolute z-[1100] bottom-6 right-6 w-16 h-16 rounded-full bg-red-600 text-white shadow-lg hover:bg-red-700 active:scale-95 transition flex items-center justify-center"
      @click="reportarEnCentro"
      title="Reportar incidente en el centro del mapa (o hacé click en cualquier punto)"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
        <path d="M12 5v14M5 12h14" stroke="white" stroke-width="3" stroke-linecap="round"/>
      </svg>
    </button>

    <div
      v-if="modalAbierto"
      class="absolute inset-0 z-[2000] bg-black/40 flex items-center justify-center p-4"
      @click.self="modalAbierto = false"
    >
      <form
        @submit.prevent="enviarReporte"
        class="bg-white rounded-lg shadow-xl w-full max-w-md p-5 max-h-[90vh] overflow-y-auto"
      >
        <h3 class="text-lg font-bold mb-1">Reportar incidente</h3>
        <p class="text-xs text-gray-500 mb-3">
          Ubicación: {{ nuevo.lat.toFixed(5) }}, {{ nuevo.lon.toFixed(5) }}
        </p>
        <div v-if="errorModal" class="bg-red-100 text-red-700 p-2 rounded mb-3 text-xs">{{ errorModal }}</div>
        <div class="space-y-3">
          <div>
            <label class="block text-xs font-medium mb-1">Tipo</label>
            <select v-model="nuevo.tipo" required class="w-full border rounded px-3 py-2 text-sm">
              <option value="" disabled>Selecciona...</option>
              <option v-for="t in tipos" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Nivel de riesgo</label>
            <select v-model="nuevo.nivel_riesgo" required class="w-full border rounded px-3 py-2 text-sm">
              <option v-for="n in niveles" :key="n" :value="n">{{ n }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Descripción</label>
            <textarea v-model="nuevo.descripcion" required rows="3" class="w-full border rounded px-3 py-2 text-sm"></textarea>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium mb-1">Región (opcional)</label>
              <select v-model="nuevo.region" @change="nuevo.comuna = ''" class="w-full border rounded px-2 py-2 text-sm">
                <option value="">—</option>
                <option v-for="r in regionesOrdenadas" :key="r.nombre" :value="r.nombre">{{ r.nombre }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Comuna</label>
              <select v-model="nuevo.comuna" :disabled="!nuevo.region" class="w-full border rounded px-2 py-2 text-sm disabled:bg-gray-100">
                <option value="">—</option>
                <option v-for="c in comunasNuevo" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="flex gap-2 mt-4">
          <button type="button" class="flex-1 border border-gray-300 text-gray-700 py-2 rounded text-sm hover:bg-gray-50" @click="modalAbierto = false" :disabled="enviando">
            Cancelar
          </button>
          <button type="submit" class="flex-1 bg-red-600 text-white py-2 rounded text-sm hover:bg-red-700 disabled:opacity-60" :disabled="enviando">
            {{ enviando ? 'Enviando...' : 'Reportar' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
