# Empirical research protocol (draft; preregistration pending)

## Hypothesis
H0: Arthur-inspired features provide no improvement over a well-specified product-space and economic complexity baseline in forecasting sustained RCA entry.

H1: Arthur-inspired features improve genuinely held-out predictive performance.

## Guardrails
1. Define origin year t and five-year outcome horizon t+1…t+5.
2. Estimate all feature transformations and product networks only using observations available by t.
3. Compare models using identical country-product-year evaluation sets.
4. Prevent training labels whose outcome window overlaps the test period.
5. Report uncertainty, class imbalance, missingness and changes in HS coverage.
6. Report ablations by mechanism; avoid relabeling standard relatedness as novel theory.
7. Conduct leave-country-out and Africa-only robustness tests.
8. Interpret export diversification as an observable proxy, not direct proof of technology evolution.

## Data caveats
Trade data do not directly measure non-tradables, production networks, firms or capital formation. RCA may change because of trade prices, exchange rates or reporting practices. A later causal study would require separate identification.

## Metrics
Primary: PR-AUC and log loss versus baseline, with country-clustered confidence intervals. Secondary: Brier score, ROC-AUC, recall at fixed precision and top-k entry hit rate. No quantitative result is reported until actual data have been processed.
