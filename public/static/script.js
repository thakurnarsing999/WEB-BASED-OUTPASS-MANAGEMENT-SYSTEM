/* ==========================================================================
   Google Antigravity Interactive Micro-Particles & Zero-Gravity Physics
   Theme Management (Light / Dark Mode with Persistence & System Fallback)
   ========================================================================== */

function confirmApprove() {
    return confirm("Are you sure you want to approve this out-pass request?");
}

function confirmReject() {
    return confirm("Are you sure you want to reject this out-pass request?");
}

// Global Theme Management
(function initTheme() {
    function getStoredTheme() {
        try {
            return localStorage.getItem('outpass_theme');
        } catch (e) {
            return null;
        }
    }

    function getSystemTheme() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        try {
            localStorage.setItem('outpass_theme', theme);
        } catch (e) {}

        const toggleBtn = document.getElementById('themeToggleBtn');
        if (toggleBtn) {
            const isDark = theme === 'dark';
            toggleBtn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
            toggleBtn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
        }

        // Trigger particle color update if canvas exists
        if (window.updateAntigravityParticleColors) {
            window.updateAntigravityParticleColors();
        }
    }

    // Initialize toggle button on DOM ready
    window.addEventListener('DOMContentLoaded', () => {
        const toggleBtn = document.getElementById('themeToggleBtn');
        if (toggleBtn) {
            const currentTheme = document.documentElement.getAttribute('data-theme') || getStoredTheme() || getSystemTheme();
            toggleBtn.setAttribute('aria-label', currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
            toggleBtn.setAttribute('title', currentTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');

            toggleBtn.addEventListener('click', () => {
                const active = document.documentElement.getAttribute('data-theme') || getSystemTheme();
                const next = active === 'dark' ? 'light' : 'dark';
                applyTheme(next);
            });
        }
    });

    // Auto-update if OS theme changes and user hasn't explicitly set preference
    try {
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!getStoredTheme()) {
                    applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    } catch (e) {}
})();

// Zero-Gravity Particle Physics Canvas with Theme Adaptation
(function initAntigravityParticles() {
    window.addEventListener('DOMContentLoaded', () => {
        const canvas = document.getElementById('antigravity-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        function getColors() {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark' ||
                (!document.documentElement.getAttribute('data-theme') && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
            if (isDark) {
                return [
                    'rgba(138, 180, 248, 0.65)', // Google Luminous Blue
                    'rgba(129, 201, 149, 0.65)', // Google Luminous Green
                    'rgba(253, 214, 99, 0.65)',  // Google Luminous Yellow
                    'rgba(242, 139, 130, 0.65)'  // Google Luminous Coral Red
                ];
            }
            return [
                'rgba(49, 134, 255, 0.45)',  // Google Blue
                'rgba(0, 185, 92, 0.45)',   // Google Green
                'rgba(251, 188, 4, 0.45)',  // Google Yellow
                'rgba(252, 65, 61, 0.45)'   // Google Coral Red
            ];
        }

        let colors = getColors();

        const particleCount = Math.min(Math.floor(width / 35), 45);
        const particles = [];

        for (let i = 0; i < particleCount; i++) {
            const colorIndex = Math.floor(Math.random() * colors.length);
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 2.5 + 1.2,
                colorIndex: colorIndex,
                vx: (Math.random() - 0.5) * 0.4,
                vy: -Math.random() * 0.45 - 0.15, // Floating gently upward (anti-gravity)
                alpha: Math.random() * 0.5 + 0.3
            });
        }

        window.updateAntigravityParticleColors = function() {
            colors = getColors();
        };

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
                ctx.fillStyle = colors[p.colorIndex] || colors[0];
                ctx.fill();
            });

            requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    });
})();
