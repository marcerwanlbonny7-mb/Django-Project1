function formatCurrency(amount) {
  return new Intl.NumberFormat('fr-CI', {
    style: 'currency',
    currency: 'XOF',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount || 0);
}

function formatDate(dateStr) {
  if (!dateStr) return '-';
  try {
    return new Date(dateStr).toLocaleDateString('fr-CI', {
      day: '2-digit', month: 'short', year: 'numeric',
    });
  } catch { return dateStr; }
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-';
  try {
    return new Date(dateStr).toLocaleDateString('fr-CI', {
      day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
    });
  } catch { return dateStr; }
}

function statutClass(statut) {
  const map = {
    'SOUMISE': 'statut-soumise', 'EN_ANALYSE': 'statut-en_analyse',
    'APPROUVEE': 'statut-approuvee', 'DECAISSEE': 'statut-decaissee', 'REJETEE': 'statut-rejetee',
    'ACTIVE': 'statut-active', 'EXPIREE': 'statut-expiree', 'RESILIEE': 'statut-resiliee',
    'EN_ATTENTE': 'statut-en_attente', 'PAYEE': 'statut-payee', 'EN_RETARD': 'statut-en_retard',
    'OUVERTE': 'statut-ouverte', 'EN_COURS': 'statut-en_cours', 'FERMEE': 'statut-fermee',
  };
  return map[statut] || 'statut-soumise';
}

function statutLabel(statut) {
  const map = {
    'SOUMISE': 'Soumise', 'EN_ANALYSE': 'En analyse', 'APPROUVEE': 'Approuvée',
    'DECAISSEE': 'Décaissée', 'REJETEE': 'Rejetée', 'ACTIVE': 'Active',
    'EXPIREE': 'Expirée', 'RESILIEE': 'Résiliée', 'EN_ATTENTE': 'En attente',
    'PAYEE': 'Payée', 'EN_RETARD': 'En retard', 'OUVERTE': 'Ouverte',
    'EN_COURS': 'En cours', 'FERMEE': 'Fermée',
  };
  return map[statut] || statut;
}

function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function showLoading(container) {
  container.innerHTML = `<div class="loading-spinner"><div class="spinner"></div></div>`;
}

function showError(container, message) {
  container.innerHTML = `<div class="alert alert-danger">${message}</div>`;
}

function clearErrors() {
  document.querySelectorAll('.error-text').forEach(el => {
    el.textContent = '';
    el.classList.remove('visible');
  });
  document.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));
}

function showFieldError(fieldId, message) {
  const group = document.getElementById(fieldId)?.closest('.form-group');
  if (group) {
    group.classList.add('has-error');
    const errorEl = group.querySelector('.error-text');
    if (errorEl) {
      errorEl.textContent = message;
      errorEl.classList.add('visible');
    }
  }
}

function openModal(modalId) {
  document.getElementById(modalId)?.classList.add('active');
}

function closeModal(modalId) {
  document.getElementById(modalId)?.classList.remove('active');
}

function closeAllModals() {
  document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
}

function sanitize(str) {
  const div = document.createElement('div');
  div.textContent = str || '';
  return div.innerHTML;
}

function formatRelativeTime(dateStr) {
  if (!dateStr) return '';
  const now = new Date();
  const date = new Date(dateStr);
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  if (diffMins < 1) return "à l'instant";
  if (diffMins < 60) return `il y a ${diffMins} min`;
  if (diffHours < 24) return `il y a ${diffHours}h`;
  if (diffDays < 7) return `il y a ${diffDays}j`;
  return formatDate(dateStr);
}

document.addEventListener('click', function (e) {
  if (e.target.classList.contains('modal-overlay') || e.target.classList.contains('modal-close') || e.target.closest('.modal-close')) {
    closeAllModals();
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (hamburger && sidebar) {
    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('open');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
    });
  }
});
