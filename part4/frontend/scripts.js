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
  const loginLink = document.getElementById('login-link') ||
    document.querySelector('.login-button');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }
  return token;
}

let placesCache = [];

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id') || params.get('id');
}

async function submitReview(token, placeId, reviewText, rating) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ text: reviewText, rating: parseInt(rating, 10), place_id: placeId })
  });
  return response;
}

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
      <h2><a href="place.html?id=${place.id}">${place.title}</a></h2>
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

// Extract place ID from URL query string
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// Fetch details for a specific place
async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
    if (!response.ok) throw new Error('Failed to fetch place details');
    const place = await response.json();

    if (!place.reviews) {
      try {
        const revRes = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`);
        if (revRes.ok) place.reviews = await revRes.json();
      } catch (e) {
        // ignore errors fetching reviews
      }
    }

    displayPlaceDetails(place);
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

// Display place details and reviews
function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  const reviewsSection = document.getElementById('reviews');
  if (!detailsSection) return;

  detailsSection.innerHTML = '';
  const nameEl = document.createElement('h2');
  nameEl.textContent = place.title || place.name || 'Untitled place';
  const descEl = document.createElement('p');
  descEl.textContent = place.description || '';
  const priceEl = document.createElement('p');
  priceEl.textContent = `Price: $${place.price}`;

  const amenitiesTitle = document.createElement('h3');
  amenitiesTitle.textContent = 'Amenities';
  const amenitiesList = document.createElement('ul');
  (place.amenities || []).forEach(amenity => {
    const li = document.createElement('li');
    li.textContent = amenity.name || amenity;
    amenitiesList.appendChild(li);
  });

  detailsSection.append(nameEl, descEl, priceEl, amenitiesTitle, amenitiesList);

  if (reviewsSection) {
    reviewsSection.innerHTML = '';
    const reviewsTitle = document.createElement('h3');
    reviewsTitle.textContent = 'Reviews';
    const reviewsList = document.createElement('ul');
    (place.reviews || []).forEach(review => {
      const li = document.createElement('li');
      li.textContent = `${review.text || ''} - Rating: ${review.rating || ''}`;
      reviewsList.appendChild(li);
    });
    reviewsSection.append(reviewsTitle, reviewsList);
  }
}

// Show add review form when authenticated
function showAddReviewForm(placeId, token) {
  const section = document.getElementById('add-review-section');
  if (!section) return;
  section.innerHTML = `
    <h3>Add a Review</h3>
    <form id="review-form" class="add-review form">
      <label for="review">Your Review:</label>
      <textarea id="review" name="review" required></textarea>
      <label for="rating">Rating:</label>
      <select id="rating" name="rating" required>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
      </select>
      <button type="submit">Submit Review</button>
    </form>`;

  const form = document.getElementById('review-form');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const text = document.getElementById('review').value;
    const rating = document.getElementById('rating').value;
    try {
      const resp = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ text, rating })
      });
      if (!resp.ok) throw new Error('Failed to submit review');
      form.reset();
      fetchPlaceDetails(token, placeId);
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  });
}

// Execute when DOM is ready
window.addEventListener('DOMContentLoaded', () => {
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (placeId) {
    if (token) {
      showAddReviewForm(placeId, token);
    } else {
      const section = document.getElementById('add-review-section');
      if (section) section.style.display = 'none';
    }
    fetchPlaceDetails(token, placeId);
  } else {
    if (document.getElementById('places-list')) {
      fetchPlaces(token);
      setupPriceFilter();
    }
    handleLoginForm();
  }
});

