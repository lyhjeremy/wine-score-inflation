# Wine score inflation: the 100-point scale that uses eight points

The lowest score in 119,988 unique Wine Enthusiast reviews is 80. Nothing below it is ever published, and 85.0% of wines land between 84 and 92, so the scale that reads like a grade out of 100 works in practice as a band about eight points wide.

I hold the WSET Level 3 award in wines, and the course teaches you to judge quality on a short ladder (faulty, poor, acceptable, good, very good, outstanding). A 92 on a shelf talker implies something finer than that, with the lower half of the scale available for wines that earn it. This study checks whether the lower half is used at all.

## The data

The reviews are the public `winemag-data-130k-v2` Wine Enthusiast dataset, which `fetch_data.py` downloads from a GitHub mirror of the Kaggle set. Each review has points (80 to 100), a price, a title that usually contains the vintage year, and the taster's name. The file has 129,971 rows, but 9,983 of them repeat an earlier review exactly, so the analysis drops them and works from 119,988 reviews.

## What the scores do

The mean is 88.44 and the median 88. With an 80 floor and most of the mass between 84 and 92, almost everything that happens in a wine score happens inside those eight points.

Price explains a good share of where a wine falls in the band. For wines priced $4 to $500, points correlate with log price at r = 0.62; wines at about $10 average 85.2 points and wines at about $100 average 91.9, a gain of 6.7 points for a tenfold price increase. Over 20 equal-count price bins the curve is close to a straight line on a log price axis: $10 to $20 adds 2.6 points and $50 to about $115 adds 2.0, so each doubling buys about two points. The top bin runs from $85 to $500, so the bins can't show what happens above $100. (An earlier version of this note said the curve flattens after $100; the bin data in `tables/chart_data.json` doesn't support that.)

Vintage barely moves anything. Mean score by vintage from 1995 to 2016 rises 0.08 points per decade (r = 0.10 across the yearly means), so the compression is built into the scale; newer vintages are not scoring their way into it.

The taster moves the score more than the vintage does. Among the ten tasters with the most reviews, mean scores run from 86.9 to 90.1, a spread of 3.2 points. That is about half the effect of the $10 to $100 step and more than a third of the 84 to 92 band.

## Correction, 2026-10-29

The source CSV repeats 9,983 reviews word for word, and earlier versions of this analysis counted each of them twice. `analyze.py` now drops exact duplicates, which leaves 119,988 reviews. These numbers moved: the share scoring 84 to 92 went from 85.7% to 85.0%, points against log price from r = 0.61 to 0.62, the average at about $10 from 85.3 to 85.2, the mean score from 88.45 to 88.44, the vintage trend from 0.09 to 0.08 points per decade, and the top taster mean from 90.0 to 90.1 (so the taster spread went from 3.1 to 3.2 points). The 80 floor, the median of 88 and the $100 average of 91.9 did not change.

## Limitations

This is a snapshot from a single publication, and the reviews carry no dates, so it cannot measure scores drifting upward over time. "Inflation" here means the structural compression of the scale plus the price, vintage and taster effects inside it. The taster means are unadjusted for the regions and price points each taster covers.

The code is in `analyze.py`, the headline numbers in `tables/summary.csv`, and the charts in `figures/`.
