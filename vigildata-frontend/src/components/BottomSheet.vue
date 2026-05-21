<script setup>
// HU-11 - Bottom sheet reutilizable para filtros y acciones en movil.
// Cierra con swipe down, backdrop tap, o boton X. Soporta safe-area.
import { ref, watch } from 'vue'

const props = defineProps({
  abierto: { type: Boolean, default: false },
  titulo: { type: String, default: '' },
})
const emit = defineEmits(['update:abierto'])

const startY = ref(null)
const offsetY = ref(0)
const sheet = ref(null)

function cerrar() { emit('update:abierto', false) }

function onTouchStart(e) { startY.value = e.touches[0].clientY; offsetY.value = 0 }
function onTouchMove(e) {
  if (startY.value == null) return
  const dy = e.touches[0].clientY - startY.value
  offsetY.value = Math.max(0, dy)
}
function onTouchEnd() {
  if (offsetY.value > 80) cerrar()
  startY.value = null
  offsetY.value = 0
}

watch(() => props.abierto, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
})
</script>

<template>
  <transition name="bs-fade">
    <div v-if="abierto" class="fixed inset-0 z-[1800] bg-black/40" @click="cerrar"></div>
  </transition>
  <transition name="bs-slide">
    <div
      v-if="abierto"
      ref="sheet"
      class="fixed left-0 right-0 bottom-0 z-[1900] bg-white rounded-t-2xl shadow-2xl"
      :style="{ transform: `translateY(${offsetY}px)`, paddingBottom: 'max(1rem, env(safe-area-inset-bottom))' }"
      @touchstart="onTouchStart"
      @touchmove="onTouchMove"
      @touchend="onTouchEnd"
    >
      <div class="flex justify-center pt-2"><span class="block w-10 h-1.5 rounded-full bg-gray-300"></span></div>
      <div class="flex items-center justify-between px-4 py-2">
        <h3 class="font-semibold text-sm">{{ titulo }}</h3>
        <button class="text-gray-500 touch-target" @click="cerrar" aria-label="Cerrar">✕</button>
      </div>
      <div class="px-4 pb-3 max-h-[70vh] overflow-y-auto">
        <slot />
      </div>
    </div>
  </transition>
</template>

<style scoped>
.bs-fade-enter-active, .bs-fade-leave-active { transition: opacity .2s ease; }
.bs-fade-enter-from, .bs-fade-leave-to { opacity: 0; }
.bs-slide-enter-active, .bs-slide-leave-active { transition: transform .25s ease; }
.bs-slide-enter-from, .bs-slide-leave-to { transform: translateY(100%) !important; }
</style>
