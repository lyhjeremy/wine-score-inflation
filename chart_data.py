"""chart_data.py - small aggregates behind the interactive charts on the write-up page.

Reads the same data/winemag-data-130k-v2.csv as analyze.py (fetch it with
fetch_data.py first) and applies the same filters, so nothing here changes a
published number. Writes tables/chart_data.json:
  hist     score -> number of reviews, 80 to 100
  price    20 equal-count price bins, $4 to $500: median price, mean points, n,
           lower and upper bin edge
  vintage  1995 to 2016: mean points and n per vintage year
  tasters  the ten tasters with the most reviews: mean points and n
"""
import json
import os

import numpy as np
import pandas as pd

from analyze import load

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    df = load()
    hist = df.points.value_counts().sort_index()
    d = df.dropna(subset=["price"])
    d = d[(d.price >= 4) & (d.price <= 500)]
    bins = pd.qcut(d.price, 20, duplicates="drop")
    g = d.groupby(bins, observed=True).agg(price=("price", "median"), points=("points", "mean"),
                                           n=("points", "size"))
    v = df[(df.vintage >= 1995) & (df.vintage <= 2016)]
    gv = v.groupby("vintage")["points"].agg(["mean", "size"])
    top = df.taster_name.value_counts().head(10).index
    gt = df[df.taster_name.isin(top)].groupby("taster_name")["points"].agg(["mean", "size"]).sort_values("mean")
    out = {
        "hist": [[int(k), int(n)] for k, n in hist.items()],
        "price": [[round(float(r.price), 2), round(float(r.points), 3), int(r.n),
                   round(float(iv.left), 2), round(float(iv.right), 2)] for iv, r in zip(g.index, g.itertuples())],
        "vintage": [[int(y), round(float(r["mean"]), 3), int(r["size"])] for y, r in gv.iterrows()],
        "tasters": [[name, round(float(r["mean"]), 3), int(r["size"])] for name, r in gt.iterrows()],
    }
    with open(os.path.join(HERE, "tables", "chart_data.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("wrote tables/chart_data.json")


if __name__ == "__main__":
    main()
