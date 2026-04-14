<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-blue-700 text-white px-6 py-3 flex items-center justify-between">
      <router-link to="/" class="text-xl font-bold">VigilData</router-link>
      <div class="space-x-4">
        <router-link to="/mapa" class="hover:underline">Mapa</router-link>
        <router-link to="/login" class="hover:underline">Ingresar</router-link>
      </div>
    </nav>
    <RouterView />
  </div>
</template>
