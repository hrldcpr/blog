const OMEGA = -0.05; // turns per second

const latex3ds = Array.from(document.getElementsByClassName('latex3d'));
const spin = () => {
  const t = performance.now();
  const theta = (OMEGA * t / 1000) + 0.5;
  latex3ds.forEach(latex3d => {
    latex3d.style.setProperty('--theta', `${theta}turn`);
  });
  setTimeout(spin, 10*1000);
};
spin();
