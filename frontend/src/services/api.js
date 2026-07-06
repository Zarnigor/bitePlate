import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT token if present
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('access_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// ── Tables ─────────────────────────────────────────────────
export const tablesApi = {
  list:         ()           => api.get('/tables/'),
  create:       (data)       => api.post('/tables/', data),
  setStatus:    (id, action) => api.post(`/tables/${id}/${action}`),
}

// ── Reservations ───────────────────────────────────────────
export const reservationsApi = {
  list:   (date) => api.get('/reservations/', { params: date ? { date } : {} }),
  create: (data) => api.post('/reservations/', data),
  arrive: (id)   => api.post(`/reservations/${id}/arrive`),
}

// ── Orders ─────────────────────────────────────────────────
export const ordersApi = {
  list:    ()       => api.get('/orders/'),
  get:     (id)     => api.get(`/orders/${id}`),
  create:  (data)   => api.post('/orders/', data),
  confirm: (id, staffId) => api.post(`/orders/${id}/confirm`, {}, { headers: { 'x-staff-id': staffId } }),
  cancel:  (id, staffId) => api.post(`/orders/${id}/cancel`, {}, { headers: { 'x-staff-id': staffId } }),
  served:  (id)     => api.post(`/orders/${id}/served`),
  history: ()       => api.get('/orders/history/summary'),
  allHistory: ()    => api.get('/orders/history/all'),
}

// ── Kitchen ────────────────────────────────────────────────
export const kitchenApi = {
  queue:     ()   => api.get('/kitchen/queue'),
  prepare:   (id) => api.post(`/kitchen/tickets/${id}/prepare`),
  ready:     (id) => api.post(`/kitchen/tickets/${id}/ready`),
  cancel:    (id) => api.post(`/kitchen/tickets/${id}/cancel`),
  undoLast:  ()   => api.post('/kitchen/undo'),
}

// ── Menu ───────────────────────────────────────────────────
export const menuApi = {
  list:             ()     => api.get('/menu/items'),
  create:           (data) => api.post('/menu/items', data),
  toggleAvailable:  (id)   => api.patch(`/menu/items/${id}/availability`),
  customise:        (id, data) => api.post(`/menu/items/${id}/customise`, data),
  listCombos:       ()     => api.get('/menu/combos'),
  createCombo:      (data) => api.post('/menu/combos', data),
}

// ── Billing ────────────────────────────────────────────────
export const billingApi = {
  generate:   (orderId, data) => api.post(`/billing/generate/${orderId}`, data),
  pay:        (billId)        => api.post(`/billing/pay/${billId}`),
  strategies: ()              => api.get('/billing/strategies'),
}

export default api
