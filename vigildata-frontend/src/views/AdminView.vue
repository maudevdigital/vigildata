<script setup>
<<<<<<< Updated upstream
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { parseFechaIncidenteGmt4 } from '../utils/fechaIncidente'

const incidentes = ref([])
const error = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/incidentes/')
    incidentes.value = res.data
  } catch (e) {
    error.value = 'No se pudieron cargar los incidentes'
  }
=======
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useIncidentesStore } from '../stores/incidentesStore'

const incidentesStore = useIncidentesStore()
const auth = useAuthStore()
const error = ref('')
const mensaje = ref('')
const procesandoId = ref(null)

const pendientes = computed(() =>
  incidentesStore.incidentes.filter((i) => !i.estado || i.estado === 'pendiente')
)
const aprobados = computed(() => incidentesStore.incidentes.filter((i) => i.estado === 'aprobado'))
const rechazados = computed(() => incidentesStore.incidentes.filter((i) => i.estado === 'rechazado'))

function formatearFecha(valor) {
  if (!valor) return '—'
  return new Date(valor).toLocaleString('es-CL')
}

function etiquetaEstado(estado) {
  if (!estado || estado === 'pendiente') return 'Pendiente'
  if (estado === 'aprobado') return 'Aprobado'
  if (estado === 'rechazado') return 'Rechazado'
  return estado
}

async function cargarIncidentes() {
  error.value = ''
  try {
    await incidentesStore.cargar({ estado: 'todos' })
  } catch {
    error.value = 'No se pudieron cargar los incidentes'
  }
}

async function cambiarEstado(id, nuevoEstado) {
  mensaje.value = ''
  error.value = ''
  procesandoId.value = id
  try {
    const actualizado = await incidentesStore.cambiarEstado(id, nuevoEstado)
    mensaje.value = `Incidente #${id} marcado como ${etiquetaEstado(nuevoEstado).toLowerCase()} por ${actualizado.revisado_por_email || auth.usuario?.email}`
  } catch (e) {
    error.value = e.response?.data?.detail || 'No se pudo cambiar el estado'
  } finally {
    procesandoId.value = null
  }
}

async function eliminarIncidente(id) {
  if (!confirm('¿Estás seguro de que quieres eliminar este reporte?')) return
  mensaje.value = ''
  error.value = ''
  procesandoId.value = id
  try {
    await incidentesStore.eliminar(id)
    mensaje.value = `Incidente #${id} eliminado`
  } catch (e) {
    error.value = e.response?.data?.detail || 'No se pudo eliminar el incidente'
  } finally {
    procesandoId.value = null
  }
}

onMounted(() => {
  cargarIncidentes()
>>>>>>> Stashed changes
})
</script>

<template>
<<<<<<< Updated upstream
  <div class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-2">Panel de Administración</h1>
    <p class="text-gray-500 mb-6">Vista exclusiva para analistas — Sprint 1</p>
=======
  <div class="max-w-7xl mx-auto px-4 py-6 md:py-8">
    <h1 class="text-2xl md:text-3xl font-bold mb-2">Panel de moderación</h1>
    <p class="text-gray-500 mb-4 text-sm md:text-base">
      Revisa los reportes antes de publicarlos en el mapa. Solo los incidentes <strong>aprobados</strong> se muestran
      como activos.
    </p>
>>>>>>> Stashed changes

    <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{{ error }}</div>
    <div v-if="mensaje" class="bg-green-100 text-green-800 p-3 rounded mb-4 text-sm">{{ mensaje }}</div>

<<<<<<< Updated upstream
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="px-6 py-4 border-b flex items-center justify-between">
        <h2 class="font-semibold text-lg">Incidentes reportados</h2>
        <span class="text-sm text-gray-500">{{ incidentes.length }} total</span>
      </div>

      <div v-if="incidentes.length === 0" class="p-6 text-center text-gray-400">
        No hay incidentes registrados aún.
      </div>

      <table v-else class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
          <tr>
            <th class="px-4 py-3 text-left">#</th>
            <th class="px-4 py-3 text-left">Tipo</th>
            <th class="px-4 py-3 text-left">Comuna</th>
            <th class="px-4 py-3 text-left">Descripción</th>
            <th class="px-4 py-3 text-left">Fecha</th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="inc in incidentes" :key="inc.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-gray-400">{{ inc.id }}</td>
            <td class="px-4 py-3 font-medium">{{ inc.tipo }}</td>
            <td class="px-4 py-3">{{ inc.comuna || '—' }}</td>
            <td class="px-4 py-3 text-gray-600 max-w-xs truncate">{{ inc.descripcion }}</td>
            <td class="px-4 py-3 text-gray-500">{{ parseFechaIncidenteGmt4(inc.fecha).toLocaleString('es-CL') }}</td>
          </tr>
        </tbody>
      </table>
