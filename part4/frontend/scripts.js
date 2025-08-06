// Utility functions for cookie management
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = '; expires=' + date.toUTCString();
  }
  document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

async function loginUser(email, password) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.error || response.statusText);
  }
  return response.json();
}
// Authentication check and login link toggle
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }
  return token;
}

let placesCache = [];

// Fetch places from the API
async function fetchPlaces(token) {
  try {
    const headers = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      headers
    });
  if (!response.ok) {
      throw new Error('Failed to fetch places');
    }
    placesCache = await response.json();
    displayPlaces(placesCache);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

// Populate places list in the DOM
function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';
  places.forEach(place => {
    const item = document.createElement('div');
    item.className = 'place-card';
    item.dataset.price = place.price;
    item.innerHTML = `
      <h2>${place.title}</h2>
      <p>${place.description || ''}</p>
      <p>Location: ${place.latitude}, ${place.longitude}</p>
      <p>Price: $${place.price}</p>
    `;
    list.appendChild(item);
  });
}
// Handle price filtering
function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;
  filter.addEventListener('change', event => {
    const value = event.target.value;
    const filtered = value === 'all'
      ? placesCache
      : placesCache.filter(p => p.price <= parseFloat(value));
    displayPlaces(filtered);
  });
}

function handleLoginForm() {
  const form = document.getElementById('login-form');
  if (!form) return;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('login-error');
    if (errorEl) errorEl.textContent = '';
    try {
      const data = await loginUser(email, password);
      setCookie('token', data.access_token, 1);
      window.location.href = 'index.html';
    } catch (error) {
      if (errorEl) errorEl.textContent = error.message || 'Login failed';
    }
  });
}
// Execute when DOM is ready
window.addEventListener('DOMContentLoaded', () => {
  const token = checkAuthentication();
  fetchPlaces(token);
  setupPriceFilter();
  handleLoginForm();
});

