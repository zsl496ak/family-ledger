import http from './http'

export const categoryApi = {
  list: (type?: string) => http.get('/categories', { params: { category_type: type } }),
  create: (data: any) => http.post('/categories', data),
  update: (id: number, data: any) => http.put(`/categories/${id}`, data),
  delete: (id: number) => http.delete(`/categories/${id}`),
}
