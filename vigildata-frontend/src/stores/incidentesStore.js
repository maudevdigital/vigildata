import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useIncidentesStore = defineStore('incidentes', () => {
  const incidentes = ref([])

  async function cargar(params = {}) {
    const res = await api.get('/incidentes', { params })
    incidentes.value = res.data
  }

  async function crear(data) {
    const res = await api.post('/incidentes/', data)
    incidentes.value.unshift(res.data)
    return res.data
  }

  async function cambiarEstado(id, estado) {
    const res = await api.patch(`/incidentes/${id}/estado`, { estado })
    const idx = incidentes.value.findIndex(i => i.id === id)
    if (idx !== -1) {
      incidentes.value[idx] = res.data
    }
    return res.data
  }

  async function eliminar(id) {
    await api.delete(`/incidentes/${id}`)
    incidentes.value = incidentes.value.filter(i => i.id !== id)
  }

  return { incidentes, cargar, crear, cambiarEstado, eliminar }
})
