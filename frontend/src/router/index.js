import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/main.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: HomeView
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
