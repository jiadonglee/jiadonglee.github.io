import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
sys.path.insert(0, sys.argv[1]); import dunhuang_style as D
D.use()
d = json.load(open(sys.argv[1] + "/imf_data.json"))
fig, ax = plt.subplots(figsize=(8.0, 6.2))
D.paper(fig)
ax.axvspan(-0.5, 0.1, color=D.PALE, alpha=0.75, lw=0, zorder=0)
ax.axvspan(-0.5, 0.1, facecolor="none", edgecolor=D.SAND, hatch="||||", lw=0, alpha=0.35, zorder=0.05)
for y, lab, dy in ((2.35, r"Salpeter  $\alpha = 2.35$", 0.04), (2.3, r"Kroupa  $\alpha_2 = 2.3$", -0.105), (1.3, r"Kroupa  $\alpha_1 = 1.3$", 0.04)):
    ax.axhline(y, color=D.LINE, lw=0.9, ls=(0, (5, 3)), zorder=0.5)
    ax.text(-0.935, y + dy, lab, fontsize=16, color=D.INK, style="italic", zorder=6)
for key, col in (("hot_line", D.RED), ("cold_line", D.TEAL)):
    x = np.array([p["x"] for p in d[key]]); lo = np.array([p["lo"] for p in d[key]])
    hi = np.array([p["hi"] for p in d[key]]); ln = np.array([p["line"] for p in d[key]])
    ax.fill_between(x, lo, hi, color=col, alpha=0.2, lw=0, zorder=1)
    ax.fill_between(x, lo, hi, facecolor="none", edgecolor=col, hatch="|||", lw=0, alpha=0.18, zorder=1.05)
    ax.plot(x, lo, color=col, lw=0.6, alpha=0.6, zorder=1.1); ax.plot(x, hi, color=col, lw=0.6, alpha=0.6, zorder=1.1)
    ax.plot(x, ln, color=col, lw=4.5, alpha=0.25, zorder=2); ax.plot(x, ln, color=col, lw=1.8, zorder=2.1)
def pts(key, fmt, fc, ec, ms, dx=0.0, z=4):
    p = d[key]; x = np.array([q["x"] for q in p]) + dx
    ax.errorbar(x, [q["y"] for q in p], yerr=[q["err"] for q in p], fmt=fmt, ms=ms, mfc=fc, mec=ec, mew=1.0,
                ecolor=ec, elinewidth=1.3, capsize=0, zorder=z)
pts("all", "s", "#7C7466", D.INK, 7.5, z=3.5)
pts("hot", "o", D.RED, "#6E2F22", 8.5)
pts("cold", "^", D.TEAL, D.TEAL_DEEP, 9)
ax.set_xlim(-0.95, 0.42); ax.set_ylim(1.2, 3.0)
ax.set_xlabel("[M/H]"); ax.set_ylabel(r"IMF power-law exponent  $\alpha$")
ax.set_xticks([-0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4])
ax.set_xticklabels([f"{t:+.1f}".replace("-", "−").replace("+0.0", "0.0") for t in ax.get_xticks()])
h = [Line2D([0], [0], color=D.RED, lw=1.8, label="Hot, binary-corrected"),
     Line2D([0], [0], color=D.TEAL, lw=1.8, label="Cold, binary-corrected"),
     Line2D([0], [0], marker="s", lw=0, mfc="#7C7466", mec=D.INK, ms=7.5, label="All stars"),
     Line2D([0], [0], marker="o", lw=0, mfc=D.RED, mec="#6E2F22", ms=8.5, label="Dynamically hot stars"),
     Line2D([0], [0], marker="^", lw=0, mfc=D.TEAL, mec=D.TEAL_DEEP, ms=9, label="Dynamically cold stars")]
ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, handlelength=1.5, columnspacing=1.4, labelspacing=0.55)
D.save(fig, sys.argv[2])
