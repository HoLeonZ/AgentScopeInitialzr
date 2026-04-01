import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
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
