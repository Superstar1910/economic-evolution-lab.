import pytest
from evolution_lab.atlas import AtlasError, graphql, normalize, TRADE_QUERY

def test_normalize_preserves_hs_leading_zeros():
    rows = [{"productId": 9, "year": 2001, "exportValue": 150, "exportRca": 1.3}]
    assert normalize(rows, "UGA", {9: "0101"}, 2001, 2001)[0]["product_hs92_4"] == "0101"

def test_duplicate_fails():
    rows = [{"productId": 9, "year": 2001, "exportValue": 1, "exportRca": 1}] * 2
    with pytest.raises(AtlasError, match="Duplicate"):
        normalize(rows, "UGA", {9: "0101"}, 2001, 2001)

def test_future_year_fails():
    with pytest.raises(AtlasError, match="outside"):
        normalize([{"productId": 9, "year": 2025}], "UGA", {9: "0101"}, 2001, 2001)

def test_documented_graphql_fields():
    assert "countryProductYear" in TRADE_QUERY
    assert "exportRca" in TRADE_QUERY
    assert "yearMin" in TRADE_QUERY

def test_graphql_errors_fail_closed():
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return b'{"errors":[{"message":"invalid field"}],"data":null}'
    with pytest.raises(AtlasError):
        graphql("query { broken }", opener=lambda *a, **kw: Response())
