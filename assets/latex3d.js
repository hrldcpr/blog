const OMEGA = -0.05; // turns per second

const latex3ds = Array.from(document.getElementsByClassName('latex3d'));
const spin = (t) => {
  const theta = (OMEGA * t / 1000) % 1;
  latex3ds.forEach(latex3d => {
    latex3d.style.setProperty('--theta', `${theta}turn`);
    latex3d.style.setProperty('--untheta', `${-theta}turn`);
  });
  requestAnimationFrame(spin);
};
requestAnimationFrame(spin);
