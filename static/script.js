/* ==========================================================================
   Google Antigravity Interactive Micro-Particles & Zero-Gravity Physics
   ========================================================================== */

function confirmApprove() {
    return confirm("Are you sure you want to approve this out-pass request?");
}

function confirmReject() {
    return confirm("Are you sure you want to reject this out-pass request?");
}

// Zero-Gravity Particle Physics Canvas
(function initAntigravityParticles() {
    window.addEventListener('DOMContentLoaded', () => {
        const canvas = document.getElementById('antigravity-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const colors = [
            'rgba(49, 134, 255, 0.45)',  // Google Blue
            'rgba(0, 185, 92, 0.45)',   // Google Green
            'rgba(251, 188, 4, 0.45)',  // Google Yellow
            'rgba(252, 65, 61, 0.45)'   // Google Coral Red
        ];

        const particleCount = Math.min(Math.floor(width / 35), 45);
        const particles = [];

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 2.5 + 1.2,
                color: colors[Math.floor(Math.random() * colors.length)],
                vx: (Math.random() - 0.5) * 0.4,
                vy: -Math.random() * 0.45 - 0.15, // Floating gently upward (anti-gravity)
                alpha: Math.random() * 0.5 + 0.3
            });
        }

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        function animate() {
            ctx.clearRect(0, 0, width, height);

            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;

                // Wrap around edges with anti-gravity drift
                if (p.y < -10) {
                    p.y = height + 10;
                    p.x = Math.random() * width;
                }
                if (p.x < -10) p.x = width + 10;
                if (p.x > width + 10) p.x = -10;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();
            });

            requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    });
})();