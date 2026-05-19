<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useIncidentesStore } from '../stores/incidentesStore'

const router = useRouter()
const store = useIncidentesStore()

const tipo = ref('')
const descripcion = ref('')
const comuna = ref('')
const error = ref('')
const exito = ref(false)
const ubicando = ref(false)
const enviando = ref(false)
/** @type {import('vue').Ref<{ lat: number; lng: number } | null>} */
const ubicacion = ref(null)

const tipos = ['Robo', 'Asalto', 'Vandalismo', 'Iluminación deficiente', 'Accidente', 'Otro']

const comunas = [
  'Cerrillos',
  'Cerro Navia',
  'Conchalí',
  'El Bosque',
  'Estación Central',
  'Huechuraba',
  'Independencia',
  'La Cisterna',
  'La Florida',
  'La Granja',
  'La Pintana',
  'La Reina',
  'Las Condes',
  'Lo Barnechea',
  'Lo Espejo',
  'Lo Prado',
  'Macul',
  'Maipú',
  'Ñuñoa',
  'Pedro Aguirre Cerda',
  'Peñalolén',
  'Providencia',
  'Pudahuel',
  'Puente Alto',
  'Quilicura',
  'Quinta Normal',
  'Recoleta',
  'Renca',
  'San Joaquín',
  'San Miguel',
  'San Ramón',
  'Santiago',
  'Vitacura',
]

/** Fecha y hora local del dispositivo en ISO 8601 con offset (p. ej. ...-04:00). */
function fechaHoraUsuarioISO() {
  const d = new Date()
  const pad = (n, z = 2) => String(n).padStart(z, '0')
  const yyyy = d.getFullYear()
  const mm = pad(d.getMonth() + 1)
  const dd = pad(d.getDate())
  const hh = pad(d.getHours())
  const mi = pad(d.getMinutes())
  const ss = pad(d.getSeconds())
  const offsetMin = -d.getTimezoneOffset()
  const sign = offsetMin >= 0 ? '+' : '-'
  const absMin = Math.abs(offsetMin)
  const oh = pad(Math.floor(absMin / 60))
  const om = pad(absMin % 60)
  return `${yyyy}-${mm}-${dd}T${hh}:${mi}:${ss}${sign}${oh}:${om}`
}

function mensajeErrorGeolocalizacion(code) {
  if (code === 1) return 'Permiso de ubicación denegado. Actívalo en el navegador.'
  if (code === 2) return 'No se pudo determinar la posición. Intenta de nuevo.'
  if (code === 3) return 'Tiempo de espera agotado al obtener GPS.'
  return 'No se pudo obtener la ubicación.'
}

function obtenerPosicion() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Tu navegador no soporta geolocalización.'))
      return
    }
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: true,
      timeout: 15000,
      maximumAge: 0,
    })
  })
}

async function capturarUbicacion() {
  error.value = ''
  ubicando.value = true
  try {
    const pos = await obtenerPosicion()
    ubicacion.value = {
      lat: pos.coords.latitude,
      lng: pos.coords.longitude,
    }
  } catch (e) {
    const code = e?.code
    error.value =
      typeof code === 'number'
        ? mensajeErrorGeolocalizacion(code)
        : e.message || 'Error al obtener GPS.'
    ubicacion.value = null
  } finally {
    ubicando.value = false
  }
}

async function handleReportar() {
  error.value = ''
  enviando.value = true
  try {
    let lat
    let lng
    if (ubicacion.value) {
      lat = ubicacion.value.lat
      lng = ubicacion.value.lng
    } else {
      const pos = await obtenerPosicion()
      lat = pos.coords.latitude
      lng = pos.coords.longitude
      ubicacion.value = { lat, lng }
    }

    await store.crear({
      tipo: tipo.value.trim(),
      descripcion: descripcion.value.trim(),
      comuna: comuna.value.trim(),
      latitud: lat,
      longitud: lng,
      fecha: fechaHoraUsuarioISO(),
    })

    exito.value = true
    setTimeout(() => router.push('/mapa'), 1500)
  } catch (e) {
<<<<<<< Updated upstream
    const detail = e.response?.data?.detail
    error.value = Array.isArray(detail)
      ? detail.map((x) => x.msg || x).join('. ')
      : detail || e.message || 'Error al reportar'
    if (typeof error.value === 'object') error.value = JSON.stringify(error.value)
  } finally {
    enviando.value = false
=======
    const detalle = e.response?.data?.detail
    if (e.response?.status === 401) {
      error.value = 'Sesi?n inv?lida o expirada. Cierra sesi?n, vuelve a iniciar sesi?n e intenta de nuevo.'
    } else {
      error.value = detalle || e.message || 'Error al reportar'
    }
>>>>>>> Stashed changes
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
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Descripción</label>
        <textarea v-model="descripcion" required rows="3" class="w-full border rounded px-3 py-2"></textarea>
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Comuna</label>
        <select v-model="comuna" required class="w-full border rounded px-3 py-2">
          <option value="" disabled>Selecciona comuna</option>
          <option v-for="c in comunas" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div class="mb-4 rounded border border-gray-200 bg-gray-50 p-3">
        <p class="text-sm font-medium text-gray-700 mb-2">Ubicación GPS</p>
        <button
          type="button"
          class="w-full border border-gray-300 bg-white py-2 rounded text-sm hover:bg-gray-100 disabled:opacity-50"
          :disabled="ubicando"
          @click="capturarUbicacion"
        >
          {{ ubicando ? 'Obteniendo ubicación…' : 'Obtener ubicación ahora' }}
        </button>
        <p v-if="ubicacion" class="mt-2 text-xs text-gray-600 font-mono">
          Lat {{ ubicacion.lat.toFixed(6) }}, Lon {{ ubicacion.lng.toFixed(6) }}
        </p>
        <p class="mt-2 text-xs text-gray-500">
          Si no pulsas el botón, al enviar el reporte se pedirá la ubicación automáticamente (Geolocation API).
        </p>
      </div>
      <button
        type="submit"
        class="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700 disabled:opacity-50"
        :disabled="enviando"
      >
        {{ enviando ? 'Enviando…' : 'Reportar' }}
      </button>
    </form>
  </div>
</template>
