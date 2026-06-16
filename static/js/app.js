const API = (() => {
  const BASE = '/api';
  let refreshInterval = null;

  function getToken() { return localStorage.getItem('access_token'); }
  function getRefresh() { return localStorage.getItem('refresh_token'); }
  function getUser() { return JSON.parse(localStorage.getItem('user') || 'null'); }
  function setUser(u) { localStorage.setItem('user', JSON.stringify(u)); }
  function isAuth() { return !!getToken(); }

  async function request(url, options = {}) {
    const config = {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    };
    const token = getToken();
    if (token) config.headers['Authorization'] = `Bearer ${token}`;
    if (config.body && typeof config.body === 'object') config.body = JSON.stringify(config.body);
    const res = await fetch(BASE + url, config);
    if (res.status === 401 && getRefresh()) {
      const refreshed = await refreshToken();
      if (refreshed) {
        config.headers['Authorization'] = `Bearer ${getToken()}`;
        const retry = await fetch(BASE + url, config);
        return retry.json();
      }
      logout();
      window.location.href = '/login/';
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || err.message || 'Erreur serveur');
    }
    return res.json();
  }

  async function refreshToken() {
    try {
      const res = await fetch(BASE + '/auth/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: getRefresh() }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      localStorage.setItem('access_token', data.access);
      return true;
    } catch { return false; }
  }

  function startTokenRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(async () => {
      if (isAuth()) await refreshToken();
    }, 55 * 60 * 1000);
  }
  function stopTokenRefresh() { if (refreshInterval) { clearInterval(refreshInterval); refreshInterval = null; } }

  async function login(username, password) {
    const data = await request('/auth/login/', {
      method: 'POST',
      body: { username, password },
    });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    const profile = await request('/auth/profile/');
    setUser(profile);
    startTokenRefresh();
    return profile;
  }

  async function register(data) {
    const res = await request('/auth/register/', {
      method: 'POST',
      body: data,
      headers: { 'Content-Type': 'application/json' },
    });
    return res;
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    stopTokenRefresh();
  }

  async function getProfile() { return request('/auth/profile/'); }
  async function updateProfile(data) { return request('/auth/profile/', { method: 'PUT', body: data }); }

  async function getCredits(params = '') { return request('/credits/' + params); }
  async function createCredit(data) { return request('/credits/', { method: 'POST', body: data }); }
  async function getCredit(id) { return request(`/credits/${id}/`); }
  async function updateCreditStatus(id, data) { return request(`/credits/${id}/statut/`, { method: 'PATCH', body: data }); }
  async function getEcheances(id) { return request(`/credits/${id}/echeancier/`); }

  async function getRepaymentEcheances(params = '') { return request('/remboursements/echeances/' + params); }
  async function getRepaymentHistory(params = '') { return request('/remboursements/historique/' + params); }
  async function createPaiement(data) { return request('/remboursements/', { method: 'POST', body: data }); }

  async function getFormules() { return request('/assurances/formules/'); }
  async function souscrire(data) { return request('/assurances/souscrire/', { method: 'POST', body: data }); }
  async function getMesPolices() { return request('/assurances/mes-polices/'); }
  async function resilier(id) { return request(`/assurances/${id}/resilier/`, { method: 'PATCH', body: {} }); }

  async function getConversations() { return request('/chat/conversations/'); }
  async function createConversation() { return request('/chat/conversations/', { method: 'POST', body: {} }); }
  async function getMessages(id) { return request(`/chat/conversations/${id}/messages/`); }
  async function getAgents() { return request('/chat/agents/'); }

  async function getNotifications() { return request('/notifications/'); }
  async function markNotifRead(id) { return request(`/notifications/${id}/lire/`, { method: 'PATCH', body: {} }); }
  async function markAllRead() { return request('/notifications/lire-tout/', { method: 'PATCH', body: {} }); }

  async function getDashboardStats(params = '') { return request('/dashboard/stats/' + params); }

  function connectChat(conversationId, onMessage, onTyping, onPresence) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${conversationId}/`);
    ws.onopen = () => console.log('Chat WS connected');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'typing' && onTyping) onTyping(data);
      else if (data.type === 'stop_typing' && onTyping) onTyping(data);
      else if (data.type === 'presence' && onPresence) onPresence(data);
      else if (onMessage) onMessage(data);
    };
    ws.onclose = () => console.log('Chat WS disconnected');
    return ws;
  }

  function sendChatMessage(ws, contenu) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'message', contenu }));
    }
  }

  function sendTyping(ws, conversationId) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'typing', conversation_id: conversationId }));
    }
  }

  function sendStopTyping(ws, conversationId) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'stop_typing', conversation_id: conversationId }));
    }
  }

  return {
    isAuth, getUser, setUser, login, register, logout,
    getProfile, updateProfile,
    getCredits, createCredit, getCredit, updateCreditStatus, getEcheances,
    getRepaymentEcheances, getRepaymentHistory, createPaiement,
    getFormules, souscrire, getMesPolices, resilier,
    getConversations, createConversation, getMessages, getAgents,
    getNotifications, markNotifRead, markAllRead,
    getDashboardStats,
    connectChat, sendChatMessage, sendTyping, sendStopTyping,
    startTokenRefresh,
  };
})();

function $(id) { return document.getElementById(id); }
function formatMoney(n) { return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'XOF', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(n); }
function formatDate(d) { return new Date(d).toLocaleDateString('fr-FR'); }
function formatDateTime(d) { return new Date(d).toLocaleString('fr-FR'); }
function statutBadge(s) { return `<span class="status-badge status-${s}">${s.replace(/_/g, ' ')}</span>`; }
function presenceDot(online) { return `<span class="presence-dot ${online ? 'online' : 'offline'}"></span>`; }
function escapeHtml(text) {
  const d = document.createElement('div');
  d.textContent = text;
  return d.innerHTML;
}
