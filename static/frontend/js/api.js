async function apiFetch(endpoint, options = {}) {
  const token = getToken();
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    },
    ...options,
  };

  if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
    config.body = JSON.stringify(config.body);
  }

  if (config.body instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  let response = await fetch(`${API_BASE}${endpoint}`, config);

  if (response.status === 401 && token) {
    const newToken = await refreshToken();
    if (newToken) {
      config.headers['Authorization'] = `Bearer ${newToken}`;
      response = await fetch(`${API_BASE}${endpoint}`, config);
    } else {
      throw new Error('Session expirée. Veuillez vous reconnecter.');
    }
  }

  return response;
}

async function apiGet(endpoint) {
  const response = await apiFetch(endpoint, { method: 'GET' });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || err.message || `Erreur ${response.status}`);
  }
  const data = await response.json();
  if (data && Array.isArray(data.results)) {
    return data.results;
  }
  return data;
}

async function apiPost(endpoint, data) {
  const response = await apiFetch(endpoint, {
    method: 'POST',
    body: data,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    const msg = err.detail || err.message || Object.values(err).flat().join(', ') || `Erreur ${response.status}`;
    throw new Error(msg);
  }
  return await response.json();
}

async function apiPatch(endpoint, data) {
  const response = await apiFetch(endpoint, {
    method: 'PATCH',
    body: data,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    const msg = err.detail || err.message || Object.values(err).flat().join(', ') || `Erreur ${response.status}`;
    throw new Error(msg);
  }
  return await response.json();
}

async function apiPut(endpoint, data) {
  const response = await apiFetch(endpoint, {
    method: 'PUT',
    body: data,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    const msg = err.detail || err.message || Object.values(err).flat().join(', ') || `Erreur ${response.status}`;
    throw new Error(msg);
  }
  return await response.json();
}

async function apiDelete(endpoint) {
  const response = await apiFetch(endpoint, { method: 'DELETE' });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || err.message || `Erreur ${response.status}`);
  }
  return response.status === 204 ? null : await response.json();
}
