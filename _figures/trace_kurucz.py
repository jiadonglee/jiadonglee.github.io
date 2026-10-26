import numpy as np, sys
from PIL import Image
SRC = '/Users/jdli/Project/jdli_page/jiadonglee.github.io/assets/img/publication_preview/kurucza1.png'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(float)
H, W, _ = a.shape
boxes = [(1248, 1741, 329, 438), (1361, 1741, 610, 651), (1431, 1741, 788, 864)]
inbox = np.zeros((H, W), bool)
for c0, c1, r0, r1 in boxes:
    inbox[r0 + 4:r1 - 3, c0 + 4:c1 - 3] = True
un = np.where(inbox[..., None], 255 - (255 - a) / 0.2, a)   # undo the legend's 80% white veil
un = np.clip(un, 0, 255)
mx, mn = un.max(-1), un.min(-1); chroma = mx - mn
r, g, b = un[..., 0], un[..., 1], un[..., 2]
hue = np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) % 360
lum = un.sum(-1)
col = chroma > 28
B = col & (hue > 190) & (hue < 235)
O = col & (hue > 15) & (hue < 45) & (lum > 470)
Br = col & (hue > 15) & (hue < 45) & (lum <= 470)
G = col & (hue > 95) & (hue < 150)
Ol = col & (hue >= 50) & (hue <= 90)
# legend handles are drawn on top of the veil: drop them
for c0, c1, r0, r1 in boxes:
    inbox[r0:r1, c0:c0 + 75] = True
    for m in (B, O, Br, G, Ol):
        m[r0:r1, c0:c0 + 75] = False

X = lambda c: 5160 + (c - 160) * 70 / (1750 - 160)
panels = {'top': (26, 447, 59.5, 413.5, 1.0, 0.0), 'mid': (451, 660, 484.5, 626.5, 0.1, -0.1),
          'bot': (664, 872, 697.5, 839.5, 0.1, -0.1)}
def Yf(p, rr):
    _, _, ra, rb, va, vb = panels[p]; return va + (rr - ra) * (vb - va) / (rb - ra)

def envelope(mask, p):
    r0, r1 = panels[p][:2]
    lo = np.full(W, np.nan); hi = np.full(W, np.nan)
    for c in range(162, 1749):
        rows = np.where(mask[r0:r1, c])[0]
        if len(rows): lo[c], hi[c] = rows.min() + r0, rows.max() + r0
    return lo, hi

def fill_gaps(lo, hi, maxgap):
    idx = np.arange(W); ok = np.isfinite(lo)
    out_lo, out_hi = lo.copy(), hi.copy()
    if ok.sum() < 2: return out_lo, out_hi
    good = idx[ok]
    for i in range(len(good) - 1):
        s, e = good[i], good[i + 1]
        if 1 < e - s <= maxgap:
            out_lo[s:e] = np.interp(idx[s:e], [s, e], [lo[s], lo[e]])
            out_hi[s:e] = np.interp(idx[s:e], [s, e], [hi[s], hi[e]])
    return out_lo, out_hi

res = {}
atlas = envelope(O | Br | Ol, 'top'); a1 = envelope(B | Br, 'top'); obs = envelope(G | Ol, 'top')
atlas = fill_gaps(*atlas, 40)
for k, (lo, hi) in (('a1', a1), ('obs', obs)):
    lo, hi = fill_gaps(lo, hi, 14 if k == 'obs' else 6)
    miss = ~np.isfinite(lo)
    lo[miss], hi[miss] = atlas[0][miss], atlas[1][miss]
    res[k] = (lo, hi)
res['atlas'] = atlas
mid = fill_gaps(*envelope(B, 'mid'), 40)
bot_a1 = envelope(B | Br, 'bot'); bot_at = fill_gaps(*envelope(O | Br, 'bot'), 40)
lo, hi = fill_gaps(*bot_a1, 6); miss = ~np.isfinite(lo); lo[miss], hi[miss] = bot_at[0][miss], bot_at[1][miss]
cols = np.arange(162, 1749); wl = X(cols)
out = dict(wl=wl)
for key, p, (lo, hi) in (('top_a1', 'top', res['a1']), ('top_atlas', 'top', res['atlas']), ('top_obs', 'top', res['obs']),
                         ('mid', 'mid', mid), ('bot_a1', 'bot', (lo, hi)), ('bot_atlas', 'bot', bot_at)):
    l, h = lo[cols], hi[cols]
    out[key + '_lo'] = Yf(p, h); out[key + '_hi'] = Yf(p, l)   # rows grow downward
    print(key, 'missing', int(np.isnan(l).sum()))
np.savez(sys.argv[1], **out)
