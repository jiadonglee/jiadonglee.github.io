import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, sys.argv[1]); import dunhuang_style as D
D.use()
d = np.load(sys.argv[1] + "/kurucz_trace.npz"); wl = d["wl"]
def env(ax, k, color, alpha=1.0, z=2):
    lo, hi = d[k + "_lo"], d[k + "_hi"]
    thin = (hi - lo) < 1e-9
    ax.fill_between(wl, lo, hi, color=color, alpha=alpha, lw=0, zorder=z)
    ax.plot(wl, 0.5 * (lo + hi), color=color, alpha=alpha, lw=0.5, zorder=z)

fig, axs = plt.subplots(3, 1, figsize=(8.0, 6.2), sharex=True,
                        gridspec_kw=dict(height_ratios=[2.0, 1.0, 1.0], hspace=0.08))
D.paper(fig)
ax = axs[0]
obs_mid = 0.5 * (d["top_obs_lo"] + d["top_obs_hi"])
ax.fill_between(wl, obs_mid, 1.0, where=obs_mid < 1.0, color=D.CELADON, alpha=0.35, lw=0, zorder=0.5)
ax.fill_between(wl, obs_mid, 1.0, where=obs_mid < 1.0, facecolor="none", edgecolor=D.PALE, hatch="|||", lw=0, alpha=0.4, zorder=0.6)
ax.axhline(1.0, color=D.LINE, lw=0.7, ls=(0, (3, 3)), zorder=0.4)
env(ax, "top_obs", D.INK, 0.85, 1.5)
env(ax, "top_a1", D.TEAL, 0.9, 2)
env(ax, "top_atlas", D.RED, 0.7, 2.5)
ax.set_ylim(-0.05, 1.08); ax.set_ylabel("Normalised flux")
ax.legend(handles=[Line2D([0], [0], color=D.TEAL, lw=2, label="Kurucz-a1"),
                   Line2D([0], [0], color=D.RED, lw=2, label="Kurucz-ATLAS"),
                   Line2D([0], [0], color=D.INK, lw=2, label="Observed Sun")],
          loc="lower left", ncol=3, bbox_to_anchor=(0.0, 1.0), handlelength=1.4, columnspacing=1.6)
for ax, keys, lab in ((axs[1], [("mid", D.TEAL, 0.9)], "a1 − ATLAS"),
                      (axs[2], [("bot_atlas", D.RED, 0.75), ("bot_a1", D.TEAL, 0.85)], "Model − obs.")):
    ax.axhline(0, color=D.LINE, lw=0.7, ls=(0, (3, 3)), zorder=0.4)
    ax.axhspan(-0.15, 0.15, color=D.PALE, alpha=0.35, lw=0, zorder=0)
    for k, c, al in keys: env(ax, k, c, al)
    ax.set_ylim(-0.15, 0.15); ax.set_yticks([-0.1, 0, 0.1])
    ax.set_yticklabels(["−0.1", "0", "0.1"])
    ax.text(0.995, 0.9, lab, transform=ax.transAxes, ha="right", va="top", fontsize=16, style="italic", color=D.INK, zorder=6,
            bbox=dict(boxstyle="square,pad=0.25", fc=D.GROUND, ec="none", alpha=0.9))
axs[2].set_xlim(5160, 5230); axs[2].set_xlabel("Wavelength  [Å]")
D.save(fig, sys.argv[2])
