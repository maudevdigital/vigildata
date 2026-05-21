<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/authStore'
import { useIncidentesStore } from '../stores/incidentesStore'

const incidentesStore = useIncidentesStore()
const error = ref('')
const auth = useAuthStore()

const pendientes = computed(() => incidentesStore.incidentes.filter(i => !i.estado || i.estado === 'pendiente'))
const aprobados = computed(() => incidentesStore.incidentes.filter(i => i.estado === 'aprobado'))
const rechazados = computed(() => incidentesStore.incidentes.filter(i => i.estado === 'rechazado'))

async function cargarIncidentes() {
  try {
    await incidentesStore.cargar({ estado: 'todos' })
  } catch (e) {
    error.value = 'No se pudieron cargar los incidentes'
  }
}

async function cambiarEstado(id, nuevoEstado) {
  try {
    await incidentesStore.cambiarEstado(id, nuevoEstado)
  } catch (e) {
    alert(e.response?.data?.detail || 'No se pudo cambiar el estado')
  }
}

async function eliminarIncidente(id) {
  if (!confirm('¿Estás seguro de que quieres eliminar este reporte?')) return
  try {
    await incidentesStore.eliminar(id)
  } catch (e) {
    alert(e.response?.data?.detail || 'No se pudo eliminar el incidente')
  }
}

