# Baseline specification — implementation stage

## First benchmark ladder
1. Historical RCA persistence and lagged export status.
2. Country/product/time controls with explicit missingness indicators.
3. Ex-ante product-space proximity and relatedness density.
4. Country economic complexity, macroeconomic and product controls.
5. Arthur-inspired recombination, complementarity and displacement features, **only after** baselines have been validated.

## Product-space proximity
For product pair i,j, proximity is the minimum of the conditional probabilities P(M_i=1 | M_j=1) and P(M_j=1 | M_i=1), with M=1 when RCA≥1. The `baselines.py` implementation is a small deterministic reference for complete training snapshots; production calculations must use a broad cross-country reference panel and robust handling of missing observations.

## Historical evaluation
Forecast at t using information available at or before t; outcome uses t+1 through t+5. Purge training origins whose label windows overlap the test period. For a complete dataset ending in 2024, the latest fully observed five-year origin is 2019.

## Limits of current implementation
No global product network, no WDI covariates, no fitted baseline model, no measured out-of-sample scores and no empirical support for the Arthur-inspired hypothesis have yet been produced.
