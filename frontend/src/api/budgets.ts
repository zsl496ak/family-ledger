import http from './http'

export const budgetApi = {
  list: (year: number, month: number) => http.get('/budgets', { params: { year, month } }),
  create: (data: any) => http.post('/budgets', data),
  update: (id: number, data: any) => http.put(`/budgets/${id}`, data),
  delete: (id: number) => http.delete(`/budgets/${id}`),
  overview: (year: number, month: number) => http.get('/budgets/overview', { params: { year, month } }),
}
