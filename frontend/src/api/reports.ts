import http from './http'

export const reportApi = {
  monthly: (year: number, month: number) => http.get('/reports/monthly', { params: { year, month } }),
  yearly: (year: number) => http.get('/reports/yearly', { params: { year } }),
  categoryBreakdown: (year: number, month: number, type?: string) =>
    http.get('/reports/category-breakdown', { params: { year, month, transaction_type: type } }),
  trend: (year: number) => http.get('/reports/trend', { params: { year } }),
  accountBalances: () => http.get('/reports/account-balances'),
}
