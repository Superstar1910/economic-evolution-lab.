# Uganda Lakehouse integration — research assessment

Status: **proposed research integration; no data imported and no predictive evidence claimed**.

## Source repository and isolation

The source is the **private** repository `Superstar1910/oakstone-allocation-os`, with its v0.2 Uganda research lakehouse, private Library source artifacts and selected sanitized research marts. Economic Evolution Lab is public. **Do not copy private source files, credentials, transaction records or Library paths into this repository.** Any data publication needs independent license, privacy, attribution and disclosure review. Prefer an operator-approved, sanitized data contract or authenticated read-only interface.

Source inventory and limitations were inspected in the source repository on 7 November 2026:
- `lakehouse/uganda/v02/README.md`, `manifest.json`, `ingestion_coverage.csv`, `quality_issues.csv`.
- `lakehouse/uganda/LAKEHOUSE_DATA_CONTRACT.md`.
- `docs/UGANDA_UBOS_TRADE_1996_2026.md`.

## Analytically useful inputs

| Source feed | Intended use | Main caveat |
| --- | --- | --- |
| UBOS export composition (1996–2026) | Cross-check sector entry and export diversification | Commodity categories not automatically HS92-4 |
| UBOS import composition (1996–2026) | Complementarity and imported-input proxies | SITC2, not a direct product-level match |
| UBOS exports by destination (1996–2026) | Market diversification and access proxies | Avoid counting regional aggregates and member countries twice |
| BoU exchange and interest rates (1983–2026) | Credit/FX constraints | Distinguish FX quotation and rate definitions |
| BoU selected macro (2005–2026) | Financial conditions | Missingness and limited historic data vintages |
| World Bank commodity monthly (1960–2026) | Commodity price-shock controls | Monthly retrospective snapshot, not old releases |
| Sovereign auction/secondary market (2001–2024) | Exploratory funding-condition regime tests | Quality issues, conventions and incomplete reconstruction |
| Derived EPPI (1998–2026) | Exploratory cycle robustness | Derived, not independent ground truth |

Source repo reports v0.2 **24 source feeds, 392,518 numeric observations, 88,579 transaction records** (including repeated/derived records); an aligned monthly research panel of 802 calendar months (1960-01–2026-10) contains missing observations, not a complete observation panel.

## Required integration contract

Normalize approved inputs to `country_iso3, period, frequency, indicator, value, unit, source, classification, observed_at, released_at, ingested_at, vintage_status, quality_status, source_sha256`.

- Uganda's ISO3 key is `UGA`; join to annual Atlas features only after establishing availability at forecast origin `t`.
- `period` is not evidence of `released_at`. Do not fill unknown release timestamps with month-end or extraction date.
- Classify each indicator as `PIT_VERIFIED`, `RETROSPECTIVE_ONLY` or `UNVERIFIED`. The current source manifest marks ingested sources retrospective, not PIT.
- Apply audited publication lags; prohibit future observations, post-origin revisions and outcome-window leakage.
- Preserve explicitly distinct trade concepts: UBOS merchandise vs BoU balance-of-payments goods and Atlas trade export values.
- Use authoritative HS↔SITC crosswalks only with documented many-to-many aggregation rules; otherwise retain series as coarse macro/sector covariates.
- Keep source-country panels separate from the global all-country reference needed for estimating product-space networks.

## Experimental sequence

1. Atlas-only globally estimated baseline, historical rolling evaluation.
2. Uganda-specific **descriptive** bridge and dataset comparability study (periods, classifications, values, sources).
3. Introduce lagged Uganda aggregate macro/financial indicators in a **Uganda-only exploratory ablation**, with feature availability clearly graded.
4. Validate archive-based point-in-time sources before presenting additional gains as genuine historical forecasting results.
5. Expand to other countries only through comparable data coverage and harmonized definitions; a Uganda-only variable cannot be used naively in the global benchmark.

## Specific research questions
- Does access to finance condition the association between ex-ante product-space density and subsequent RCA entry?
- Do imported intermediate-goods categories precede new export specialization (subject to defensible crosswalks)?
- How much apparent diversification is explained by commodity prices or exchange-rate movements?
- Do observed financial regimes moderate persistence of newly entered activities?

These are candidate tests, not confirmed causal relationships. A positive prediction lift does not establish an autopoietic economic mechanism.
