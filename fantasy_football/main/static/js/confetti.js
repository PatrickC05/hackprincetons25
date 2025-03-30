// // Simple confetti animation using Canvas
// const canvas = document.getElementById("confetti-canvas");
// const ctx = canvas.getContext("2d");

// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;

// let particles = [];

// function createParticles() {
//     for (let i = 0; i < 100; i++) {
//         particles.push({
//             x: Math.random() * canvas.width,
//             y: Math.random() * canvas.height,
//             size: Math.random() * 5 + 2,
//             color: `hsl(${Math.random() * 360}, 100%, 50%)`,
//             velocityX: (Math.random() - 0.5) * 2,
//             velocityY: Math.random() * 3 + 1,
//         });
//     }
// }

// function drawParticles() {
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     particles.forEach((p, i) => {
//         ctx.fillStyle = p.color;
//         ctx.beginPath();
//         ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
//         ctx.fill();

//         p.x += p.velocityX;
//         p.y += p.velocityY;

//         if (p.y > canvas.height) {
//             particles[i] = {
//                 x: Math.random() * canvas.width,
//                 y: 0,
//                 size: p.size,
//                 color: p.color,
//                 velocityX: p.velocityX,
//                 velocityY: p.velocityY,
//             };
//         }
//     });
// }

// function startConfetti() {
//     createParticles();
//     setInterval(drawParticles, 30);
// }

const canvas = document.getElementById("confetti-canvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];
let confettiActive = false;

function createParticles() {
    particles = [];
    for (let i = 0; i < 100; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 5 + 2,
            color: `hsl(${Math.random() * 360}, 100%, 50%)`,
            velocityX: (Math.random() - 0.5) * 2,
            velocityY: Math.random() * 3 + 1,
            opacity: 1
        });
    }
    confettiActive = true;
}

function drawParticles() {
    if (!confettiActive) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach((p, i) => {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.opacity;  // Apply fading effect
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        
        p.x += p.velocityX;
        p.y += p.velocityY;
        p.opacity -= 0.01;  // Gradually fade out

        if (p.y > canvas.height || p.opacity <= 0) {
            particles.splice(i, 1);
        }
    });

    if (particles.length > 0) {
        requestAnimationFrame(drawParticles);
    } else {
        confettiActive = false;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
}

function startConfetti() {
    createParticles();
    drawParticles();
    
    // Stop confetti after 15 seconds instead of 5 seconds
    setTimeout(() => {
        confettiActive = false;
    }, 15000);
}
