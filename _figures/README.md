# Homepage figures

Sources for the four research plates in `assets/img/dunhuang/`, drawn in the
Dunhuang mineral-pigment style defined in `dunhuang_style.py`.

| Plate | Script | Data |
| --- | --- | --- |
| `msms.jpg` | `fig_msms.py` | `msms_cmd.npz`, written by `msms_extract.py` from `~/Project/data/MSMS/msms_36m_v0.hdf5` (golden-sample cuts, q > 0.9) and PARSEC `[M/H] = 0`, log age 10 |
| `imf-alpha.jpg` | `fig_imf.py` | `imf_data.json`, values read off the published Nature 2023 figure |
| `kurucz-a1.jpg` | `fig_kurucz.py` | `kurucz_trace.npz`, written by `trace_kurucz.py` from `assets/img/publication_preview/kurucza1.png` |
| `ifmr.jpg` | `fig_ifmr.py` | `~/Project/WDMS/astrometry/wdforge/result/flow_merger_wdwd_wdnondeg/20260408_161718_ifmr_feh_bins_widebinary_posterior.npz`, via the helpers in `wdforge/runs/plots_post.ipynb` |

Each script takes the working directory (holding `dunhuang_style.py`, the data
files and `fonts/`) and the output path:

```bash
mkdir -p fonts
curl -L -o fonts/EBGaramond.ttf "https://github.com/google/fonts/raw/main/ofl/ebgaramond/EBGaramond%5Bwght%5D.ttf"
curl -L -o fonts/EBGaramond-Italic.ttf "https://github.com/google/fonts/raw/main/ofl/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf"
~/anaconda3/envs/gaia-dr4/bin/python msms_extract.py msms_cmd.npz
python fig_msms.py . msms.png
python fig_imf.py . imf.png
python fig_kurucz.py . kurucz.png
python fig_ifmr.py . ifmr.png
```

The site uses the PNGs resized to 1400 px wide and saved as JPEG (quality 86).
