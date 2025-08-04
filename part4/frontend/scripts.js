const samplePlaces = [
  {
    id: 1,
    name: 'Cozy Cottage',
    price: 120,
    host: 'Alice',
    description: 'A cozy cottage in the woods.',
    amenities: ['WiFi', '2 beds', '1 bath'],
    reviews: [
      { user: 'Bob', rating: 4, comment: 'Great stay!' },
      { user: 'Carol', rating: 5, comment: 'Loved it!' }
    ]
  },
  {
    id: 2,
    name: 'Urban Apartment',
    price: 90,
    host: 'Dave',
    description: 'Modern apartment in the city center.',
    amenities: ['WiFi', '1 bed', '1 bath'],
    reviews: []
  }
];


function setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = '; expires=' + date.toUTCString();
  }
  document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

function getCookie(name) {
  return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
}

function eraseCookie(name) {
  document.cookie = name + '=; Max-Age=0; path=/';
}

function isLoggedIn() {
  return !!getCookie('token');
}

function updateLoginButton() {
  const btn = document.querySelector('.login-button');
  if (!btn) return;
  if (isLoggedIn()) {
    btn.textContent = 'Logout';
    btn.href = '#';
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      eraseCookie('token');
      window.location.href = 'index.html';
    });
  } else {
    btn.textContent = 'Login';
    btn.href = 'login.html';
  }
}

function renderPlacesList() {
  const container = document.getElementById('places-list');
  if (!container) return;
  samplePlaces.forEach(function (place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = '<h2>' + place.name + '</h2>' +
      '<p>$' + place.price + ' per night</p>' +
      '<a class="details-button" href="place.html?id=' + place.id + '">View Details</a>';
    container.appendChild(card);
  });
}

function renderPlaceDetails() {
  const detailsSection = document.getElementById('place-details');
  if (!detailsSection) return;
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'), 10);
  const place = samplePlaces.find(function (p) { return p.id === id; });
  if (!place) return;
  detailsSection.classList.add('place-details');
  detailsSection.innerHTML = '<h1>' + place.name + '</h1>' +
    '<div class="place-info"><strong>Host:</strong> ' + place.host + '</div>' +
    '<div class="place-info"><strong>Price:</strong> $' + place.price + ' per night</div>' +
    '<div class="place-info"><strong>Description:</strong> ' + place.description + '</div>' +
    '<div class="place-info"><strong>Amenities:</strong> ' + place.amenities.join(', ') + '</div>';

  const reviewsSection = document.getElementById('reviews');
  place.reviews.forEach(function (r) {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = '<p>' + r.comment + '</p>' +
      '<p><strong>' + r.user + '</strong> - Rating: ' + r.rating + '</p>';
    reviewsSection.appendChild(card);
  });

  const addReview = document.getElementById('add-review-section');
  if (isLoggedIn()) {
    addReview.innerHTML = '<a href="add_review.html?id=' + place.id + '" class="add-review">Add Review</a>';
  } else {
    addReview.innerHTML = '<p>Please <a href="login.html">log in</a> to add a review.</p>';
  }
}

function handleLoginForm() {
  const form = document.getElementById('login-form');
  if (!form) return;
  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('login-error');
    if (errorEl) errorEl.textContent = '';
    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (response.ok) {
        const data = await response.json();
        setCookie('token', data.access_token, 1);
        window.location.href = 'index.html';
      } else {
        const err = await response.json();
        if (errorEl) errorEl.textContent = err.error || 'Login failed';
      }
    } catch (err) {
      if (errorEl) errorEl.textContent = 'Login failed';
    }
  });
}

function protectReviewForm() {
  const form = document.getElementById('review-form');
  if (!form) return;
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'), 10);
  const place = samplePlaces.find(function (p) { return p.id === id; });
  const title = document.getElementById('place-name');
  if (place && title) {
    title.textContent = 'Add Review for ' + place.name;
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Review submitted!');
    window.location.href = 'place.html?id=' + id;
  });
}

document.addEventListener('DOMContentLoaded', function () {
  updateLoginButton();
  renderPlacesList();
  renderPlaceDetails();
  handleLoginForm();
  protectReviewForm();
});

