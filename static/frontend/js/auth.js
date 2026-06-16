const API_BASE = 'http://127.0.0.1:8000';

function getToken() {
  return localStorage.getItem('access_token');
}

function getRefresh() {
  return localStorage.getItem('refresh_token');
}

function saveTokens(access, refresh) {
  localStorage.setItem('access_token', access);
  if (refresh) localStorage.setItem('refresh_token', refresh);
}

function saveUserData(data) {
  localStorage.setItem('username', data.username || data.user?.username || '');
  localStorage.setItem('role', data.role || data.user?.role || '');
  localStorage.setItem('user_id', data.id || data.user?.id || '');
}

function getUserName() {
  return localStorage.getItem('username') || 'Utilisateur';
}

function getUserRole() {
  return localStorage.getItem('role') || '';
}

function getUserId() {
  return localStorage.getItem('user_id') || '';
}

function logout() {
  localStorage.clear();
  window.location.href = '/static/frontend/index.html';
}

function checkAuth() {
  if (!getToken()) {
    window.location.href = '/static/frontend/index.html';
  }
}

async function refreshToken() {
  const refresh = getRefresh();
  if (!refresh) {
    logout();
    return null;
  }

  try {
    const response = await fetch(`${API_BASE}/api/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });

    if (!response.ok) {
      logout();
      return null;
    }

    const data = await response.json();
    saveTokens(data.access, data.refresh || refresh);
    return data.access;
  } catch (error) {
    logout();
    return null;
  }
}

async function login(username, password) {
  const response = await fetch(`${API_BASE}/api/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || err.non_field_errors?.[0] || 'Identifiants invalides');
  }

  const data = await response.json();
  saveTokens(data.access, data.refresh);

  const profileResponse = await fetch(`${API_BASE}/api/auth/profile/`, {
    headers: { 'Authorization': `Bearer ${data.access}` }
  });

  if (profileResponse.ok) {
    const profile = await profileResponse.json();
    saveUserData(profile);
  }

  return data;
}

async function register(userData) {
  const response = await fetch(`${API_BASE}/api/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    const messages = [];
    if (err.username) messages.push(err.username[0]);
    if (err.email) messages.push(err.email[0]);
    if (err.password) messages.push(err.password[0]);
    if (err.phone) messages.push(err.phone[0]);
    if (err.non_field_errors) messages.push(err.non_field_errors[0]);
    throw new Error(messages.join('. ') || "Erreur lors de l'inscription");
  }

  return await response.json();
}

function redirectByRole(role) {
  switch (role?.toUpperCase()) {
    case 'CLIENT':
      window.location.href = '/static/frontend/dashboard_client.html';
      break;
    case 'ADMIN':
    case 'AGENT':
      window.location.href = '/static/frontend/dashboard_admin.html';
      break;
    default:
      window.location.href = '/static/frontend/dashboard_client.html';
  }
}
