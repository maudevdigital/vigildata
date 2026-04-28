<script setup>
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
})
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-2">Panel de Administración</h1>
    <p class="text-gray-500 mb-6">Vista exclusiva para analistas — Sprint 1</p>

    <div v-if="error" class="bg-red-100 text-red-700 p-3 rounded mb-4">{{ error }}</div>

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
    </div>
  </div>
</template>
