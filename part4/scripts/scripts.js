document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    // 1. Login Link Visibility
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    // 2. Handle Login Form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = 'index.html';
            } else {
                alert('Login failed!');
            }
        });
    }

    // 3. Fetch and Display Places
    if (document.getElementById('places-list')) {
        fetchPlaces();
    }
});

async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/');
        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    list.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price_per_night;
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price: $${place.price_per_night}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });
}

// 4. Helper: Get Cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// 5. Client-side Filtering
if (document.getElementById('price-filter')) {
    document.getElementById('price-filter').addEventListener('change', (e) => {
        const maxPrice = e.target.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            card.style.display = (maxPrice === 'All' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
        });
    });
}