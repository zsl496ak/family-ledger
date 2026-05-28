import { defineStore } from 'pinia'
import { ref } from 'vue'
import { categoryApi } from '@/api/categories'

export const useCategoryStore = defineStore('category', () => {
  const categories = ref<any[]>([])
  const loading = ref(false)

  async function fetchCategories(type?: string) {
    loading.value = true
    try {
      const { data } = await categoryApi.list(type)
      categories.value = data
    } finally {
      loading.value = false
    }
  }

  async function createCategory(data: any) {
    const res = await categoryApi.create(data)
    await fetchCategories()
    return res.data
  }

  async function updateCategory(id: number, data: any) {
    const res = await categoryApi.update(id, data)
    await fetchCategories()
    return res.data
  }

  async function deleteCategory(id: number) {
    await categoryApi.delete(id)
    await fetchCategories()
  }

  return { categories, loading, fetchCategories, createCategory, updateCategory, deleteCategory }
})
