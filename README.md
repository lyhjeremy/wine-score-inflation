# Wine Score Inflation — the 100-point scale that isn't

Across ~130,000 Wine Enthusiast reviews, the famous 100-point scale is really an
**8-point** one: nothing is published below **80**, and **86%** of all wines score
between **84 and 92**. Price buys points with steep diminishing returns, the trend
across vintages is flat, and the reviewer matters as much as a 10× price jump.

> 🌐 **Read the story:** https://lyhjeremy.github.io/wine-score-inflation/

## Findings
- Scores floored at **80**; **86%** land in **84–92** (scale is ~8 points wide).
- Points vs **log-price r = 0.61**, steep diminishing returns (~$10 → ≈85 pts, ~$100 → ≈92 pts).
- Average score is **flat across vintages** (~0.09 pts/decade) — the inflation is structural.
- **3.1-point** spread between the most and least generous reviewers.

## Reproduce
```bash
pip install -r requirements.txt
python fetch_data.py     # downloads the ~130k-review dataset to data/
python analyze.py        # writes figures/ and tables/summary.csv
```

## Data & caveat
The public "winemag-data-130k-v2" Wine Enthusiast dataset (~130k reviews, Kaggle,
via a GitHub mirror). Vintage is parsed from each wine's title. Because this is a
single snapshot from one publication, it can't measure score drift by **review
date**; the "inflation" here is the structural compression of the scale (an 80
floor and a narrow band) plus price/vintage/reviewer effects, not a year-over-year
creep. Raw data is downloaded by `fetch_data.py` and git-ignored.

## License
[MIT](LICENSE) © 2026 Jeremy Lee
