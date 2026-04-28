<script setup>
import { onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useIncidentesStore } from '../stores/incidentesStore'
import { parseFechaIncidenteGmt4 } from '../utils/fechaIncidente'

const incidentesStore = useIncidentesStore()
const mapContainer = ref(null)

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
  <div ref="mapContainer" class="w-full" style="height: calc(100vh - 56px)"></div>
</template>
