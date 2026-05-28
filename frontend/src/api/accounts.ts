import http from './http'

export const accountApi = {
  list: () => http.get('/accounts'),
  get: (id: number) => http.get(`/accounts/${id}`),
  create: (data: any) => http.post('/accounts', data),
  update: (id: number, data: any) => http.put(`/accounts/${id}`, data),
  delete: (id: number) => http.delete(`/accounts/${id}`),
}
