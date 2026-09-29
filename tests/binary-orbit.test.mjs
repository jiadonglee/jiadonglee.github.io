import assert from 'node:assert/strict';
import { binaryParameters, binaryState, eccentricAnomaly } from '../assets/js/binary-orbit.js';

const norm = vector => Math.hypot(...vector);
const close = (a, b, tolerance = 1e-9) => assert.ok(Math.abs(a - b) < tolerance, `${a} != ${b}`);
for (const q of [0.4, 0.7, 1]) {
  for (const e of [0, 0.45, 0.8]) {
    for (const inclination of [0, 60, 90]) {
      const parameters = binaryParameters(q, e, inclination);
      close(parameters.periodYears ** 2 * (1 + q), 1);
      for (const phase of [0, 0.001, 0.17, 0.5, 0.81, 0.999]) {
        const state = binaryState(phase, parameters);
        const E = eccentricAnomaly(2 * Math.PI * phase, e);
        close(E - e * Math.sin(E), 2 * Math.PI * phase);
        // The centre of mass is stationary; the light centroid uses the same positions.
        for (let axis = 0; axis < 3; axis++) {
          close(state.primary[axis] + q * state.secondary[axis], 0);
          close(state.photocentre[axis], 10 * (
            (1 - parameters.lightFraction) * state.primary[axis] +
            parameters.lightFraction * state.secondary[axis]));
        }
        close(state.rvPrimary + q * state.rvSecondary, 0);
        // Specific angular momentum and orbital energy stay constant around the orbit.
        const [x, y, z] = state.relative;
        const [vx, vy, vz] = state.velocity;
        const mu = 4 * Math.PI ** 2 * (1 + q);
        close(norm([y*vz-z*vy,z*vx-x*vz,x*vy-y*vx]), Math.sqrt(mu*(1-e*e)));
        close(norm(state.velocity)**2/2-mu/norm(state.relative), -mu/2);
        // RV equals the time derivative of the same line-of-sight displacement.
        const delta = 1e-6;
        const before = binaryState(phase-delta, parameters);
        const after = binaryState(phase+delta, parameters);
        close((after.primary[2]-before.primary[2])/(2*delta*parameters.periodYears)*4.74047046,
          state.rvPrimary, 2e-6);
        if (inclination === 0) close(state.rvPrimary, 0);
        if (q === 1) close(norm(state.photocentre), 0);
      }
      close(norm(binaryState(0,parameters).relative), 1-e);
      close(norm(binaryState(0.5,parameters).relative), 1+e);
    }
  }
}
console.log('Kepler equation, period, conservation, RV derivative, face-on RV and equal-light photocentre checks passed.');
