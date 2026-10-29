# Wine score inflation

A study of 119,988 unique Wine Enthusiast reviews (the source file has 129,971 rows and repeats 9,983 of them). The 100-point wine scale turns out to be about eight points wide in practice.

[Live site](https://lyhjeremy.github.io/wine-score-inflation/) · [Write-up](https://lyhjeremy.github.io/wine-score-inflation/overview/)

Design and copy follow [these standards](https://github.com/lyhjeremy/lyhjeremy/blob/main/DESIGN_STANDARDS.md).

## Results

| Measure | Value |
|---|---|
| Lowest published score | 80 |
| Share of wines scoring 84 to 92 | 85.0% |
| Points against log price | r = 0.62 |
| Average at about $10 / about $100 | 85.2 / 91.9 points |
| Vintage trend, 1995 to 2016 | 0.08 points per decade |
| Spread between the ten most prolific tasters | 3.2 points (86.9 to 90.1) |

![Histogram of wine scores with a hard floor at 80 and most wines between 84 and 92](figures/01_distribution.png)

## Correction, 2026-10-29

The source CSV repeats 9,983 reviews word for word, and earlier versions of this analysis counted each of them twice. `analyze.py` now drops exact duplicates, which leaves 119,988 reviews. These numbers moved: the share scoring 84 to 92 went from 85.7% to 85.0%, points against log price from r = 0.61 to 0.62, the average at about $10 from 85.3 to 85.2, the mean score from 88.45 to 88.44, the vintage trend from 0.09 to 0.08 points per decade, and the top taster mean from 90.0 to 90.1 (so the taster spread went from 3.1 to 3.2 points). The 80 floor, the median of 88 and the $100 average of 91.9 did not change.

## Method

`analyze.py` loads the reviews with pandas, drops the 9,983 rows that repeat an earlier review exactly, coerces points and price to numbers, and pulls the vintage year out of each title with a regular expression. It then computes four things:

1. The score distribution: minimum, mean, median and the share of wines from 84 to 92.
2. Price against points: the Pearson correlation of points with log10 price for wines from $4 to $500, the mean score at $9 to $11 and at $90 to $110, and a curve over 20 equal-count price bins.
3. Vintage: mean score per vintage from 1995 to 2016 and a linear fit (`scipy.stats.linregress`) through those means.
4. Tasters: the mean score of each of the ten tasters with the most reviews.

Every number above is written to `tables/summary.csv` and drawn in `figures/`. `chart_data.py` writes the small aggregates behind the write-up's interactive charts (score counts, the 20 price bins, vintage and taster means) to `tables/chart_data.json`, using the same filters.

Stack: Python, pandas, NumPy, SciPy, matplotlib.

## How to run

```bash
pip install -r requirements.txt
python fetch_data.py     # downloads the review CSV to data/ (git-ignored)
python analyze.py        # writes figures/ and tables/summary.csv
python chart_data.py     # writes tables/chart_data.json for the write-up charts
```

## Repo layout

| Path | Contents |
|---|---|
| `fetch_data.py` | Downloads `winemag-data-130k-v2.csv` |
| `analyze.py` | All statistics and figures |
| `figures/` | The four charts used on the site |
| `tables/summary.csv` | The headline numbers |
| `index.html`, `overview/` | The published story and write-up |

## Limitations

The data is the public `winemag-data-130k-v2` set (Kaggle, through a GitHub mirror), which is one snapshot from one publication with no review dates, so it cannot show scores creeping upward over time. The inflation it measures is structural (an 80 floor and a narrow band) plus the price, vintage and taster effects inside that band. Wines whose titles carry no year drop out of the vintage chart only. Taster means are raw, so they mix taster generosity with the regions and price points each taster covers.

## License

[MIT](LICENSE) © 2026 Jeremy Lee
