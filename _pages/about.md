---
layout: about
title: about
permalink: /
subtitle: <a href='#'>Max-Planck-Institut für Astronomie</a>.

profile:
  align: right
  image: jdli_sicily.jpg
  image_circular: false # crops the image to make it circular
  address: >
    <p>    Sicily, 2025</p>

news: false  # includes a list of news items
selected_papers: false # disabled for GitHub Pages compatibility
social: true  # includes social icons at the bottom of the page
---
My research focuses on understanding the intricacies of star formation and stellar physics, leveraging extensive datasets. I employ advanced methodologies, including machine learning techniques, statistical inference, and predictive modeling, to analyze data from leading astronomical surveys such as SDSS-V/APOGEE, Gaia, LAMOST, and CSST. **Specifically, my work centers on the identification and statistical analysis of binary stars, the stellar initial mass function (**IMF**), and the physics of stellar atmosphere models.** These areas are fundamental to my broader investigation into stellar populations and the assembly history of the Milky Way.

I was born in Benxi, a small city in Northeast China. When the People's Republic was founded, this place was a powerhouse of steel and coal. Winters here bite with bitter cold, but come autumn, the hillsides blaze with maple leaves in breathtaking beauty.

After finishing high school in Benxi, I moved to Beijing to study astronomy at Beijing Normal University (BNU), home to one of China's oldest astronomy departments. Later, I pursued my PhD at the National Astronomical Observatories of China (NAOC), Chinese Academy of Sciences, under the guidance of Professor Liu Chao. During my doctoral studies, I spent time as a visiting researcher at the Flatiron Institute in New York.
In the winter of 2023, I made my way to Heidelberg to begin my postdoctoral journey at MPIA, working alongside Professor Hans-Walter Rix.

## Selected Publications

<div class="publications">
  <div class="publication">
    <strong>Millions of Main-Sequence Binary Stars from Gaia BP/RP Spectra</strong><br>
    <em class="author-highlight">Li, Jiadong</em>, Rix, Hans-Walter, Ting, Yuan-Sen, Müller-Horn, Johanna, El-Badry, Kareem, Liu, Chao, Seeburger, Rhys, Green, Gregory M., Zhang, Xiangyu<br>
    <em>arXiv e-prints</em>, arXiv:2507.09622 (2025)<br>
    <a href="https://ui.adsabs.harvard.edu/abs/2025arXiv250709622L" target="_blank">ADS</a> |
    <a href="https://arxiv.org/abs/2507.09622" target="_blank">arXiv</a>
  </div>

  <div class="publication">
    <strong>Differentiable Stellar Atmospheres with Physics-Informed Neural Networks</strong><br>
    <em class="author-highlight">Li, Jiadong</em>, Jian, Mingjie, Ting, Yuan-Sen, Green, Gregory M.<br>
    <em>arXiv e-prints</em>, arXiv:2507.06357 (2025)<br>
    <a href="https://ui.adsabs.harvard.edu/abs/2025arXiv250706357L" target="_blank">ADS</a> |
    <a href="https://arxiv.org/abs/2507.06357" target="_blank">arXiv</a>
  </div>

  <div class="publication">
    <strong>Identification of 30,000 White Dwarf-Main Sequence binaries candidates from Gaia DR3 BP/RP(XP) low-resolution spectra</strong><br>
    <em class="author-highlight">Li, Jiadong</em>, Ting, Yuan-Sen, Rix, Hans-Walter, Green, Gregory M., Hogg, David W., Ren, Juan-Juan, Müller-Horn, Johanna, Seeburger, Rhys<br>
    <em>arXiv e-prints</em>, arXiv:2501.14494 (2025)<br>
    <a href="https://ui.adsabs.harvard.edu/abs/2025arXiv250114494L" target="_blank">ADS</a> |
    <a href="https://arxiv.org/abs/2501.14494" target="_blank">arXiv</a>
  </div>

  <div class="publication">
    <strong>AspGap: Augmented Stellar Parameters and Abundances for 37 Million Red Giant Branch Stars from Gaia XP Low-resolution Spectra</strong><br>
    <em class="author-highlight">Li, Jiadong</em>, Wong, Kaze W. K., Hogg, David W., Rix, Hans-Walter, Chandra, Vedant<br>
    <em>ApJS</em>, 272, 2 (2024)<br>
    <a href="https://ui.adsabs.harvard.edu/abs/2024ApJS..272....2L" target="_blank">ADS</a> |
    <a href="https://arxiv.org/abs/2309.14294" target="_blank">arXiv</a>
  </div>

  <div class="publication">
    <strong>Stellar initial mass function varies with metallicity and time</strong><br>
    <em class="author-highlight">Li, Jiadong</em>, Liu, Chao, Zhang, Zhi-Yu, Tian, Hao, Fu, Xiaoting, Li, Jiao, Yan, Zhi-Qiang<br>
    <em>Nature</em>, 613, 460-462 (2023)<br>
    <a href="https://ui.adsabs.harvard.edu/abs/2023Natur.613..460L" target="_blank">ADS</a> |
    <a href="https://arxiv.org/abs/2301.07029" target="_blank">arXiv</a>
  </div>

  <div class="publication">
    <strong>Stellar Parameterization of LAMOST M Dwarf Stars</strong><br>
    <em class="author-highlight">Li, Jiadong</em>, Liu, Chao, Zhang, Bo, Tian, Hao, Qiu, Dan, Tian, Haijun<br>
    <em>ApJS</em>, 253, 45 (2021)<br>
    <a href="https://ui.adsabs.harvard.edu/abs/2021ApJS..253...45L" target="_blank">ADS</a> |
    <a href="https://arxiv.org/abs/2012.14080" target="_blank">arXiv</a>
  </div>
</div>

<style>
.publication {
  margin-bottom: 1.5em;
  padding: 1em;
  border-left: 3px solid var(--global-theme-color);
  background-color: var(--global-card-bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

html[data-theme='dark'] .publication {
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.publication:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

html[data-theme='dark'] .publication:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

.publication strong {
  color: var(--global-theme-color);
}

.publication em {
  font-style: normal;
  font-weight: bold;
  color: var(--global-text-color);
}

/* Highlight Li, Jiadong name in pink for dark mode */
.author-highlight {
  color: #ff69b4 !important;
  background-color: rgba(255, 105, 180, 0.1);
  padding: 2px 4px;
  border-radius: 3px;
}

/* Only apply in dark mode */
html[data-theme='light'] .author-highlight {
  color: var(--global-text-color) !important;
  background-color: transparent;
  padding: 0;
}

.publication a {
  color: var(--global-theme-color);
  text-decoration: none;
}

.publication a:hover {
  color: var(--global-hover-color);
  text-decoration: underline;
}
</style>