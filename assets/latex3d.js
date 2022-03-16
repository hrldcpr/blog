const OMEGA = -0.05; // turns per second

const {style} = document.documentElement;
const spin = (t) => {
  const theta = (OMEGA * t / 1000) % 1;
  style.setProperty('--theta', `${theta}turn`);
  requestAnimationFrame(spin);
};
requestAnimationFrame(spin);
