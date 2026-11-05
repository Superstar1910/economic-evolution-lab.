# Economic Evolution Lab

**Status: research infrastructure under development; no empirical validation claimed.**

A reproducible research programme examining whether Arthur-inspired combinatorial economic evolution improves forecasts of new industrial activity beyond economic complexity, product-space relatedness and macroeconomic baselines.

## Research question
Do capability recombination, complementary opportunity creation, displacement and economic readjustment provide *incremental out-of-sample predictive power* for sustained country-product export entry?

## Empirical design
- Historical country × HS92 four-digit product × year panel, target 1995–2024 (subject to source coverage).
- Primary outcome: new sustained RCA ≥ 1 entry within a five-year forward horizon, conditional on initial RCA < 1.
- Baselines: persistence, product-space density, economic complexity and macroeconomic controls.
- Candidate additional features: opportunity complementarity, capability recombination, competing/displaced activities and network spillovers.
- Rolling-origin evaluation; train-only product proximity estimation; strict anti-leakage checks; country and time disaggregation.
- Evaluate calibration, precision/recall, PR-AUC and improvement over baselines; cluster uncertainty at country level.
- Export products are imperfect proxies for technologies and productive capabilities. Predictive improvement alone does not establish causality.

## Structure
- `src/evolution_lab/`: data ingestion, validation and baseline logic
- `tests/`: deterministic unit tests
- `docs/`: thesis, data contract, research protocol
- `.github/workflows/`: continuous integration
- `data/`: documentation only; raw and large files remain outside Git

## Run
```bash
python -m pip install -e ".[dev]"
pytest -q
python -m evolution_lab.cli --help
```

## Source and reproducibility
Harvard Growth Lab Atlas of Economic Complexity: https://atlas.hks.harvard.edu/ ; World Bank WDI: https://data.worldbank.org/ . API schema, license, country/product harmonization and historical coverage must be verified before any full-scale extract. Do not commit raw large datasets or credentials.

## Roadmap
1. Validate official API query and small historical extract.
2. Create provenance-checked panel, RCA outcome labels and rolling splits.
3. Implement persistence/product-space baselines.
4. Add preregistered Arthur-inspired features and run ablation studies.
5. Publish reproducible findings, including null results.
