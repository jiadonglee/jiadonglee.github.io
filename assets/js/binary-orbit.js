const TAU = 2 * Math.PI;
const AU_PER_YEAR_TO_KMS = 4.74047046;

export function planck(wavelengthNm, temperatureK) {
  return 1 / (wavelengthNm ** 5 * Math.expm1(1.438776877e7 / (wavelengthNm * temperatureK)));
}

export function binaryParameters(q, eccentricity, inclinationDeg) {
  const massFraction = q / (1 + q);
  const fluxRatio = q ** 1.6 * planck(550, 5800 * Math.sqrt(q)) / planck(550, 5800);
  return {
    q, eccentricity, inclination: inclinationDeg * Math.PI / 180,
    omega: Math.PI / 4, node: Math.PI / 6,
    massFraction, lightFraction: fluxRatio / (1 + fluxRatio), fluxRatio,
    // M1 = 1 solar mass, relative semimajor axis = 1 AU, distance = 100 pc.
    periodYears: Math.sqrt(1 / (1 + q)), masPerAU: 10
  };
}

export function eccentricAnomaly(meanAnomaly, eccentricity) {
  const mean = ((meanAnomaly % TAU) + TAU) % TAU;
  let eccentric = mean;
  for (let iteration = 0; iteration < 20; iteration++) {
    const correction = (eccentric - eccentricity * Math.sin(eccentric) - mean) /
      (1 - eccentricity * Math.cos(eccentric));
    eccentric -= correction;
    if (Math.abs(correction) < 1e-12) break;
  }
  return eccentric;
}

function project(x, y, parameters) {
  const { omega, node, inclination } = parameters;
  const u = x * Math.cos(omega) - y * Math.sin(omega);
  const v = x * Math.sin(omega) + y * Math.cos(omega);
  return [
    u * Math.cos(node) - v * Math.cos(inclination) * Math.sin(node),
    u * Math.sin(node) + v * Math.cos(inclination) * Math.cos(node),
    v * Math.sin(inclination)
  ];
}

export function binaryState(phase, parameters) {
  const { eccentricity: e, periodYears, massFraction: b, lightFraction: beta } = parameters;
  const E = eccentricAnomaly(TAU * phase, e);
  const root = Math.sqrt(1 - e * e);
  const relative = project(Math.cos(E) - e, root * Math.sin(E), parameters);
  const rate = TAU / periodYears / (1 - e * Math.cos(E));
  const velocity = project(-Math.sin(E) * rate, root * Math.cos(E) * rate, parameters);
  return {
    relative, velocity,
    primary: relative.map(component => -b * component),
    secondary: relative.map(component => (1 - b) * component),
    photocentre: relative.map(component => (beta - b) * component * parameters.masPerAU),
    rvPrimary: -b * velocity[2] * AU_PER_YEAR_TO_KMS,
    rvSecondary: (1 - b) * velocity[2] * AU_PER_YEAR_TO_KMS
  };
}
