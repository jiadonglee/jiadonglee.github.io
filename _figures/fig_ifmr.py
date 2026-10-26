import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap, BoundaryNorm
sys.path.insert(0, sys.argv[1])
import dunhuang_style as D

NB = "/Users/jdli/Project/WDMS/astrometry/wdforge/runs/plots_post.ipynb"
src = "".join([c for c in json.load(open(NB))["cells"] if c["cell_type"] == "code"][0]["source"])
src = src.replace("PAPER_FIG_DIR.mkdir(parents=True, exist_ok=True)", "")
src = src.replace("    plt.style.use(STYLE_PATH)", "    pass")
src = src.replace("CMAP = mcm.colormaps[CMAP_NAME] if hasattr(mcm, 'colormaps') else mcm.get_cmap(CMAP_NAME)", "CMAP = matplotlib.colormaps[CMAP_NAME]")
ns = {"matplotlib": matplotlib}
exec(src, ns)
D.use()

pack = ns["load_pack"](ns["MERGER_POSTERIOR"], ns["MERGER_POSTPRED"])
print("posterior:", ns["MERGER_POSTERIOR"])
mi = np.linspace(0.8, 8.0, 220)
p16, p50, p84 = ns["make_ifmr_prior_band"](mi)

fig, ax = plt.subplots(figsize=(6.8, 5.0))
D.paper(fig)
ax.fill_between(mi, p16, p84, color=D.SAND, alpha=0.45, lw=0, zorder=0)
ax.fill_between(mi, p16, p84, facecolor="none", edgecolor=D.PALE, hatch="|||||", lw=0, alpha=0.22, zorder=0.1)
ax.plot(mi, p50, color=D.LINE, lw=1.4, ls=(0, (4, 3)), zorder=1)

s, centers = pack["samples"], pack["centers"]
has_free_a4 = "a4" in s and not np.allclose(np.asarray(s["a4"]), np.asarray(s["a3"]))
idx = np.arange(s["a1"].shape[0])
colors = D.FEH_COLORS
for i in range(pack["k"]):
    curves = np.array([ns["ifmr_cunningham_numpy"](mi, s["a1"][j, i], s["a2"][j, i], s["a3"][j, i],
                       s["a4"][j, i] if has_free_a4 else s["a3"][j, i], s["b1"][j, i]) for j in idx])
    lo, med, hi = np.percentile(curves, [16, 50, 84], axis=0)
    ax.fill_between(mi, lo, hi, color=colors[i], alpha=0.16, lw=0, zorder=2)
    ax.plot(mi, med, color=colors[i], lw=4.2, alpha=0.35, zorder=3)
    ax.plot(mi, med, color=colors[i], lw=2.0, zorder=3.1)

C = ns
ax.errorbar(C["C22_INIT_MASS"], C["C22_FINAL_MASS"], xerr=np.vstack([C["C22_INIT_ERR_LO"], C["C22_INIT_ERR_HI"]]),
            yerr=np.vstack([C["C22_FINAL_ERR_LO"], C["C22_FINAL_ERR_HI"]]), fmt="s", ms=6, mfc=D.INK, mec=D.PALE, mew=0.8,
            ecolor=D.INK, elinewidth=1.0, capsize=0, zorder=5)
ax.errorbar(C["MILLER26_FULL1_INIT"], C["MILLER26_FULL1_FINAL"],
            xerr=np.vstack([C["MILLER26_FULL1_INIT_ERR_LO"], C["MILLER26_FULL1_INIT_ERR_HI"]]),
            yerr=np.vstack([C["MILLER26_FULL1_FINAL_ERR_LO"], C["MILLER26_FULL1_FINAL_ERR_HI"]]), fmt="^", ms=7,
            mfc=D.GROUND, mec=D.INK, mew=1.0, ecolor=D.INK, elinewidth=0.9, capsize=0, zorder=5)

ax.set_xlim(0.8, 8.3); ax.set_ylim(0.45, 1.45)
ax.set_xlabel(r"Initial mass  [$M_\odot$]")
ax.set_ylabel(r"White dwarf mass  [$M_\odot$]")
handles = [Line2D([0], [0], color=D.SAND, lw=9, alpha=0.6, label="Prior 68%"),
           Line2D([0], [0], color=D.LINE, lw=1.4, ls=(0, (4, 3)), label="Prior median"),
           Line2D([0], [0], marker="s", color=D.INK, lw=0, ms=6, label="Cunningham+24"),
           Line2D([0], [0], marker="^", mfc=D.GROUND, mec=D.INK, lw=0, ms=7, label="Miller+26 full fit")]
ax.legend(handles=handles, loc="upper left", handlelength=1.6)

edges = np.asarray(pack["edges"], float)
cmap = ListedColormap(colors); norm = BoundaryNorm(edges, cmap.N)
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap); sm.set_array([])
cb = fig.colorbar(sm, ax=ax, boundaries=edges, ticks=centers, spacing="proportional", fraction=0.045, pad=0.03)
cb.set_label("[Fe/H]"); cb.ax.set_yticklabels([f"{c:+.1f}".replace("-", "−") for c in centers])
cb.outline.set_edgecolor(D.LINE); cb.ax.tick_params(color=D.LINE, length=3)
D.save(fig, sys.argv[2])
