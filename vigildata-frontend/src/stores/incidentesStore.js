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

  return { incidentes, cargar, crear }
})
