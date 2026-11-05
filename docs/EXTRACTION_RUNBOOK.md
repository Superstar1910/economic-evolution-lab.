# Harvard Atlas extraction runbook

## Official API
Documentation: https://github.com/harvard-growth-lab/api-docs/blob/main/atlas.md
Endpoint: https://atlas.hks.harvard.edu/api/graphql

The documented `countryProductYear` query supports `countryId`, `productClass: HS92`, `productLevel: 4`, `yearMin`, `yearMax` and returns `productId`, `year`, `exportValue`, `exportRca`. Product IDs are **not** HS codes: the script joins them to `productHs92` catalogue codes. Country IDs are discovered through `locationCountry`.

## Smoke test
GitHub Actions > **Atlas API smoke extract** > Run workflow. Defaults: Uganda, 2022. Inspect downloadable artifact and manifest. This is manual-only to avoid unapproved API traffic.

## Local pilot
```bash
pip install -e ".[dev]"
python -m evolution_lab.cli extract-atlas --countries UGA KEN TZA RWA ETH MAR MUS KOR CHN VNM --start 1995 --end 2024 --output data/raw/atlas_hs92_pilot.csv
pytest -q
```

## Quality gates
- Confirm response schema and full-year coverage.
- Inspect missing years, country mappings, duplicate rows and HS92 code formatting.
- Compare sampled values with Atlas source.
- Do **not** infer zero exports from absent product-year records.
- Use supplied RCA for pilot labels; global all-country data are needed for independently estimated proximity networks.
- Do not publish empirical performance claims until out-of-sample runs complete.

## Operational limitations
The public API has a documented rate limit of 120 requests/minute; the script defaults to a slower pace and retries transient failures. The API may change without notice. Large multi-country runs should be run locally or on dedicated compute, not as unbounded scheduled GitHub Actions jobs.
