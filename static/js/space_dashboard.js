// Main Dashboard Controller

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initGPS();
    initPIV();
});

// --- UI Logic ---
function switchTab(tabName) {
    document.querySelectorAll('.dashboard-tab').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-links li').forEach(el => el.classList.remove('active'));

    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Highlight the correct nav item
    const navItems = document.querySelectorAll('.nav-links li');
    navItems.forEach(item => {
        if (item.getAttribute('onclick').includes(tabName)) {
            item.classList.add('active');
        }
    });
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

function initClock() {
    const updateTime = () => {
        const now = new Date();
        const dateEl = document.getElementById('sys-date');
        const timeEl = document.getElementById('sys-time');
        if (dateEl) dateEl.textContent = now.toLocaleDateString();
        if (timeEl) timeEl.textContent = now.toLocaleTimeString();
    };
    setInterval(updateTime, 1000);
    updateTime();
}

// --- GPS Logic ---
function initGPS() {
    // Init Leaflet Map if element exists
    if (!document.getElementById('map')) return;

    const map = L.map('map').setView([25.3, 83], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    let markers = {};

    function updateData() {
        // console.log("Fetching GPS Data...");
        fetch('/map_data')
            .then(res => res.json())
            .then(data => {
                const tbody = document.querySelector('#gps-table tbody');
                if (tbody) tbody.innerHTML = '';

                Object.values(markers).forEach(m => map.removeLayer(m));
                markers = {};

                let totalTemp = 0;
                let count = 0;

                const recentData = data.slice(0, 15); // Top 15

                recentData.forEach(row => {
                    const m = L.marker([row.latitude, row.longitude]).addTo(map);
                    m.bindPopup(`<b>${row.robot_id}</b><br>Temp: ${row.temperature}`);
                    markers[row.id] = m;

                    if (tbody) {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td>${row.data_id}</td>
                            <td class="neon-blue">${row.robot_id}</td>
                            <td>${row.temperature}°</td>
                            <td>${row.latitude.toFixed(4)}</td>
                            <td>${row.longitude.toFixed(4)}</td>
                            <td class="text-dim">LIVE</td>
                        `;
                        tbody.appendChild(tr);
                    }

                    totalTemp += row.temperature;
                    count++;
                });

                const avg = count > 0 ? (totalTemp / count).toFixed(1) : 0;
                const tempEl = document.getElementById('avg-temp');
                const botsEl = document.getElementById('active-bots');
                if (tempEl) tempEl.textContent = `${avg}°C`;
                if (botsEl) botsEl.textContent = count;
            })
            .catch(err => console.error("GPS Fetch Error:", err));
    }

    setInterval(updateData, 5000);
    updateData();
}

// --- PIV Logic ---
function initPIV() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('processed-canvas');
    if (!video || !canvas) return;

    const ctx = canvas.getContext('2d');
    const processor = new window.ImageProcessor();

    let activeFilter = 'original';
    let isStreaming = false;

    let currentStream = null;

    function startCamera(facingMode = 'user') {
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
        }

        navigator.mediaDevices.getUserMedia({ video: { facingMode: facingMode } })
            .then(stream => {
                currentStream = stream;
                video.srcObject = stream;
                video.play();
                video.onloadedmetadata = () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    isStreaming = true;
                    requestAnimationFrame(processFrame);
                };
            })
            .catch(err => console.error("Camera error:", err));
    }

    // Initial Camera Load
    startCamera();

    // Camera Switcher
    const camSelect = document.getElementById('camera-select');
    if (camSelect) {
        camSelect.addEventListener('change', (e) => {
            // If user explicitly selects camera, we switch back to webcams
            startCamera(e.target.value);
        });
    }

    // Video Upload Logic
    const videoUpload = document.getElementById('video-upload');
    if (videoUpload) {
        videoUpload.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                // Stop any webcam stream
                if (currentStream) {
                    currentStream.getTracks().forEach(track => track.stop());
                    currentStream = null;
                }

                // Clear srcObject (webcam) and set src (file)
                video.srcObject = null;
                video.src = URL.createObjectURL(file);
                video.loop = true;
                video.play();

                video.onloadeddata = () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    isStreaming = true;
                    requestAnimationFrame(processFrame);
                    console.log("Video uploaded and playing");
                };
            }
        });
    }

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            activeFilter = e.target.dataset.filter;
        });
    });

    let lastTime = 0;

    function processFrame(time) {
        if (!isStreaming) return;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        if (activeFilter !== 'original') {
            try {
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const processedLines = processor.process(imageData, activeFilter, {});
                ctx.putImageData(processedLines, 0, 0);
            } catch (e) {
                // Ignore frame errors
            }
        }

        const delta = time - lastTime;
        if (delta > 0) {
            const fps = (1000 / delta).toFixed(0);
            const fpsEl = document.getElementById('fps-counter');
            if (fpsEl) fpsEl.textContent = `FPS: ${fps}`;
        }
        lastTime = time;

        requestAnimationFrame(processFrame);
    }
}

// --- Graph Logic (WITH DEBUGGING) ---
let graphInterval = null;

function initGraphs() {
    console.log("Initializing Graphs...");

    // Bar Chart
    fetch('/bar_chart_data')
        .then(res => res.json())
        .then(data => {
            console.log("Bar Chart Data Received:", data);

            if (!data || data.length === 0) {
                console.warn("Bar chart data is empty or null");
                return;
            }

            const traces = [];
            const colors = ['#00f3ff', '#bc13fe', '#0aff00'];

            data.forEach((dataset, i) => {
                if (!dataset) return;

                // Debug individual dataset
                // console.log(`Processing dataset ${i}:`, dataset);

                const x_vals = dataset.map(d => d.robot_id);
                const y_vals = dataset.map(d => d.avg_quality);

                traces.push({
                    x: x_vals,
                    y: y_vals,
                    name: `Quality ${i + 1}`,
                    type: 'bar',
                    marker: { color: colors[i % colors.length] }
                });
            });

            console.log("Bar Chart Traces:", traces);

            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#7a8b99', family: 'Rajdhani' },
                xaxis: { title: 'Robot ID', gridcolor: 'rgba(0,243,255,0.1)' },
                yaxis: { title: 'Avg Quality', gridcolor: 'rgba(0,243,255,0.1)' },
                barmode: 'group',
                margin: { t: 30, b: 40, l: 40, r: 20 },
                legend: { orientation: 'h', y: 1.1 },
                height: 380, // Force height in JS too
                autosize: true
            };

            Plotly.newPlot('quality-chart', traces, layout, { responsive: true });
        })
        .catch(err => console.error("Bar Chart Fetch Error:", err));

    // Pie Chart
    fetch('/pie_chart_data')
        .then(res => res.json())
        .then(data => {
            console.log("Pie Chart Data Received:", data);

            if (!data || data.length === 0) {
                console.warn("Pie chart data is empty or null");
                return;
            }

            const labels = data.map(d => d.robot_id);
            const values = data.map(d => d.count);

            const pieData = [{
                labels: labels,
                values: values,
                type: 'pie',
                marker: {
                    colors: ['#00f3ff', '#bc13fe', '#0aff00', '#ff0055', '#ffff00'],
                    line: { color: '#050a14', width: 2 }
                },
                textinfo: 'label+percent',
                textfont: { color: '#e0faff' },
                hoverinfo: 'label+value'
            }];

            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#7a8b99', family: 'Rajdhani' },
                showlegend: true,
                legend: { font: { color: '#e0faff' } },
                margin: { t: 30, b: 30, l: 30, r: 30 },
                height: 380,
                autosize: true
            };

            Plotly.newPlot('distribution-chart', pieData, layout, { responsive: true });
        })
        .catch(err => console.error("Pie Chart Fetch Error:", err));
}

// Auto-load graphs when tab is switched
document.addEventListener('click', (e) => {
    const target = e.target.closest('li[onclick*="graphs"]') || e.target.closest('button[onclick*="graphs"]');

    if (target) {
        console.log("Graphs Tab Clicked. Starting Update Loop.");
        setTimeout(() => {
            initGraphs();
            if (graphInterval) clearInterval(graphInterval);
            graphInterval = setInterval(initGraphs, 5000);
        }, 100);
    } else if (e.target.closest('li[onclick*="piv"]') || e.target.closest('li[onclick*="gps"]')) {
        console.log("Leaving Graphs Tab. Stopping Update Loop.");
        if (graphInterval) {
            clearInterval(graphInterval);
            graphInterval = null;
        }
    }
});
