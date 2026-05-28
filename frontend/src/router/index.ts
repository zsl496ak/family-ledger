import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/components/layout/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
        { path: 'transactions', name: 'Transactions', component: () => import('@/views/Transactions.vue') },
        { path: 'accounts', name: 'Accounts', component: () => import('@/views/Accounts.vue') },
        { path: 'budgets', name: 'Budgets', component: () => import('@/views/Budgets.vue') },
        { path: 'reports', name: 'Reports', component: () => import('@/views/Reports.vue') },
        { path: 'settings', name: 'Settings', component: () => import('@/views/Settings.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    return { name: 'Login' }
  }
  if (!to.meta.requiresAuth && auth.token && (to.name === 'Login' || to.name === 'Register')) {
    return { name: 'Dashboard' }
  }
})

export default router
