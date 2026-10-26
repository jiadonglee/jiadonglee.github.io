"""Matplotlib style for Dunhuang mineral-pigment plates."""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap, to_rgb

HERE = os.path.dirname(os.path.abspath(__file__))
for f in ("EBGaramond.ttf", "EBGaramond-Italic.ttf"):
    fm.fontManager.addfont(os.path.join(HERE, "fonts", f))

GROUND = "#E9DCC0"     # plate ground
PALE = "#F1E8D6"       # pale highlight wash
OCHRE = "#C99A55"      # earth yellow
SAND = "#D8BC86"
TEAL = "#3F8C88"       # malachite / azurite green-blue
TEAL_DEEP = "#2C6566"
CELADON = "#9DBFAF"
RED = "#A9533C"        # cinnabar / terracotta
RED_SOFT = "#C17B62"
INK = "#3A3830"
LINE = "#8C7A5B"       # brown line work

TEAL_CMAP = LinearSegmentedColormap.from_list("teal", [GROUND, CELADON, TEAL, TEAL_DEEP])
RED_CMAP = LinearSegmentedColormap.from_list("red", [GROUND, "#E2B79C", RED_SOFT, RED, "#7E3A2A"])
FEH_COLORS = [TEAL_DEEP, CELADON, OCHRE, RED_SOFT, RED]


def use():
    mpl.rcParams.update({
        "figure.facecolor": GROUND,
        "axes.facecolor": GROUND,
        "savefig.facecolor": GROUND,
        "font.family": "EB Garamond",
        "mathtext.fontset": "custom",
        "mathtext.rm": "EB Garamond",
        "mathtext.it": "EB Garamond:italic",
        "mathtext.bf": "EB Garamond:bold",
        "font.size": 19,
        "axes.labelsize": 20,
        "axes.edgecolor": LINE,
        "axes.labelcolor": INK,
        "axes.linewidth": 1.1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": LINE,
        "ytick.color": LINE,
        "xtick.labelcolor": INK,
        "ytick.labelcolor": INK,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 5,
        "ytick.major.size": 5,
        "xtick.minor.visible": False,
        "ytick.minor.visible": False,
        "legend.frameon": False,
        "legend.fontsize": 17,
        "lines.solid_capstyle": "round",
        "lines.dash_capstyle": "round",
        "hatch.linewidth": 0.45,
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.25,
    })


def paper(fig, seed=3):
    """Mark the figure for a paper texture, applied to the saved raster."""
    fig._paper_seed = seed


def _texture(path, seed, strength=0.05):
    from PIL import Image, ImageDraw
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float) / 255
    h, w = a.shape[:2]
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, 1, (h, w))
    grain = (grain + np.roll(grain, 1, 1) + np.roll(grain, -1, 1)) / 3
    a *= 1 - strength * np.clip(grain, 0, None)[..., None] * np.array([0.6, 0.7, 0.9])
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    for _ in range(int(w * h / 5000)):
        x0, y0 = rng.uniform(0, w), rng.uniform(0, h)
        L, t = rng.uniform(10, 60), rng.uniform(0, np.pi)
        dr.line([(x0, y0), (x0 + L * np.cos(t), y0 + L * np.sin(t))],
                fill=(140, 122, 91, int(rng.uniform(18, 46))), width=1)
    im = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    im.save(path, optimize=True)


def strata(ax, x, lo, hi, color, n=4, alpha=0.55, edge=None, zorder=1):
    """A band painted as stacked mineral layers with fine brush striations."""
    base = np.array(to_rgb(color))
    pale = np.array(to_rgb(PALE))
    for i in range(n):
        f0, f1 = i / n, (i + 1) / n
        c = base * (0.55 + 0.45 * (1 - f0)) + pale * (0.45 * f0)
        y0 = lo + (hi - lo) * f0
        y1 = lo + (hi - lo) * f1
        ax.fill_between(x, y0, y1, color=np.clip(c, 0, 1), alpha=alpha, lw=0, zorder=zorder)
    ax.fill_between(x, lo, hi, facecolor="none", edgecolor=PALE, hatch="|||||", lw=0,
                    alpha=0.35, zorder=zorder + 0.1)
    ec = edge or color
    ax.plot(x, lo, color=ec, lw=0.8, alpha=0.8, zorder=zorder + 0.2)
    ax.plot(x, hi, color=ec, lw=0.8, alpha=0.8, zorder=zorder + 0.2)


def save(fig, path):
    fig.savefig(path)
    seed = getattr(fig, "_paper_seed", None)
    plt.close(fig)
    if seed is not None:
        _texture(path, seed)
