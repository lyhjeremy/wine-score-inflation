# Wine Score Inflation: the 100-point scale that uses eight points

## Question

What does a wine score tell you? A 92 reads like a grade out of 100, which assumes the lower half of the scale is in use. This study checks that assumption against a large set of professional reviews.

## Data

The public `winemag-data-130k-v2` Wine Enthusiast dataset: 129,971 reviews, each with points (80 to 100), price, a title that usually contains the vintage year, and the taster's name. `fetch_data.py` downloads it from a GitHub mirror of the Kaggle set.

## Results

**Distribution.** The minimum is 80; no lower score is published. The mean is 88.45 and the median 88. 85.7% of wines score from 84 to 92, so the usable scale is about eight points wide.

**Price.** For wines priced $4 to $500, points correlate with log price at r = 0.61. Wines at about $10 average 85.3 points and wines at about $100 average 91.9, a gain of 6.6 points for a tenfold price increase. The curve over 20 price bins flattens after $100.

**Vintage.** Mean score by vintage, 1995 to 2016, rises 0.09 points per decade (r = 0.10 across the yearly means). The compression is structural and does not come from newer vintages scoring higher.

**Tasters.** Among the ten tasters with the most reviews, mean scores range from 86.9 to 90.0, a spread of 3.1 points. That is about half the effect of the $10 to $100 step and more than a third of the 84 to 92 band.

## Limitations

A single-publication snapshot without review dates cannot measure score drift over time. Inflation here means the structural compression of the scale plus the price, vintage and taster effects inside it. Taster means are unadjusted for region or price.

See `analyze.py`, `tables/summary.csv` and `figures/`.
