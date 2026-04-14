<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useIncidentesStore } from '../stores/incidentesStore'

const router = useRouter()
const store = useIncidentesStore()

const tipo = ref('')
const descripcion = ref('')
const error = ref('')
const exito = ref(false)

const tipos = ['Robo', 'Asalto', 'Vandalismo', 'Iluminación deficiente', 'Accidente', 'Otro']

async function handleReportar() {
  error.value = ''
  try {
    const pos = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject)
    })

    await store.crear({
      tipo: tipo.value,
      descripcion: descripcion.value,
      latitud: pos.coords.latitude,
      longitud: pos.coords.longitude,
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
      <p class="text-xs text-gray-500 mb-4">La ubicación GPS se capturará automáticamente.</p>
      <button type="submit" class="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700">
        Reportar
      </button>
    </form>
  </div>
</template>
