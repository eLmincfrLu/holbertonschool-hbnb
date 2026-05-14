document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    // 1. Login linkinin görünürlüyü
    if (loginLink) {
        // Əgər token varsa (login olubsa), Login düyməsini gizlət
        loginLink.style.display = token ? 'none' : 'block';
    }

    // 2. Login Formasını İdarə Et
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // DİQQƏT: Buradakı URL sənin Flask serverinin ünvanı olmalıdır
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Tokeni cookie-də saxlayırıq
                    document.cookie = `token=${data.access_token}; path=/; max-age=3600`;
                    // Əsas səhifəyə yönləndir
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.message || 'Invalid credentials'));
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('Serverlə əlaqə qurulmadı. Backend-in işlədiyindən əmin ol!');
            }
        });
    }

    // 3. Əsas səhifədə yerləri göstər
    if (document.getElementById('places-list')) {
        fetchPlaces();
    }
});

// Məkanları API-dən çəkən funksiya
async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/');
        if (!response.ok) throw new Error('Məlumat alınmadı');
        
        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
        const list = document.getElementById('places-list');
        if (list) list.innerHTML = '<p style="color:red;">Məkanlar yüklənmədi. API-nin işlədiyindən əmin olun.</p>';
    }
}

// Məkanları ekrana yazdıran funksiya
function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;
    
    list.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = place.price_per_night;
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p><strong>Price:</strong> $${place.price_per_night}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });
}

// Cookie oxumaq üçün köməkçi funksiya
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Qiymətə görə filterləmə
const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
    priceFilter.addEventListener('change', (e) => {
        const maxPrice = e.target.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}