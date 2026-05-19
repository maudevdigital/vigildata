<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  resumen: {
    type: Object,
    default: () => ({ total: 0, por_comuna: [], por_tipo: [] }),
  },
  cargando: { type: Boolean, default: false },
})

const expandido = ref(true)

function maxTotal(items) {
  if (!items.length) return 1
  return Math.max(...items.map((i) => i.total))
}

function porcentaje(total, max) {
  return Math.round((total / max) * 100)
}

const maxComuna = computed(() => maxTotal(props.resumen.por_comuna))
const maxTipo = computed(() => maxTotal(props.resumen.por_tipo))
</script>

<template>
  <div
    class="absolute z-[1000] bottom-4 left-4 w-[calc(100%-2rem)] sm:w-[calc(100%-28rem)] md:w-80 lg:w-96 bg-white/95 backdrop-blur rounded-lg shadow"
  >
    <button
      type="button"
      class="w-full flex items-center justify-between px-4 py-3 text-left"
      @click="expandido = !expandido"
      :aria-expanded="expandido"
    >
      <div>
        <h3 class="font-semibold text-sm">Resumen de incidentes</h3>
        <p class="text-xs text-gray-500 mt-0.5">
          <span v-if="cargando">Actualizando...</span>
          <span v-else>{{ resumen.total }} incidente{{ resumen.total === 1 ? '' : 's' }}</span>
        </p>
      </div>
      <span class="text-gray-400 text-xs ml-2 shrink-0">{{ expandido ? '▲' : '▼' }}</span>
    </button>

    <div v-show="expandido" class="px-4 pb-4 border-t border-gray-100">
      <div v-if="cargando" class="py-6 text-center text-xs text-gray-500">Cargando resumen...</div>

      <div v-else-if="resumen.total === 0" class="py-4 text-center text-xs text-gray-500">
        No hay incidentes con los filtros actuales.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3 max-h-48 md:max-h-56 overflow-y-auto">
        <section>
          <h4 class="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide">Por comuna</h4>
          <ul class="space-y-2">
            <li v-for="item in resumen.por_comuna" :key="'c-' + item.etiqueta">
              <div class="flex justify-between text-xs mb-0.5">
                <span class="truncate pr-2" :title="item.etiqueta">{{ item.etiqueta }}</span>
                <span class="font-medium shrink-0">{{ item.total }}</span>
              </div>
              <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  class="h-full bg-red-500 rounded-full transition-all"
                  :style="{ width: porcentaje(item.total, maxComuna) + '%' }"
                ></div>
              </div>
            </li>
          </ul>
        </section>

        <section>
          <h4 class="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide">Por tipo</h4>
          <ul class="space-y-2">
            <li v-for="item in resumen.por_tipo" :key="'t-' + item.etiqueta">
              <div class="flex justify-between text-xs mb-0.5">
                <span class="truncate pr-2" :title="item.etiqueta">{{ item.etiqueta }}</span>
                <span class="font-medium shrink-0">{{ item.total }}</span>
              </div>
              <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  class="h-full bg-amber-500 rounded-full transition-all"
                  :style="{ width: porcentaje(item.total, maxTipo) + '%' }"
                ></div>
              </div>
            </li>
          </ul>
        </section>
      </div>
    </div>
  </div>
</template>
