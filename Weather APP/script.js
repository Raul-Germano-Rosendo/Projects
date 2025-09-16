const cityInput = document.getElementById('city-input');
const searchBtn = document.getElementById('search-btn');
const currentLocationBtn = document.getElementById('current-location-btn');
const weatherCard = document.getElementById('weather-card');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const currentDate = document.getElementById('current-date');
const forecastContainer = document.getElementById('forecast');
const themeBtn = document.getElementById('theme-btn');

const API_KEY = '2bdda6eb635833b1b7cac7e4aa210f26';

// Date
currentDate.textContent = new Date().toLocaleDateString('en-US', { weekday:'long', year:'numeric', month:'long', day:'numeric' });

// Theme toggle
themeBtn.addEventListener('click', () => document.body.classList.toggle('dark-mode'));

// Event listeners
searchBtn.addEventListener('click', searchCity);
cityInput.addEventListener('keypress', (e) => e.key === 'Enter' && searchCity());
currentLocationBtn.addEventListener('click', getCurrentLocationWeather);

function searchCity() {
    const city = cityInput.value.trim();
    city ? getWeatherByCity(city) : showError('Please enter a city name');
}

function getCurrentLocationWeather() {
    if (!navigator.geolocation) return showError('Geolocation not supported');
    loading.style.display = 'block'; weatherCard.style.display = 'none'; errorMessage.style.display = 'none';
    navigator.geolocation.getCurrentPosition(pos => {
        getWeatherByCoords(pos.coords.latitude, pos.coords.longitude);
    }, () => {
        loading.style.display = 'none'; weatherCard.style.display = 'block';
        showError('Unable to retrieve your location.');
    });
}

async function getWeatherByCity(city) {
    try {
        loading.style.display = 'block'; weatherCard.style.display = 'none'; errorMessage.style.display = 'none';
        const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`);
        if (!res.ok) throw new Error('City not found.');
        const data = await res.json();
        displayWeather(data);
        getForecast(data.coord.lat, data.coord.lon);
    } catch(err) { loading.style.display = 'none'; showError(err.message); }
}

async function getWeatherByCoords(lat, lon) {
    try {
        const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${API_KEY}`);
        if (!res.ok) throw new Error('Unable to fetch weather.');
        const data = await res.json();
        displayWeather(data);
        getForecast(lat, lon);
    } catch(err) { loading.style.display = 'none'; showError(err.message); }
}

function displayWeather(data) {
    document.querySelector('.city-name').textContent = `${data.name}, ${data.sys.country}`;
    document.querySelector('.current-temp').textContent = `${Math.round(data.main.temp)}°C`;
    document.querySelector('.weather-desc').textContent = capitalize(data.weather[0].description);
    document.querySelector('.weather-icon').innerHTML = getWeatherIcon(data.weather[0].icon);

    const details = [data.main.feels_like, data.main.humidity, data.wind.speed, data.main.pressure];
    document.querySelectorAll('.detail-value').forEach((el,i) => {
        el.textContent = i===0||i===1 ? `${Math.round(details[i])}${i===0?'°C':'%'}` : i===2 ? `${details[i]} m/s` : `${details[i]} hPa`;
    });

    loading.style.display = 'none'; weatherCard.style.display = 'block';
}

async function getForecast(lat, lon) {
    forecastContainer.innerHTML = '';
    const res = await fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${API_KEY}`);
    const data = await res.json();
    // Show 5 cards (every 8 hours = 1 per day roughly)
    for(let i=0; i<5; i++){
        const item = data.list[i*8]; // approx one per day
        const card = document.createElement('div');
        card.className = 'forecast-card';
        card.innerHTML = `
            <div class="forecast-date">${new Date(item.dt_txt).toLocaleDateString('en-US',{weekday:'short'})}</div>
            <div class="forecast-icon">${getWeatherIcon(item.weather[0].icon)}</div>
            <div class="forecast-temp">${Math.round(item.main.temp)}°C</div>
        `;
        forecastContainer.appendChild(card);
    }
}

function getWeatherIcon(iconCode){
    const map = {
        '01d':'fas fa-sun','01n':'fas fa-moon',
        '02d':'fas fa-cloud-sun','02n':'fas fa-cloud-moon',
        '03d':'fas fa-cloud','03n':'fas fa-cloud',
        '04d':'fas fa-cloud','04n':'fas fa-cloud',
        '09d':'fas fa-cloud-showers-heavy','09n':'fas fa-cloud-showers-heavy',
        '10d':'fas fa-cloud-sun-rain','10n':'fas fa-cloud-moon-rain',
        '11d':'fas fa-bolt','11n':'fas fa-bolt',
        '13d':'fas fa-snowflake','13n':'fas fa-snowflake',
        '50d':'fas fa-smog','50n':'fas fa-smog'
    };
    return `<i class="${map[iconCode]||'fas fa-cloud'}"></i>`;
}

function showError(msg){ errorText.textContent=msg; errorMessage.style.display='block'; weatherCard.style.display='none'; loading.style.display='none'; }
function capitalize(str){ return str.charAt(0).toUpperCase()+str.slice(1); }

window.addEventListener('load',()=>getWeatherByCity('London'));
