# Wine Score Inflation: the 100-point scale that isn't

**Question.** What does a wine "score" actually tell you?

**Data.** The public winemag-data-130k-v2 Wine Enthusiast dataset (129,971 reviews):
points (80-100), price, title (vintage), taster_name. Vintage parsed from title.

**Results.**
- Distribution: min 80 (hard floor - nothing lower is published), mean 88.4,
  median 88; 85.7% of wines score 84-92. The usable scale is ~8 points wide.
- Price: points vs log-price r = 0.61; ~$10 wine averages 85.3 pts, ~$100 wine 91.9
  pts - steep diminishing returns.
- Vintage: average points essentially flat across vintages (~0.09 pts/decade,
  r = 0.10) - the compression is structural, not a recency trend.
- Reviewer: among the 10 most prolific tasters, mean scores span 3.1 points
  (86.9 to 90.0) - comparable to a 10x price increase.

**Caveat.** A single-publication snapshot cannot measure score drift by review date.
"Inflation" here means the structural compression of the scale plus price, vintage,
and reviewer effects.

See `analyze.py` and `figures/`.