onMounted(() => {
  cargarIncidentes()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-2">Panel de Administración</h1>
    <p class="text-gray-500 mb-6">Revisión de incidentes reportados</p>

    <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>

    <!-- Pendientes -->
    <div class="bg-white rounded-lg shadow overflow-hidden mb-8 border border-yellow-200">
      <div class="px-6 py-4 border-b bg-yellow-50 flex items-center justify-between">
        <h2 class="font-semibold text-lg text-yellow-800">Incidentes reportados (pendientes)</h2>
        <span class="text-sm text-yellow-700">{{ pendientes.length }} total</span>
      </div>
      <div v-if="pendientes.length === 0" class="p-6 text-center text-gray-400">
        No hay incidentes pendientes de revisión.
      </div>
      <div v-if="pendientes.length > 0" class="vigil-admin-cards p-3">
        <div v-for="inc in pendientes" :key="'card-'+inc.id" class="border rounded-lg p-3 bg-white shadow-sm">
          <div class="flex justify-between items-start">
            <div>
              <div class="font-semibold text-sm">#{{ inc.id }} · {{ inc.tipo }}</div>
              <div class="text-xs text-gray-600">{{ inc.comuna || '—' }} · Riesgo: {{ inc.nivel_riesgo || '—' }}</div>
              <div class="text-xs text-gray-400 mt-1">{{ new Date(inc.fecha).toLocaleString('es-CL') }}</div>
            </div>
          </div>
          <div v-if="auth.esAdmin" class="grid grid-cols-3 gap-2 mt-3">
            <button @click="cambiarEstado(inc.id, 'aprobado')" class="bg-green-600 text-white py-2 rounded text-xs touch-target">Aprobar</button>
            <button @click="cambiarEstado(inc.id, 'rechazado')" class="bg-orange-500 text-white py-2 rounded text-xs touch-target">Rechazar</button>
            <button @click="eliminarIncidente(inc.id)" class="bg-red-600 text-white py-2 rounded text-xs touch-target">Borrar</button>
          </div>
        </div>
      </div>
      <table v-if="pendientes.length > 0" class="w-full text-sm vigil-admin-table">
        <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
          <tr>
            <th class="px-4 py-3 text-left">#</th>
            <th class="px-4 py-3 text-left">Tipo</th>
            <th class="px-4 py-3 text-left">Riesgo</th>
            <th class="px-4 py-3 text-left">Comuna</th>
            <th class="px-4 py-3 text-left">Fecha</th>
            <th v-if="auth.esAdmin" class="px-4 py-3 text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="inc in pendientes" :key="inc.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-gray-400">{{ inc.id }}</td>
            <td class="px-4 py-3 font-medium">{{ inc.tipo }}</td>
            <td class="px-4 py-3">{{ inc.nivel_riesgo || '—' }}</td>
            <td class="px-4 py-3 text-gray-600 max-w-xs truncate">{{ inc.comuna || '—' }}</td>
            <td class="px-4 py-3 text-gray-500">{{ new Date(inc.fecha).toLocaleString('es-CL') }}</td>
            <td v-if="auth.esAdmin" class="px-4 py-3 text-right space-x-2">
              <button @click="cambiarEstado(inc.id, 'aprobado')" class="text-green-600 hover:text-green-800 text-sm font-medium">Aprobar</button>
              <button @click="cambiarEstado(inc.id, 'rechazado')" class="text-orange-500 hover:text-orange-700 text-sm font-medium">Rechazar</button>
              <button @click="eliminarIncidente(inc.id)" class="text-red-500 hover:text-red-700 text-sm font-medium">Borrar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Aprobados -->
      <div class="bg-white rounded-lg shadow overflow-hidden border border-green-200">
        <div class="px-6 py-4 border-b bg-green-50 flex items-center justify-between">
          <h2 class="font-semibold text-lg text-green-800">Incidentes aceptados</h2>
          <span class="text-sm text-green-700">{{ aprobados.length }} total</span>
        </div>
        <div v-if="aprobados.length === 0" class="p-6 text-center text-gray-400">
          No hay incidentes aprobados.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-4 py-3 text-left">Aceptado por</th>
                <th class="px-4 py-3 text-left">Tipo</th>
                <th class="px-4 py-3 text-left">Comuna</th>
                <th v-if="auth.esAdmin" class="px-4 py-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="inc in aprobados" :key="inc.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-gray-500 text-xs">{{ inc.revisado_por_email || '—' }}</td>
                <td class="px-4 py-3 font-medium">{{ inc.tipo }}</td>
                <td class="px-4 py-3 text-gray-600">{{ inc.comuna || '—' }}</td>
                <td v-if="auth.esAdmin" class="px-4 py-3 text-right space-x-2">
                  <button @click="cambiarEstado(inc.id, 'rechazado')" class="text-orange-500 hover:text-orange-700 text-sm font-medium">Rechazar</button>
                  <button @click="eliminarIncidente(inc.id)" class="text-red-500 hover:text-red-700 text-sm font-medium">Borrar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Rechazados -->
      <div class="bg-white rounded-lg shadow overflow-hidden border border-gray-300">
        <div class="px-6 py-4 border-b bg-gray-100 flex items-center justify-between">
          <h2 class="font-semibold text-lg text-gray-700">Incidentes rechazados</h2>
          <span class="text-sm text-gray-600">{{ rechazados.length }} total</span>
        </div>
        <div v-if="rechazados.length === 0" class="p-6 text-center text-gray-400">
          No hay incidentes rechazados.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-4 py-3 text-left">Rechazado por</th>
                <th class="px-4 py-3 text-left">Tipo</th>
                <th class="px-4 py-3 text-left">Comuna</th>
                <th v-if="auth.esAdmin" class="px-4 py-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="inc in rechazados" :key="inc.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-gray-500 text-xs">{{ inc.revisado_por_email || '—' }}</td>
                <td class="px-4 py-3 font-medium">{{ inc.tipo }}</td>
                <td class="px-4 py-3 text-gray-600">{{ inc.comuna || '—' }}</td>
                <td v-if="auth.esAdmin" class="px-4 py-3 text-right space-x-2">
                  <button @click="cambiarEstado(inc.id, 'aprobado')" class="text-green-600 hover:text-green-800 text-sm font-medium">Aprobar</button>
                  <button @click="eliminarIncidente(inc.id)" class="text-red-500 hover:text-red-700 text-sm font-medium">Borrar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
