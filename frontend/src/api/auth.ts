import http from './http'

export const authApi = {
  login: (email: string, password: string) =>
    http.post('/auth/login', { email, password }),
  register: (data: { username: string; email: string; password: string; family_name?: string }) =>
    http.post('/auth/register', data),
  registerJoin: (data: { username: string; email: string; password: string; invite_code: string }) =>
    http.post('/auth/register/join', data),
  refresh: (refreshToken: string) =>
    http.post('/auth/refresh', { refresh_token: refreshToken }),
  getMe: () => http.get('/auth/me'),
  updateMe: (data: any) => http.put('/auth/me', data),
  changePassword: (data: { old_password: string; new_password: string }) =>
    http.put('/auth/password', data),
}
