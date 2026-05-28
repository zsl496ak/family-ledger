import { defineStore } from 'pinia'
import { ref } from 'vue'
import { transactionApi } from '@/api/transactions'

export const useTransactionStore = defineStore('transaction', () => {
  const transactions = ref<any[]>([])
  const total = ref(0)
  const loading = ref(false)
  const summary = ref<any>(null)

  async function fetchTransactions(params: any = {}) {
    loading.value = true
    try {
      const { data } = await transactionApi.list(params)
      transactions.value = data.items
      total.value = data.total
    } finally {
      loading.value = false
    }
  }

  async function fetchSummary(params?: any) {
    const { data } = await transactionApi.summary(params)
    summary.value = data
  }

  async function createTransaction(data: any) {
    const res = await transactionApi.create(data)
    return res.data
  }

  async function updateTransaction(id: number, data: any) {
    const res = await transactionApi.update(id, data)
    return res.data
  }

  async function deleteTransaction(id: number) {
    await transactionApi.delete(id)
  }

  return { transactions, total, loading, summary, fetchTransactions, fetchSummary, createTransaction, updateTransaction, deleteTransaction }
})
