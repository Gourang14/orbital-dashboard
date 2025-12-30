const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

let width, height;
let stars = [];
const starCount = 200;

function init() {
    resize();
    createStars();
    animate();
    window.addEventListener('resize', resize);
}

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
}

function createStars() {
    stars = [];
    for (let i = 0; i < starCount; i++) {
        stars.push({
            x: Math.random() * width,
            y: Math.random() * height,
            z: Math.random() * 2 + 0.5, // speed/depth
            size: Math.random() * 1.5
        });
    }
}

function animate() {
    ctx.clearRect(0, 0, width, height);
    
    // Draw stars
    ctx.fillStyle = '#fff';
    stars.forEach(star => {
        // Move star
        star.y -= star.z * 0.2; // Move up? Or maybe center out? Let's do simple parallax drift
        
        // Reset if out of bounds
        if (star.y < 0) {
            star.y = height;
            star.x = Math.random() * width;
        }
        
        // Draw
        ctx.globalAlpha = Math.random() * 0.5 + 0.3;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fill();
    });
    
    requestAnimationFrame(animate);
}

init();
