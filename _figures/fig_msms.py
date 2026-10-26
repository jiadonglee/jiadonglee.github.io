import sys, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter
sys.path.insert(0, sys.argv[1]); import dunhuang_style as D
D.use()
d = np.load(sys.argv[1] + "/msms_cmd.npz")
xb, yb = np.linspace(0, 4, 321), np.linspace(4, 15, 441)

def density(x, y, smooth=1.2):
    H, _, _ = np.histogram2d(x, y, bins=[xb, yb]); H = gaussian_filter(H.T, smooth)
    return np.log10(H + 1)

hs = density(d["sin_br0"], d["sin_g0"]); hb = density(d["bin_br0"], d["bin_g0"])
xc, yc = 0.5 * (xb[1:] + xb[:-1]), 0.5 * (yb[1:] + yb[:-1])

iso = pd.read_csv("/Users/jdli/Project/data/stellar_model/PARSEC_logage_10_MH_n2p5_0p6.csv",
                  usecols=["MH", "label", "Mini", "Gmag", "G_BPmag", "G_RPmag"])
mh0 = iso.MH.iloc[(iso.MH - 0).abs().argsort().iloc[0]]
iso = iso[(iso.MH == mh0) & (iso.label == 1) & (iso.Mini < 1.0)].sort_values("Mini")
ic, ig = iso.G_BPmag - iso.G_RPmag, iso.Gmag

fig, ax = plt.subplots(figsize=(5.6, 6.0))
D.paper(fig)
ls = np.linspace(0.6, hs.max(), 7)
ax.contourf(xc, yc, hs, levels=ls, cmap=D.TEAL_CMAP, alpha=0.95, zorder=1)
ax.contour(xc, yc, hs, levels=ls, colors=[D.TEAL_DEEP], linewidths=0.55, alpha=0.7, zorder=1.2)
lb = np.linspace(0.45, hb.max(), 6)
ax.contourf(xc, yc, hb, levels=lb, cmap=D.RED_CMAP, alpha=0.9, zorder=2)
ax.contour(xc, yc, hb, levels=lb, colors=["#7E3A2A"], linewidths=0.55, alpha=0.75, zorder=2.2)
ax.plot(ic, ig, color=D.OCHRE, lw=1.8, zorder=3)
ax.plot(ic, ig - 2.5 * np.log10(2), color=D.OCHRE, lw=1.8, ls=(0, (5, 3)), zorder=3)
ax.set_xlim(0, 4); ax.set_ylim(14.5, 4)
ax.set_xlabel(r"$(B-R)_0$"); ax.set_ylabel(r"$M_{G,0}$")
ax.legend(handles=[Patch(color=D.TEAL, label="Single stars"), Patch(color=D.RED, label="Binary stars, q > 0.9"),
                   Line2D([0], [0], color=D.OCHRE, lw=1.8, label="PARSEC [M/H] = 0"),
                   Line2D([0], [0], color=D.OCHRE, lw=1.8, ls=(0, (5, 3)), label="Equal-mass binary")],
          loc="lower left", handlelength=1.5)
D.save(fig, sys.argv[2])
print("MH used", mh0, len(d["bin_g0"]), len(d["sin_g0"]))
