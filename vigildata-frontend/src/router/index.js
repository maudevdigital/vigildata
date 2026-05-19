import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

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
    meta: { requiereAuth: true },
  },
  {
    path: '/reportar',
    name: 'reportar',
    component: () => import('../views/ReportarView.vue'),
    meta: { requiereAuth: true },
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminView.vue'),
    meta: { requiereAuth: true, soloAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (to.meta.requiereAuth) {
    if (!auth.estaAutenticado) {
      return { name: 'login' }
    }
    const sesionValida = await auth.verificarSesion()
    if (!sesionValida) {
      return { name: 'login', query: { sesion: 'expirada' } }
    }
  }

  if (to.meta.soloAdmin && !auth.esAdmin) {
    return { name: 'mapa' }
  }
})

export default router
