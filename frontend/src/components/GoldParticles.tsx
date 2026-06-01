"use client";

import { useEffect, useRef } from "react";

export default function GoldParticles() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Capture in a constant to guarantee non-null status to the TypeScript compiler
    const activeCanvas = canvas;

    let animationFrameId: number;
    let particles: Array<{
      x: number;
      y: number;
      size: number;
      speedX: number;
      speedY: number;
      opacity: number;
      color: string;
      wobble: number;
      wobbleSpeed: number;
    }> = [];

    const handleResize = () => {
      activeCanvas.width = window.innerWidth;
      activeCanvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);
    handleResize();

    const maxParticles = 50;

    function createParticle(randomY = false) {
      const size = Math.random() * 2.2 + 0.6;
      const x = Math.random() * activeCanvas.width;
      const y = randomY ? Math.random() * activeCanvas.height : activeCanvas.height + Math.random() * 20;

      const goldColors = [
        "rgba(207, 168, 74, ",  // #cfa84a
        "rgba(247, 227, 175, ", // #f7e3af
        "rgba(170, 119, 28, ",  // #aa771c
        "rgba(223, 194, 125, "  // #dfc27d
      ];
      const color = goldColors[Math.floor(Math.random() * goldColors.length)];

      return {
        x,
        y,
        size,
        speedX: Math.random() * 0.4 - 0.2,
        speedY: -(Math.random() * 0.5 + 0.2), // slow upward drift
        opacity: Math.random() * 0.7 + 0.1,
        color,
        wobble: Math.random() * Math.PI,
        wobbleSpeed: Math.random() * 0.015 + 0.005,
      };
    }

    // Initialize particles
    for (let i = 0; i < maxParticles; i++) {
      particles.push(createParticle(true));
    }

    const animate = () => {
      ctx.clearRect(0, 0, activeCanvas.width, activeCanvas.height);

      particles.forEach((p, index) => {
        // Apply upward drift and slight horizontal wobble
        p.y += p.speedY;
        p.wobble += p.wobbleSpeed;
        p.x += p.speedX + Math.sin(p.wobble) * 0.2;

        // Draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        
        // Setup shadow/glow for luxury feel
        ctx.shadowColor = "rgba(207, 168, 74, 0.4)";
        ctx.shadowBlur = p.size * 2.5;
        
        ctx.fillStyle = p.color + p.opacity + ")";
        ctx.fill();

        // Respawn particle if it floats off-screen
        if (p.y < -10 || p.x < -10 || p.x > activeCanvas.width + 10) {
          particles[index] = createParticle(false);
        }
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full pointer-events-none z-[5]"
      style={{ mixBlendMode: "screen" }}
    />
  );
}
