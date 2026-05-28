import http from './http'

export const familyApi = {
  get: () => http.get('/family'),
  update: (data: any) => http.put('/family', data),
  regenerateInvite: () => http.post('/family/regenerate-invite'),
  members: () => http.get('/family/members'),
  updateRole: (userId: number, role: string) => http.put(`/family/members/${userId}/role`, { role }),
  removeMember: (userId: number) => http.delete(`/family/members/${userId}`),
}
