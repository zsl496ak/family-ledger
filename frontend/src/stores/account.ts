import { defineStore } from 'pinia'
import { ref } from 'vue'
import { accountApi } from '@/api/accounts'

export const useAccountStore = defineStore('account', () => {
  const accounts = ref<any[]>([])
  const loading = ref(false)

  async function fetchAccounts() {
    loading.value = true
    try {
      const { data } = await accountApi.list()
      accounts.value = data
    } finally {
      loading.value = false
    }
  }

  async function createAccount(data: any) {
    const res = await accountApi.create(data)
    await fetchAccounts()
    return res.data
  }

  async function updateAccount(id: number, data: any) {
    const res = await accountApi.update(id, data)
    await fetchAccounts()
    return res.data
  }

  async function deleteAccount(id: number) {
    await accountApi.delete(id)
    await fetchAccounts()
  }

  return { accounts, loading, fetchAccounts, createAccount, updateAccount, deleteAccount }
})
