const OMEGA = -0.05; // turns per second
const T = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--spin-duration'));

const latex3ds = Array.from(document.getElementsByClassName('latex3d'));
let theta = parseFloat(getComputedStyle(latex3ds[0]).getPropertyValue('--theta'));
let t0 = 0;
const spin = (t) => {
  requestAnimationFrame(spin);
  // only increment theta after the CSS transition duration T has elapsed:
  // (we don't use setTimeout because it continues to fire when page isn't visible)
  if (t - t0 < T*1000) return;
  t0 = t;

  // since requestAnimationFrame and CSS transitions are paused when page isn't visible,
  // we only ever increment by T, regardless of how much time has actually passed:
  theta += OMEGA * T;
  latex3ds.forEach(latex3d => {
    latex3d.style.setProperty('--theta', `${theta}turn`);
  });
};
requestAnimationFrame(spin);
