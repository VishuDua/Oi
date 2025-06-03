import React, { useCallback } from "react";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";

export default function ParticlesBackground() {
  const particlesInit = useCallback(async (engine) => {
    await loadFull(engine);
  }, []);

  const particlesLoaded = useCallback(async (container) => {}, []);

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      loaded={particlesLoaded}
      options={{
        fullScreen: { enable: true, zIndex: 0 },
        fpsLimit: 60,
        detectRetina: true,
        particles: {
          number: { value: 80, density: { enable: true, area: 800 } },
          color: { value: ["#34D399", "#10B981", "#D1FAE5"] },
          shape: { type: "circle" },
          opacity: { value: 0.5, random: { enable: true, minimumValue: 0.3 } },
          size: { value: 3, random: { enable: true, minimumValue: 1 } },
          move: {
            enable: true,
            speed: 2,
            direction: "none",
            random: false,
            straight: false,
            outModes: "out"
          },
          links: { enable: true, distance: 150, color: "#64748B", opacity: 0.4, width: 1 }
        },
        interactivity: {
          events: { onHover: { enable: true, mode: "grab" }, onClick: { enable: true, mode: "push" }, resize: true },
          modes: { grab: { distance: 200, links: { opacity: 0.5 } }, push: { quantity: 4 } }
        }
      }}
    />
  );
}
