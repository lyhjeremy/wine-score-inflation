"""
analyze.py - Wine Score Inflation: the 100-point scale that isn't
=================================================================
Using ~130k Wine Enthusiast reviews, we ask what a wine "score" really means:
how compressed the scale is, what a point costs, whether recent vintages score
higher, and how much the reviewer matters.

Outputs: figures/*.png and tables/summary.csv
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
FIG = os.path.join(HERE, "figures"); TAB = os.path.join(HERE, "tables")
INK, GOLD, TEAL, CORAL, PLUM, WINE = "#1a1a2e", "#D4A537", "#15868C", "#E0567A", "#5B4B8A", "#7b1733"
plt.rcParams.update({"figure.dpi": 200, "savefig.dpi": 200, "font.size": 12,
    "axes.edgecolor": "#888", "axes.grid": True, "grid.color": "#e8e2d4",
    "axes.axisbelow": True, "figure.facecolor": "white", "axes.facecolor": "white"})


def load():
    df = pd.read_csv(os.path.join(HERE, "data", "winemag-data-130k-v2.csv"))
    df["points"] = pd.to_numeric(df["points"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["vintage"] = df["title"].str.extract(r"(19\d\d|20[01]\d)").astype(float)
    return df.dropna(subset=["points"])


def main():
    os.makedirs(FIG, exist_ok=True); os.makedirs(TAB, exist_ok=True)
    df = load()
    n = len(df)
    pmin, pmean, pmed = df.points.min(), df.points.mean(), df.points.median()
    share = ((df.points >= 84) & (df.points <= 92)).mean() * 100
    print(f"Reviews: {n:,}")
    print(f"Points: min {pmin:.0f}, mean {pmean:.2f}, median {pmed:.0f}")
    print(f"Share scoring 84-92: {share:.1f}%")

    # ---- Fig 1: the compressed distribution ----
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    bins = np.arange(79.5, 101.5, 1)
    ax.hist(df.points, bins=bins, color=WINE, alpha=0.88, rwidth=0.9)
    ax.axvspan(83.5, 92.5, color=GOLD, alpha=0.12)
    ax.axvline(80, color=INK, ls="--", lw=2)
    ax.text(80.2, ax.get_ylim()[1]*0.92, " hard floor at 80\n (nothing lower is published)", fontsize=10, va="top")
    ax.text(88, ax.get_ylim()[1]*0.6, f"{share:.0f}% of all wines\nscore 84–92", ha="center", color="#7a5", fontsize=11, weight="bold")
    ax.set_xlabel("Points (the '100-point' scale)"); ax.set_ylabel("Number of wines")
    ax.set_title("A 100-point scale that's really an 8-point scale", color=INK, weight="bold")
    fig.tight_layout(); fig.savefig(f"{FIG}/01_distribution.png"); plt.close(fig)

    # ---- Fig 2: price buys points, with diminishing returns ----
    d = df.dropna(subset=["price"])
    d = d[(d.price >= 4) & (d.price <= 500)]
    d["lp"] = np.log10(d.price)
    bins = pd.qcut(d.price, 20, duplicates="drop")
    g = d.groupby(bins, observed=True).agg(price=("price", "median"), points=("points", "mean"))
    r = stats.pearsonr(d.lp, d.points)[0]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(g.price, g.points, "-o", color=WINE, lw=2.4, ms=6)
    ax.set_xscale("log")
    ax.set_xlabel("Price (USD, log scale)"); ax.set_ylabel("Average points")
    ax.set_title("Money buys points — but with steep diminishing returns", color=INK, weight="bold")
    ax.text(0.05, 0.9, f"points vs log(price): r = {r:.2f}", transform=ax.transAxes, fontsize=11)
    p10, p100 = d[d.price.between(9, 11)].points.mean(), d[d.price.between(90, 110)].points.mean()
    fig.tight_layout(); fig.savefig(f"{FIG}/02_price_vs_points.png"); plt.close(fig)
    print(f"~$10 wine avg: {p10:.1f} pts | ~$100 wine avg: {p100:.1f} pts | r(points,log price)={r:.2f}")

    # ---- Fig 3: mean points by vintage ----
    v = df[(df.vintage >= 1995) & (df.vintage <= 2016)]
    gv = v.groupby("vintage")["points"].mean()
    sl, ic, rv, pv, _ = stats.linregress(gv.index, gv.values)
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.plot(gv.index, gv.values, "-o", color=TEAL, lw=2.2, ms=5)
    ax.plot(gv.index, ic + sl*gv.index, color=INK, ls="--", lw=1.8, label=f"+{sl:.03f} pts/yr (r={rv:.2f})")
    ax.set_xlabel("Vintage year"); ax.set_ylabel("Average points")
    ax.set_title("Average score barely moves across vintages", color=INK, weight="bold"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/03_by_vintage.png"); plt.close(fig)
    print(f"Vintage trend: {sl*10:.2f} pts per decade (r={rv:.2f})")

    # ---- Fig 4: reviewer leniency ----
    top = df.taster_name.value_counts().head(10).index
    gt = df[df.taster_name.isin(top)].groupby("taster_name")["points"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8.6, 5))
    ax.barh(range(len(gt)), gt.values - 80, left=80, color=PLUM, alpha=0.85)
    ax.set_yticks(range(len(gt))); ax.set_yticklabels(gt.index, fontsize=10)
    ax.set_xlim(80, gt.max()+0.6); ax.set_xlabel("Average points awarded")
    ax.set_title("Some reviewers are simply more generous", color=INK, weight="bold")
    for i, v_ in enumerate(gt.values): ax.text(v_+0.05, i, f"{v_:.1f}", va="center", fontsize=9)
    fig.tight_layout(); fig.savefig(f"{FIG}/04_by_taster.png"); plt.close(fig)
    print(f"Reviewer spread: {gt.min():.1f} to {gt.max():.1f} ({gt.max()-gt.min():.1f} pts)")

    pd.DataFrame({"metric": ["reviews", "points_min", "points_mean", "share_84_92",
                             "avg_$10", "avg_$100", "r_points_logprice",
                             "vintage_pts_per_decade", "reviewer_min", "reviewer_max"],
                  "value": [n, pmin, round(pmean, 2), round(share, 1),
                            round(p10, 1), round(p100, 1), round(r, 2),
                            round(sl*10, 2), round(gt.min(), 1), round(gt.max(), 1)]}
                 ).to_csv(f"{TAB}/summary.csv", index=False)
    print("\nSaved figures + tables/summary.csv")


if __name__ == "__main__":
    main()
