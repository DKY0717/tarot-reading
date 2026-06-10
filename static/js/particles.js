class MysticalParticles {
    constructor() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        this.canvas = document.createElement('canvas');
        this.canvas.id = 'particleCanvas';
        this.ctx = this.canvas.getContext('2d');

        document.body.prepend(this.canvas);

        this.particles = [];
        this.burstParticles = [];
        this.mouse = { x: -1000, y: -1000 };
        this.mouseActive = false;
        this.dpr = Math.min(window.devicePixelRatio || 1, 2);
        this.width = 0;
        this.height = 0;
        this.animId = null;

        this.colors = [
            { r: 255, g: 215, b: 0 },
            { r: 147, g: 112, b: 219 },
            { r: 200, g: 180, b: 255 },
            { r: 255, g: 255, b: 255 },
        ];

        this.resize();
        this.createAmbientParticles();
        this.bindEvents();
        this.animate();
    }

    resize() {
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width * this.dpr;
        this.canvas.height = this.height * this.dpr;
        this.canvas.style.width = this.width + 'px';
        this.canvas.style.height = this.height + 'px';
        this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    }

    createAmbientParticles() {
        const count = Math.min(Math.floor((this.width * this.height) / 15000), 100);
        this.particles = [];
        for (let i = 0; i < count; i++) {
            this.particles.push(this.createAmbientParticle());
        }
    }

    createAmbientParticle() {
        const color = this.colors[Math.floor(Math.random() * this.colors.length)];
        return {
            x: Math.random() * this.width,
            y: Math.random() * this.height,
            vx: (Math.random() - 0.5) * 0.3,
            vy: (Math.random() - 0.5) * 0.3,
            size: Math.random() * 2 + 0.5,
            baseOpacity: Math.random() * 0.4 + 0.15,
            opacity: 0,
            phase: Math.random() * Math.PI * 2,
            pulseSpeed: Math.random() * 0.015 + 0.005,
            color: color,
            type: 'ambient'
        };
    }

    bindEvents() {
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                this.resize();
                this.createAmbientParticles();
            }, 200);
        });

        document.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
            this.mouseActive = true;
        });

        document.addEventListener('mouseleave', () => {
            this.mouseActive = false;
        });

        document.addEventListener('click', (e) => {
            this.burst(e.clientX, e.clientY, 15);
        });
    }

    burst(x, y, count = 15) {
        for (let i = 0; i < count; i++) {
            const angle = (Math.PI * 2 / count) * i + (Math.random() - 0.5) * 0.5;
            const speed = Math.random() * 3 + 1.5;
            const color = this.colors[Math.floor(Math.random() * this.colors.length)];
            this.burstParticles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size: Math.random() * 3 + 1,
                opacity: 1,
                color: color,
                life: 1,
                decay: Math.random() * 0.015 + 0.01,
                type: 'burst'
            });
        }
    }

    magicBurst(x, y, count = 30) {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 4 + 2;
            const color = this.colors[Math.floor(Math.random() * 3)];
            this.burstParticles.push({
                x: x + (Math.random() - 0.5) * 40,
                y: y + (Math.random() - 0.5) * 40,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed - 1,
                size: Math.random() * 4 + 1.5,
                opacity: 1,
                color: color,
                life: 1,
                decay: Math.random() * 0.01 + 0.008,
                type: 'magic'
            });
        }
    }

    updateAmbient() {
        for (const p of this.particles) {
            p.phase += p.pulseSpeed;
            p.opacity = p.baseOpacity + Math.sin(p.phase) * 0.15;

            if (this.mouseActive) {
                const dx = this.mouse.x - p.x;
                const dy = this.mouse.y - p.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const radius = 180;
                if (dist < radius) {
                    const force = (radius - dist) / radius;
                    const angle = Math.atan2(dy, dx);
                    p.x -= Math.cos(angle) * force * 1.2;
                    p.y -= Math.sin(angle) * force * 1.2;
                }
            }

            p.x += p.vx;
            p.y += p.vy;

            if (p.x < -10) p.x = this.width + 10;
            if (p.x > this.width + 10) p.x = -10;
            if (p.y < -10) p.y = this.height + 10;
            if (p.y > this.height + 10) p.y = -10;

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${p.color.r},${p.color.g},${p.color.b},${Math.max(0, p.opacity)})`;
            this.ctx.fill();
        }
    }

    drawConstellations() {
        const maxDist = 120;
        const len = this.particles.length;
        for (let i = 0; i < len; i++) {
            const a = this.particles[i];
            for (let j = i + 1; j < len; j++) {
                const b = this.particles[j];
                const dx = a.x - b.x;
                const dy = a.y - b.y;
                const distSq = dx * dx + dy * dy;
                if (distSq < maxDist * maxDist) {
                    const dist = Math.sqrt(distSq);
                    const alpha = (1 - dist / maxDist) * 0.12;
                    this.ctx.beginPath();
                    this.ctx.moveTo(a.x, a.y);
                    this.ctx.lineTo(b.x, b.y);
                    this.ctx.strokeStyle = `rgba(255,215,0,${alpha})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }
        }
    }

    updateBurst() {
        for (let i = this.burstParticles.length - 1; i >= 0; i--) {
            const p = this.burstParticles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vx *= 0.97;
            p.vy *= 0.97;
            p.vy += 0.02;
            p.life -= p.decay;
            p.opacity = p.life;

            if (p.life <= 0) {
                this.burstParticles.splice(i, 1);
                continue;
            }

            const glow = p.type === 'magic' ? 6 : 3;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${p.color.r},${p.color.g},${p.color.b},${p.opacity})`;
            this.ctx.shadowColor = `rgba(${p.color.r},${p.color.g},${p.color.b},${p.opacity * 0.5})`;
            this.ctx.shadowBlur = glow;
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        }
    }

    drawMouseGlow() {
        if (!this.mouseActive) return;
        const gradient = this.ctx.createRadialGradient(
            this.mouse.x, this.mouse.y, 0,
            this.mouse.x, this.mouse.y, 120
        );
        gradient.addColorStop(0, 'rgba(255, 215, 0, 0.04)');
        gradient.addColorStop(0.5, 'rgba(147, 112, 219, 0.02)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(this.mouse.x - 120, this.mouse.y - 120, 240, 240);
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);

        this.drawMouseGlow();
        this.drawConstellations();
        this.updateAmbient();
        this.updateBurst();

        this.animId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        if (this.animId) cancelAnimationFrame(this.animId);
        this.canvas.remove();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.mysticalParticles = new MysticalParticles();
});

window.particleBurst = function(x, y, count) {
    if (window.mysticalParticles) {
        window.mysticalParticles.burst(x, y, count);
    }
};

window.magicBurst = function(x, y, count) {
    if (window.mysticalParticles) {
        window.mysticalParticles.magicBurst(x, y, count);
    }
};
