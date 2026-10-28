# Wine score inflation: the 100-point scale that uses eight points

The lowest score in 129,971 Wine Enthusiast reviews is 80. Nothing below it is ever published, and 85.7% of wines land between 84 and 92, so the scale that reads like a grade out of 100 works in practice as a band about eight points wide.

I hold the WSET Level 3 award in wines, and the course teaches you to judge quality on a short ladder (faulty, poor, acceptable, good, very good, outstanding). A 92 on a shelf talker implies something finer than that, with the lower half of the scale available for wines that earn it. This study checks whether the lower half is used at all.

## The data

The reviews are the public `winemag-data-130k-v2` Wine Enthusiast dataset, which `fetch_data.py` downloads from a GitHub mirror of the Kaggle set. Each review has points (80 to 100), a price, a title that usually contains the vintage year, and the taster's name.

## What the scores do

The mean is 88.45 and the median 88. With an 80 floor and most of the mass between 84 and 92, almost everything that happens in a wine score happens inside those eight points.

Price explains a good share of where a wine falls in the band. For wines priced $4 to $500, points correlate with log price at r = 0.61; wines at about $10 average 85.3 points and wines at about $100 average 91.9, a gain of 6.6 points for a tenfold price increase. Over 20 equal-count price bins the curve flattens after $100.

Vintage barely moves anything. Mean score by vintage from 1995 to 2016 rises 0.09 points per decade (r = 0.10 across the yearly means), so the compression is built into the scale; newer vintages are not scoring their way into it.

The taster moves the score more than the vintage does. Among the ten tasters with the most reviews, mean scores run from 86.9 to 90.0, a spread of 3.1 points. That is about half the effect of the $10 to $100 step and more than a third of the 84 to 92 band.

## Limitations

This is a snapshot from a single publication, and the reviews carry no dates, so it cannot measure scores drifting upward over time. "Inflation" here means the structural compression of the scale plus the price, vintage and taster effects inside it. The taster means are unadjusted for the regions and price points each taster covers.

The code is in `analyze.py`, the headline numbers in `tables/summary.csv`, and the charts in `figures/`.
