const OMEGA = -0.05; // turns per second
const spinners = Array.from(document.getElementsByClassName('latex3d'));

const spin = (t) => {
  const theta = (OMEGA * t / 1000) % 1;
  spinners.forEach(spinner => {
    spinner.style.transform = `rotateX(0.1turn) rotateY(${theta}turn)`;
  });
  requestAnimationFrame(spin);
};
requestAnimationFrame(spin);
