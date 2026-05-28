import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const user = ref<any>(null)

  const isLoggedIn = computed(() => !!token.value)

  function setTokens(access: string, refresh: string) {
    token.value = access
    refreshToken.value = refresh
    localStorage.setItem('token', access)
    localStorage.setItem('refreshToken', refresh)
  }

  async function login(email: string, password: string) {
    const { data } = await authApi.login(email, password)
    setTokens(data.access_token, data.refresh_token)
    await fetchUser()
  }

  async function register(data: any) {
    const res = await authApi.register(data)
    setTokens(res.data.access_token, res.data.refresh_token)
    await fetchUser()
  }

  async function registerJoin(data: any) {
    const res = await authApi.registerJoin(data)
    setTokens(res.data.access_token, res.data.refresh_token)
    await fetchUser()
  }

  async function fetchUser() {
    try {
      const { data } = await authApi.getMe()
      user.value = data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }

  // Auto-fetch user on store init
  if (token.value) {
    fetchUser()
  }

  return { token, refreshToken, user, isLoggedIn, setTokens, login, register, registerJoin, fetchUser, logout }
})
