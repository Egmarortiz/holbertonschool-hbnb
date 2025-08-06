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
  const logoutLink = document.getElementById('logout-link');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }
  if (logoutLink) {
    logoutLink.style.display = token ? 'block' : 'none';
    if (!logoutLink.dataset.listener) {
      logoutLink.addEventListener('click', e => {
        e.preventDefault();
        setCookie('token', '', -1);
        window.location.href = 'index.html';
      });
      logoutLink.dataset.listener = 'true';
    }
  }
  return token;
}

// Require authentication for protected pages
function requireAuth() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
  }
  return token;
}

let placesCache = [];

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id') || params.get('id');
}

// Retrieve a place name and populate heading if present
async function populatePlaceName(placeId) {
  try {
    const resp = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
    if (!resp.ok) return;
    const place = await resp.json();
    const heading = document.getElementById('place-name');
    if (heading) heading.textContent = place.title || place.name || '';
  } catch (err) {
    // Silently ignore errors populating the name
  }
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

// Handle API responses for review submission
async function handleResponse(response, form) {
  if (response.ok) {
    alert('Review submitted successfully!');
    if (form) form.reset();
  } else {
    let errMsg = 'Failed to submit review';
    try {
      const data = await response.json();
      if (data && data.error) errMsg = data.error;
    } catch (e) {
      // Ignore JSON parsing errors
    }
    alert(errMsg);
  }
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

    const titleEl = document.createElement('h2');
    titleEl.textContent = place.title;
    const priceEl = document.createElement('p');
    priceEl.textContent = `$${place.price} per night`;

    const detailsLink = document.createElement('a');
    detailsLink.href = `place.html?id=${place.id}`;
    detailsLink.className = 'details-button';
    detailsLink.textContent = 'View Details';

    item.append(titleEl, priceEl, detailsLink);
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

// Fetch details for a specific place
async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
    if (!response.ok) throw new Error('Failed to fetch place details');
    const place = await response.json();

    try {
      const reviewsResp = await fetch('http://127.0.0.1:5000/api/v1/reviews/');
      if (reviewsResp.ok) {
        const reviewsData = await reviewsResp.json();
        const pid = parseInt(placeId, 10);
        place.reviews = reviewsData.filter(r => parseInt(r.place_id, 10) === pid);
        // fetch user names for each review
        const userPromises = place.reviews.map(r =>
          fetch(`http://127.0.0.1:5000/api/v1/users/${r.user_id}`)
        );
        const userResponses = await Promise.all(userPromises);
        for (let i = 0; i < userResponses.length; i++) {
          const resp = userResponses[i];
          if (resp.ok) {
            try {
              const user = await resp.json();
              place.reviews[i].user_name = `${user.first_name} ${user.last_name}`;
            } catch (e) {
              place.reviews[i].user_name = '';
            }
          } else {
            place.reviews[i].user_name = '';
          }
        }
      } else {
        place.reviews = [];
      }
    } catch (err) {
      place.reviews = [];
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
  detailsSection.classList.add('place-details');

  const nameEl = document.createElement('h2');
  nameEl.textContent = place.title || place.name || 'Untitled place';

  const hostEl = document.createElement('p');
  hostEl.className = 'place-info';
  hostEl.textContent = `Host: ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown'}`;

  const priceEl = document.createElement('p');
  priceEl.className = 'place-info';
  priceEl.textContent = `Price: $${place.price}`;

  const descEl = document.createElement('p');
  descEl.className = 'place-info';
  descEl.textContent = place.description || '';

  const amenitiesTitle = document.createElement('h3');
  amenitiesTitle.textContent = 'Amenities';
  const amenitiesList = document.createElement('ul');
  (place.amenities || []).forEach(amenity => {
    const li = document.createElement('li');
    li.textContent = amenity.name || amenity;
    amenitiesList.appendChild(li);
  });

  detailsSection.append(nameEl, hostEl, priceEl, descEl, amenitiesTitle, amenitiesList);

  if (reviewsSection) {
    reviewsSection.innerHTML = '';
    (place.reviews || []).forEach(review => {
      const card = document.createElement('div');
      card.className = 'review-card';

      const commentEl = document.createElement('p');
      commentEl.textContent = review.text || '';

      const userEl = document.createElement('p');
      userEl.textContent = review.user_name || '';

      const ratingEl = document.createElement('p');
      ratingEl.textContent = `Rating: ${review.rating || ''}`;

      card.append(commentEl, userEl, ratingEl);
      reviewsSection.appendChild(card);
    });
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
      const resp = await submitReview(token, placeId, text, rating);
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
  const currentPage = window.location.pathname.split('/').pop();
  const token = checkAuthentication();

  if (currentPage === 'add_review.html') {
    const authToken = requireAuth();
    const placeId = getPlaceIdFromURL();
    if (placeId) {
      populatePlaceName(placeId);
      const form = document.getElementById('review-form');
      if (form) {
        form.addEventListener('submit', async event => {
          event.preventDefault();
          const text = document.getElementById('review').value;
          const rating = document.getElementById('rating').value;
          const resp = await submitReview(authToken, placeId, text, rating);
          await handleResponse(resp, form);
        });
      }
    }
    return;
  }

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

