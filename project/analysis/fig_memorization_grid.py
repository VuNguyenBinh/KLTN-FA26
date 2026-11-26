#!/usr/bin/env python3
"""Per-target memorisation grid for the commercial model (C_ai_api).

Shows, for every target that has a hint-free run, the original outcome and each
hint-free run outcome. This exposes the full per-target data behind the
memorisation claim, far more legible than an aggregate solve-rate bar.

Usage: python fig_memorization_grid.py [results.csv] [out.png]
"""
import csv
import sys
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

CSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "results", "results.csv")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "..", "paper", "figures", "fig_memorization_grid.png")

GREEN = "#3F9E63"   # solved
RED = "#D86B6B"     # failed
GREY = "#E3E6E8"    # not run

rows = [r for r in csv.reader(open(CSV, encoding="utf-8")) if len(r) > 6 and r[0].startswith("XBEN")]
orig, hf = {}, {}
for r in rows:
    bench, arm, variant, run, solved = r[0], r[3], r[4], r[5], r[6]
    bid = bench.replace("XBEN-", "").replace("-24", "")
    if arm != "C_ai_api":
        continue
    if variant == "original":
        orig[bid] = int(solved)
    elif variant == "hintfree":
        hf.setdefault(bid, {})[int(run)] = int(solved)

# keep only targets with hint-free data
benches = sorted(hf.keys())

def hf_solved_any(b):
    return any(v == 1 for v in hf[b].values())

# narrative groups, best evidence first
def group(b):
    o = orig.get(b, 0)
    s = hf_solved_any(b)
    if o == 0 and s:  return (0, "Originally FAILED -> solved hint-free  (reverse of memorisation)")
    if o == 1 and s:  return (1, "Originally solved -> stays solved")
    if o == 1 and not s: return (2, "Originally solved -> drops (hard-XSS craft limit)")
    return (3, "Originally failed -> stays failed (consistency check)")

benches.sort(key=lambda b: (group(b)[0], b))

cols = ["Original", "Hint-free\nrun 1", "Hint-free\nrun 2"]
def cell(b, c):
    if c == 0:
        return orig.get(b, None)
    return hf[b].get(c, None)   # c=1 -> run1, c=2 -> run2

fig, ax = plt.subplots(figsize=(6.4, max(4.0, 0.32 * len(benches) + 1.2)))
for yi, b in enumerate(benches):
    y = len(benches) - 1 - yi
    for ci in range(3):
        v = cell(b, ci)
        color = GREY if v is None else (GREEN if v == 1 else RED)
        ax.add_patch(plt.Rectangle((ci, y), 0.96, 0.9, facecolor=color, edgecolor="white", linewidth=1.5))
        if v is not None:
            ax.text(ci + 0.48, y + 0.45, "✓" if v == 1 else "✗",
                    ha="center", va="center", color="white", fontsize=11, fontweight="bold")

# group separators + labels on the right
prev = None
for yi, b in enumerate(benches):
    y = len(benches) - 1 - yi
    g = group(b)[0]
    if prev is not None and g != prev:
        ax.axhline(y + 0.95, color="#9AA3A8", linewidth=0.8)
    prev = g

ax.set_xlim(-0.05, 3.9)
ax.set_ylim(-0.1, len(benches))
ax.set_xticks([i + 0.48 for i in range(3)])
ax.set_xticklabels(cols, fontsize=9)
ax.set_yticks([len(benches) - 1 - yi + 0.45 for yi in range(len(benches))])
ax.set_yticklabels(["XBEN-" + b for b in benches], fontsize=8)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")

# right-side group brackets/labels
seen = {}
for yi, b in enumerate(benches):
    y = len(benches) - 1 - yi
    gi, gl = group(b)
    seen.setdefault(gi, []).append(y)
short = {0: "reverse (orig fail -> HF solve)", 1: "stays solved", 2: "drops (hard XSS)", 3: "stays failed"}
for gi, ys in seen.items():
    ymid = (min(ys) + max(ys)) / 2 + 0.45
    ax.text(3.05, ymid, short[gi], va="center", ha="left", fontsize=8, color="#3a3a3a")

ax.set_title("Per-target outcome: original vs. hint-removed (commercial model)", fontsize=11, pad=22)
legend = [Patch(facecolor=GREEN, label="solved"), Patch(facecolor=RED, label="failed"),
          Patch(facecolor=GREY, label="not run")]
ax.legend(handles=legend, loc="lower right", bbox_to_anchor=(1.0, -0.12), ncol=3, frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(OUT, dpi=150, bbox_inches="tight")
print("[fig]", OUT, "| targets:", len(benches))
print("groups:", {short[g]: sum(1 for b in benches if group(b)[0] == g) for g in sorted(seen)})

# ---- LANDSCAPE variant (for slides): targets as columns, 3 variant rows ----
OUT_H = OUT.replace(".png", "_h.png")
rows_lab = ["Original", "Hint-free run 1", "Hint-free run 2"]
figh, axh = plt.subplots(figsize=(max(9.0, 0.5 * len(benches) + 1.0), 2.9))
for xi, b in enumerate(benches):
    for r in range(3):
        v = cell(b, r)
        color = GREY if v is None else (GREEN if v == 1 else RED)
        axh.add_patch(plt.Rectangle((xi, 2 - r), 0.92, 0.9, facecolor=color, edgecolor="white", linewidth=1.5))
        if v is not None:
            axh.text(xi + 0.46, 2 - r + 0.45, "✓" if v == 1 else "✗",
                     ha="center", va="center", color="white", fontsize=10, fontweight="bold")
# group separators + labels above
prevg = None
for xi, b in enumerate(benches):
    g = group(b)[0]
    if prevg is not None and g != prevg:
        axh.axvline(xi - 0.04, color="#9AA3A8", linewidth=0.8)
    prevg = g
gseen = {}
for xi, b in enumerate(benches):
    gseen.setdefault(group(b)[0], []).append(xi)
for gi, xs in gseen.items():
    axh.text((min(xs) + max(xs)) / 2 + 0.46, 3.15, short[gi], ha="center", va="bottom", fontsize=8, color="#3a3a3a")
axh.set_xlim(-0.05, len(benches))
axh.set_ylim(-0.1, 3.5)
axh.set_xticks([xi + 0.46 for xi in range(len(benches))])
axh.set_xticklabels([b for b in benches], fontsize=7, rotation=0)
axh.set_yticks([2 - r + 0.45 for r in range(3)])
axh.set_yticklabels(rows_lab, fontsize=8)
axh.tick_params(length=0)
for sp in axh.spines.values():
    sp.set_visible(False)
leg = [Patch(facecolor=GREEN, label="solved"), Patch(facecolor=RED, label="failed"), Patch(facecolor=GREY, label="not run")]
axh.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=3, frameon=False, fontsize=8)
figh.tight_layout()
figh.savefig(OUT_H, dpi=150, bbox_inches="tight")
print("[fig]", OUT_H, "(landscape)")