=======
    <!-- Pendientes -->
    <section class="bg-white rounded-lg shadow overflow-hidden mb-8 border border-yellow-200">
      <div class="px-4 md:px-6 py-4 border-b bg-yellow-50 flex items-center justify-between">
        <h2 class="font-semibold text-base md:text-lg text-yellow-800">Pendientes de revisión</h2>
        <span class="text-sm text-yellow-700">{{ pendientes.length }}</span>
      </div>
      <div v-if="pendientes.length === 0" class="p-6 text-center text-gray-400 text-sm">
        No hay incidentes pendientes.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm min-w-[640px]">
          <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
              <th class="px-3 py-3 text-left">#</th>
              <th class="px-3 py-3 text-left">Tipo</th>
              <th class="px-3 py-3 text-left">Descripción</th>
              <th class="px-3 py-3 text-left">Comuna</th>
              <th class="px-3 py-3 text-left">Reportado</th>
              <th class="px-3 py-3 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr v-for="inc in pendientes" :key="inc.id" class="hover:bg-gray-50 align-top">
              <td class="px-3 py-3 text-gray-400">{{ inc.id }}</td>
              <td class="px-3 py-3 font-medium">{{ inc.tipo }}</td>
              <td class="px-3 py-3 text-gray-600 max-w-[200px]">{{ inc.descripcion }}</td>
              <td class="px-3 py-3 text-gray-600">{{ inc.comuna || '—' }}</td>
              <td class="px-3 py-3 text-gray-500 text-xs whitespace-nowrap">{{ formatearFecha(inc.fecha) }}</td>
              <td class="px-3 py-3 text-right space-x-2 whitespace-nowrap">
                <button
                  :disabled="procesandoId === inc.id"
                  class="text-green-600 hover:text-green-800 text-sm font-medium disabled:opacity-50"
                  @click="cambiarEstado(inc.id, 'aprobado')"
                >
                  Aprobar
                </button>
                <button
                  :disabled="procesandoId === inc.id"
                  class="text-orange-600 hover:text-orange-800 text-sm font-medium disabled:opacity-50"
                  @click="cambiarEstado(inc.id, 'rechazado')"
                >
                  Rechazar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
      <!-- Aprobados -->
      <section class="bg-white rounded-lg shadow overflow-hidden border border-green-200">
        <div class="px-4 md:px-6 py-4 border-b bg-green-50 flex items-center justify-between">
          <h2 class="font-semibold text-base md:text-lg text-green-800">Aprobados (visibles en mapa)</h2>
          <span class="text-sm text-green-700">{{ aprobados.length }}</span>
        </div>
        <div v-if="aprobados.length === 0" class="p-6 text-center text-gray-400 text-sm">Ningún incidente aprobado.</div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm min-w-[520px]">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-3 py-3 text-left">Tipo</th>
                <th class="px-3 py-3 text-left">Revisado por</th>
                <th class="px-3 py-3 text-left">Fecha revisión</th>
                <th class="px-3 py-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="inc in aprobados" :key="inc.id" class="hover:bg-gray-50">
                <td class="px-3 py-3 font-medium">{{ inc.tipo }}</td>
                <td class="px-3 py-3 text-gray-600 text-xs">{{ inc.revisado_por_email || '—' }}</td>
                <td class="px-3 py-3 text-gray-500 text-xs whitespace-nowrap">{{ formatearFecha(inc.fecha_revision) }}</td>
                <td class="px-3 py-3 text-right space-x-2 whitespace-nowrap">
                  <button
                    :disabled="procesandoId === inc.id"
                    class="text-amber-600 hover:text-amber-800 text-sm font-medium disabled:opacity-50"
                    @click="cambiarEstado(inc.id, 'pendiente')"
                  >
                    Pendiente
                  </button>
                  <button
                    :disabled="procesandoId === inc.id"
                    class="text-orange-600 hover:text-orange-800 text-sm font-medium disabled:opacity-50"
                    @click="cambiarEstado(inc.id, 'rechazado')"
                  >
                    Rechazar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Rechazados -->
      <section class="bg-white rounded-lg shadow overflow-hidden border border-gray-300">
        <div class="px-4 md:px-6 py-4 border-b bg-gray-100 flex items-center justify-between">
          <h2 class="font-semibold text-base md:text-lg text-gray-700">Rechazados (ocultos del mapa)</h2>
          <span class="text-sm text-gray-600">{{ rechazados.length }}</span>
        </div>
        <div v-if="rechazados.length === 0" class="p-6 text-center text-gray-400 text-sm">Ningún incidente rechazado.</div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm min-w-[520px]">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-3 py-3 text-left">Tipo</th>
                <th class="px-3 py-3 text-left">Rechazado por</th>
                <th class="px-3 py-3 text-left">Fecha revisión</th>
                <th class="px-3 py-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="inc in rechazados" :key="inc.id" class="hover:bg-gray-50">
                <td class="px-3 py-3 font-medium">{{ inc.tipo }}</td>
                <td class="px-3 py-3 text-gray-600 text-xs">{{ inc.revisado_por_email || '—' }}</td>
                <td class="px-3 py-3 text-gray-500 text-xs whitespace-nowrap">{{ formatearFecha(inc.fecha_revision) }}</td>
                <td class="px-3 py-3 text-right space-x-2 whitespace-nowrap">
                  <button
                    :disabled="procesandoId === inc.id"
                    class="text-green-600 hover:text-green-800 text-sm font-medium disabled:opacity-50"
                    @click="cambiarEstado(inc.id, 'aprobado')"
                  >
                    Aprobar
                  </button>
                  <button
                    :disabled="procesandoId === inc.id"
                    class="text-amber-600 hover:text-amber-800 text-sm font-medium disabled:opacity-50"
                    @click="cambiarEstado(inc.id, 'pendiente')"
                  >
                    Pendiente
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
>>>>>>> Stashed changes
    </div>
  </div>
</template>
