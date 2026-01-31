// const API_BASE = 'http://localhost:8001'; // backend
const API_BASE = 'http://3.15.137.87:8001'; // deployed backend 

// --- Create starfield ---
const starCount = 100; // number of stars
for (let i = 0; i < starCount; i++) {
  const star = document.createElement('div');
  star.classList.add('star');
  star.style.top = Math.random() * window.innerHeight + 'px';
  star.style.left = Math.random() * window.innerWidth + 'px';
  star.style.animationDuration = 5 + Math.random() * 10 + 's'; // random speed
  star.style.width = star.style.height = 1 + Math.random() * 2 + 'px'; // random size
  document.body.appendChild(star);
}

document.addEventListener('DOMContentLoaded', () => {
  // --- DOM Elements ---
  const tempC = document.getElementById('temp-c');
  const tempF = document.getElementById('temp-f');
  const hum = document.getElementById('hum');
  const date = document.getElementById('date');
  const time = document.getElementById('time');
  const missionName = document.getElementById('mission-name');
  const status = document.getElementById('status');
  const missionDiv = document.getElementById('mission');
  const elapsedDisplay = document.getElementById('elapsed');
  const logsContainer = document.getElementById('log-list');
  const chartImage = document.getElementById('mission-chart');

  // --- State ---
  let currentMission = null;
  let currentStatus = 'Pending';
  const statusOptions = ['Pending', 'Active', 'Completed'];
  let telemetryInterval = null;
  let elapsedInterval = null;
  let missionStartTime = null;

  // --- Send telemetry to backend ---
  async function sendReading(temp, hum) {
    if (!currentMission || currentStatus !== 'Active') return;

    fetch(`${API_BASE}/telemetry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        temp: temp !== null ? Number(temp) : null,
        hum: hum !== null ? Number(hum) : null,
        mission_name: currentMission,
        status: currentStatus,
        timestamp: new Date().toISOString(),
      }),
    }).catch((err) => console.error(err));
  }

  // --- Fetch latest telemetry ---
  async function fetchTelemetry() {
    if (!currentMission || currentStatus !== 'Active') return;

    try {
      const response = await fetch(`${API_BASE}/telemetry/latest`);
      const data = await response.json();

      const celsius = data.TEMP ?? null;
      if (celsius !== null) {
        tempC.textContent = `${celsius.toFixed(1)} °C`;
        tempF.textContent = `${((celsius * 9) / 5 + 32).toFixed(1)} °F`;
        sendReading(celsius, data.HUM);
      } else {
        tempC.textContent = '-- °C';
        tempF.textContent = '-- °F';
      }

      hum.textContent =
        (data.HUM !== undefined ? data.HUM.toFixed(1) : '--') + ' %';

      if (data.TIMESTAMP) {
        const ts = new Date(data.TIMESTAMP);
        date.textContent = `${ts.getMonth() + 1}/${ts.getDate()}/${ts.getFullYear()}`;
        time.textContent = `${ts.getHours().toString().padStart(2, '0')}:${ts.getMinutes().toString().padStart(2, '0')}:${ts.getSeconds().toString().padStart(2, '0')}`;
      } else {
        date.textContent = '--/--/----';
        time.textContent = '--:--:--';
      }
    } catch (err) {
      console.error('Fetch error:', err);
    }
  }

  // --- Update elapsed time ---
  function updateElapsed() {
    if (!missionStartTime) return;
    const diffSec = Math.floor((new Date() - missionStartTime) / 1000);
    const hours = Math.floor(diffSec / 3600);
    const minutes = Math.floor((diffSec % 3600) / 60);
    const seconds = diffSec % 60;
    elapsedDisplay.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

  // --- Fetch mission logs from backend ---
  async function fetchMissions() {
    try {
      const response = await fetch(`${API_BASE}/missions`);
      const missions = await response.json();

      const uniqueMissions = new Set();
      logsContainer.innerHTML = ''; // Clear existing logs

      let lastChartMission = null; // tracks currently displayed chart

      missions.forEach((mission) => {
        if (!uniqueMissions.has(mission.mission_name)) {
          uniqueMissions.add(mission.mission_name);

          const logCard = document.createElement('div');
          logCard.classList.add('log-card');

          // --- Hover listener with cache-buster and preload ---
          logCard.addEventListener('mouseenter', () => {
            if (lastChartMission !== mission.mission_name) {
              const newChart = new Image();
              newChart.src = `${API_BASE}/missions/${encodeURIComponent(mission.mission_name)}/chart`;
              newChart.onload = () => {
                chartImage.src = newChart.src;
              };
              lastChartMission = mission.mission_name;
            }
          });

          // --- Reset to default image on mouse leave ---
          logCard.addEventListener('mouseleave', () => {
            chartImage.src = 'images/sample-graph.png';
            lastChartMission = null;
          });

          // --- Click event navigates to mission page ---
          logCard.addEventListener('click', () => {
            window.location.href = `${API_BASE}/missions/${encodeURIComponent(mission.mission_name)}`;
          });

          // --- Display mission name and date ---
          logCard.innerHTML = `
                        <h3>${mission.mission_name}</h3>
                        <p>${new Date(mission.timestamp).toLocaleString()}</p>
                    `;

          logsContainer.appendChild(logCard);
        }
      });
    } catch (err) {
      console.error('Fetch mission logs error:', err);
    }
  }

  // --- Start a new mission ---
  // missionDiv.addEventListener('click', () => {
  //     const name = prompt("Enter Mission Name:", "New Mission");
  //     if (!name) return;

  //     currentMission = name;
  //     currentStatus = "Pending";
  //     missionName.textContent = currentMission;
  //     status.textContent = currentStatus;
  //     missionStartTime = null;
  //     elapsedDisplay.textContent = "00:00:00";

  //     // Start telemetry fetch interval if not already running
  //     if (!telemetryInterval) {
  //         telemetryInterval = setInterval(fetchTelemetry, 2000);
  //     }
  // });

  // // --- Change mission status ---
  // status.addEventListener('click', () => {
  //     if (!currentMission) return;

  //     const currentIndex = statusOptions.indexOf(currentStatus);
  //     const nextIndex = (currentIndex + 1) % statusOptions.length;
  //     currentStatus = statusOptions[nextIndex];
  //     status.textContent = currentStatus;

  //     if (currentStatus === "Active") {
  //         // Start elapsed timer
  //         missionStartTime = new Date();
  //         if (!elapsedInterval) elapsedInterval = setInterval(updateElapsed, 1000);
  //         if (!telemetryInterval) telemetryInterval = setInterval(fetchTelemetry, 2000);
  //     } else {
  //         // Stop telemetry and elapsed
  //         if (telemetryInterval) { clearInterval(telemetryInterval); telemetryInterval = null; }
  //         if (elapsedInterval) { clearInterval(elapsedInterval); elapsedInterval = null; }
  //     }

  //     // Send status update to backend
  //     sendReading(null, null);
  // });

  // --- Initial load ---
  fetchMissions();
});
