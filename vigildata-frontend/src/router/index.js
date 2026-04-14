import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/registro',
    name: 'registro',
    component: () => import('../views/RegistroView.vue'),
  },
  {
    path: '/mapa',
    name: 'mapa',
    component: () => import('../views/MapaView.vue'),
  },
  {
    path: '/reportar',
    name: 'reportar',
    component: () => import('../views/ReportarView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
