import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/configure',
      name: 'configure',
      component: () => import('../views/Configure.vue')
    },
    {
      path: '/skills',
      name: 'skills',
      component: () => import('../views/SkillManagement.vue')
    }
  ]
})

export default router
