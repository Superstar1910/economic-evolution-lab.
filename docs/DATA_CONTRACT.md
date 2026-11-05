# Data contract

Expected canonical schema: `country_iso3, product_hs92_4, year, export_usd, rca`.

- `country_iso3`: ISO-3 country code, documented historical mappings.
- `product_hs92_4`: string, four digits, leading zeros preserved.
- `year`: integer.
- `export_usd`: nonnegative value in nominal USD, source definition recorded.
- `rca`: nonnegative numeric or missing; must record source methodology.

Each extract needs a manifest with original endpoint, UTC extraction time, exact request parameters, response hash, license, coverage, missingness and transformation version.

Data access should use the official Harvard Atlas published API, with a schema-confirmation query before requesting historical records. Large raw datasets are not stored in Git.
