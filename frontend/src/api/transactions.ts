import http from './http'

export const transactionApi = {
  list: (params: any) => http.get('/transactions', { params }),
  create: (data: any) => http.post('/transactions', data),
  get: (id: number) => http.get(`/transactions/${id}`),
  update: (id: number, data: any) => http.put(`/transactions/${id}`, data),
  delete: (id: number) => http.delete(`/transactions/${id}`),
  summary: (params?: any) => http.get('/transactions/summary', { params }),
  export: (params: any) => http.post('/transactions/export', null, { params, responseType: 'blob' }),
  import: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return http.post('/transactions/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  downloadTemplate: () => http.get('/transactions/import/template', { responseType: 'blob' }),
}
