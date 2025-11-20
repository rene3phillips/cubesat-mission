// --- Create starfield ---
const starCount = 100; // number of stars
for (let i = 0; i < starCount; i++) {
    const star = document.createElement('div');
    star.classList.add('star');
    star.style.top = Math.random() * window.innerHeight + 'px';
    star.style.left = Math.random() * window.innerWidth + 'px';
    star.style.animationDuration = (5 + Math.random() * 10) + 's'; // random speed
    star.style.width = star.style.height = (1 + Math.random() * 2) + 'px'; // random size
    document.body.appendChild(star);
}

// --- Telemetry fetch ---
const temp = document.getElementById('temp');
const hum = document.getElementById('hum');

async function fetchTelemetry() {
    try {
        const response = await fetch('/telemetry/latest');
        const data = await response.json();

        temp.textContent = data.TEMP + " °C";
        hum.textContent = data.HUM + " %";
    } catch (err) {
        temp.textContent = "---";
        hum.textContent = "---";
        console.error(err);
    }
}

// Fetch immediately, then every 2 seconds
fetchTelemetry();
setInterval(fetchTelemetry, 2000);