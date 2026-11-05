"""Harvard Growth Lab Atlas GraphQL extraction (official documented queries).

Small country/year requests, explicit provenance and strict schema validation.
No automatic large global extraction.
"""
from __future__ import annotations
import csv
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

API_URL = "https://atlas.hks.harvard.edu/api/graphql"
COUNTRIES_QUERY = """query { locationCountry { countryId iso3Code nameEn } }"""
PRODUCTS_QUERY = """query { productHs92(productLevel: 4) { productId code nameEn } }"""
TRADE_QUERY = """query ($country: Int!, $start: Int!, $end: Int!) {
  countryProductYear(countryId: $country, productClass: HS92,
    productLevel: 4, yearMin: $start, yearMax: $end) {
    productId year exportValue exportRca
  }
}"""
FIELDS = ("country_iso3", "product_hs92_4", "year", "export_usd", "rca")
DEFAULT_COUNTRIES = ("UGA", "KEN", "TZA", "RWA", "ETH", "MAR", "MUS", "KOR", "CHN", "VNM")


class AtlasError(RuntimeError):
    pass


def graphql(query: str, variables: dict | None = None, *, retries: int = 3, timeout: int = 90, opener=None) -> dict:
    """POST GraphQL; fail closed on GraphQL errors and unexpected envelopes."""
    opener = opener or request.urlopen
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    for attempt in range(retries + 1):
        req = request.Request(API_URL, data=payload, headers={
            "Content-Type": "application/json",
            "User-Agent": "economic-evolution-lab/0.1 (academic research)",
        }, method="POST")
        try:
            with opener(req, timeout=timeout) as resp:
                doc = json.loads(resp.read().decode("utf-8"))
            if not isinstance(doc, dict) or doc.get("errors") or not isinstance(doc.get("data"), dict):
                raise AtlasError("GraphQL returned errors or missing data: " + str(doc.get("errors", doc))[:500])
            return doc["data"]
        except (error.HTTPError, error.URLError, TimeoutError) as exc:
            if attempt >= retries or isinstance(exc, error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                raise AtlasError(f"Atlas request failed: {exc}") from exc
            time.sleep(min(2 ** attempt, 8))
    raise AssertionError("unreachable")


def catalogues() -> tuple[dict[str, int], dict[int, str]]:
    countries = graphql(COUNTRIES_QUERY).get("locationCountry")
    products = graphql(PRODUCTS_QUERY).get("productHs92")
    if not isinstance(countries, list) or not isinstance(products, list):
        raise AtlasError("Atlas country or product catalogue missing")
    iso_to_id = {str(c["iso3Code"]).upper(): int(c["countryId"])
                 for c in countries if c.get("iso3Code") and c.get("countryId") is not None}
    id_to_code = {int(p["productId"]): str(p["code"]).zfill(4)
                  for p in products if p.get("productId") is not None and p.get("code") is not None}
    if not iso_to_id or not id_to_code or any(len(code) != 4 for code in id_to_code.values()):
        raise AtlasError("Unexpected Atlas catalogue schema")
    return iso_to_id, id_to_code


def normalize(rows: list[dict], iso3: str, code_by_id: dict[int, str], start: int, end: int) -> list[dict]:
    if not isinstance(rows, list):
        raise AtlasError("Expected list of countryProductYear observations")
    result = []
    seen = set()
    for record in rows:
        product_id = int(record["productId"])
        if product_id not in code_by_id:
            raise AtlasError(f"Unknown productId {product_id}")
        year = int(record["year"])
        if not start <= year <= end:
            raise AtlasError(f"Year outside requested range: {year}")
        key = (iso3, code_by_id[product_id], year)
        if key in seen:
            raise AtlasError(f"Duplicate observation: {key}")
        seen.add(key)
        export = record.get("exportValue")
        rca = record.get("exportRca")
        if export is not None and float(export) < 0 or rca is not None and float(rca) < 0:
            raise AtlasError("Negative export or RCA")
        result.append(dict(zip(FIELDS, (iso3, code_by_id[product_id], year, export, rca))))
    return result


def extract(output: str | Path, countries: tuple[str, ...] = DEFAULT_COUNTRIES,
            start: int = 1995, end: int = 2024, delay: float = 0.7) -> dict:
    if start > end or start < 1995:
        raise ValueError("Require 1995 <= start <= end")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    iso_to_id, code_by_id = catalogues()
    missing = set(countries) - iso_to_id.keys()
    if missing:
        raise AtlasError(f"Missing country ISO3 codes: {sorted(missing)}")
    observations = []
    for iso in countries:
        # Annual batches limit response size and permit precise failure isolation.
        for year in range(start, end + 1):
            rows = graphql(TRADE_QUERY, {"country": iso_to_id[iso], "start": year, "end": year}).get("countryProductYear")
            observations.extend(normalize(rows, iso, code_by_id, year, year))
            time.sleep(max(0, delay))
    observations.sort(key=lambda r: (r["country_iso3"], r["year"], r["product_hs92_4"]))
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(observations)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    manifest = {
        "source": "Harvard Growth Lab Atlas of Economic Complexity",
        "api_url": API_URL, "classification": "HS92", "product_level": 4,
        "countries": list(countries), "year_min": start, "year_max": end,
        "rows": len(observations), "sha256": digest,
        "extracted_utc": datetime.now(timezone.utc).isoformat(),
        "notes": "Atlas API exportRca used as supplied; not recomputed from pilot sample. "
                 "Missing rows are not assumed to represent zero trade. "
                 "Full global panel required for ex-ante proximity estimation.",
    }
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
