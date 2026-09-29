import { binaryParameters, binaryState, planck } from './binary-orbit.js';

const byId = id => document.getElementById(id);
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const controls = ['mass-ratio', 'eccentricity', 'inclination'].map(byId);
const phaseSlider = byId('orbital-phase');
const pauseButton = byId('motion-toggle');
let phase = Number(phaseSlider.value);
let paused = reducedMotion.matches;
let parameters;
let rvLimit;
let lastTime;

const svgPath = points => points.map(([x, y], index) =>
  `${index ? 'L' : 'M'}${x.toFixed(3)},${y.toFixed(3)}`).join(' ');
const orbitPoint = position => [130 + 90 * position[0], 110 - 90 * position[1]];
const photocentrePoint = position => [130 + 23 * position[0], 110 - 23 * position[1]];
const rvPoint = (time, velocity) => [40 + time * 462, 66 - velocity * 50 / rvLimit];
const setPath = (id, points) => byId(id).setAttribute('d', svgPath(points));
function setDot(id, point) {
  const dot = byId(id);
  dot.setAttribute('cx', point[0]);
  dot.setAttribute('cy', point[1]);
}

const wavelengths = Array.from({ length: 181 }, (_, i) => 350 + i * 750 / 180);
const primaryFlux = wavelengths.map(wavelength => planck(wavelength, 5800));
const fluxScale = 2.15 * Math.max(...primaryFlux);
const spectrumPoints = flux => flux.map((value, i) => [36 + i * 444 / 180, 135 - 110 * value / fluxScale]);
setPath('primary-curve', spectrumPoints(primaryFlux));

function updateSpectrum() {
  const q = parameters.q;
  const secondary = wavelengths.map(wavelength => q ** 1.6 * planck(wavelength, 5800 * Math.sqrt(q)));
  setPath('secondary-curve', spectrumPoints(secondary));
  setPath('combined-curve', spectrumPoints(primaryFlux.map((flux, i) => flux + secondary[i])));
}

function renderPhase() {
  const state = binaryState(phase, parameters);
  setDot('star-primary', orbitPoint(state.primary));
  setDot('star-secondary', orbitPoint(state.secondary));
  setDot('photocentre-dot', photocentrePoint(state.photocentre));
  setDot('rv-primary-dot', rvPoint(phase, state.rvPrimary));
  setDot('rv-secondary-dot', rvPoint(phase, state.rvSecondary));
  const x = rvPoint(phase, 0)[0];
  byId('phase-line').setAttribute('d', `M${x} 16V116`);
  phaseSlider.value = phase;
  byId('phase-value').value = phase.toFixed(2);
}

function updateParameters() {
  const [q, eccentricity, inclination] = controls.map(control => Number(control.value));
  parameters = binaryParameters(q, eccentricity, inclination);
  byId('ratio-value').value = q.toFixed(2);
  byId('eccentricity-value').value = eccentricity.toFixed(2);
  byId('inclination-value').value = `${inclination}°`;
  const samples = Array.from({ length: 361 }, (_, i) => binaryState(i / 360, parameters));
  // Keep the RV axis independent of inclination so face-on suppression is visible.
  const edgeOn = binaryParameters(q, eccentricity, 90);
  const edgeSamples = Array.from({ length: 361 }, (_, i) => binaryState(i / 360, edgeOn));
  rvLimit = Math.ceil(Math.max(...edgeSamples.flatMap(s => [Math.abs(s.rvPrimary), Math.abs(s.rvSecondary)])) / 10) * 10;
  byId('rv-top').textContent = `+${rvLimit}`;
  byId('rv-bottom').textContent = `−${rvLimit}`;
  setPath('orbit-primary', samples.map(state => orbitPoint(state.primary)));
  setPath('orbit-secondary', samples.map(state => orbitPoint(state.secondary)));
  setPath('photocentre-path', samples.map(state => photocentrePoint(state.photocentre)));
  setPath('rv-primary', samples.map((state, i) => rvPoint(i / 360, state.rvPrimary)));
  setPath('rv-secondary', samples.map((state, i) => rvPoint(i / 360, state.rvSecondary)));
  byId('star-secondary').setAttribute('r', 6 * q ** 0.8);
  const aPhoto = Math.abs(parameters.lightFraction - parameters.massFraction) * parameters.masPerAU;
  byId('orbit-readout').textContent = `P = ${(parameters.periodYears * 365.25).toFixed(0)} d · aₚₕ = ${aPhoto.toFixed(2)} mas · F₂/F₁ (550 nm) = ${parameters.fluxRatio.toFixed(2)}`;
  updateSpectrum();
  renderPhase();
}

function updatePlayback() {
  pauseButton.textContent = paused ? 'Play' : 'Pause';
  pauseButton.setAttribute('aria-pressed', String(paused));
}
pauseButton.hidden = false;
pauseButton.addEventListener('click', () => {
  paused = !paused;
  lastTime = undefined;
  updatePlayback();
});
controls.forEach(control => {
  control.disabled = false;
  control.addEventListener('input', updateParameters);
});
phaseSlider.disabled = false;
phaseSlider.addEventListener('input', () => {
  paused = true;
  phase = Number(phaseSlider.value);
  updatePlayback();
  renderPhase();
});
reducedMotion.addEventListener('change', () => {
  paused = reducedMotion.matches;
  lastTime = undefined;
  updatePlayback();
});
document.addEventListener('visibilitychange', () => { lastTime = undefined; });
function animate(time) {
  if (!paused && !document.hidden && lastTime !== undefined) {
    phase = (phase + (time - lastTime) / 12000) % 1;
    renderPhase();
  }
  lastTime = time;
  requestAnimationFrame(animate);
}
updateParameters();
updatePlayback();
requestAnimationFrame(animate);

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      if (!reducedMotion.matches) entry.target.classList.add('arriving');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(section => observer.observe(section));
