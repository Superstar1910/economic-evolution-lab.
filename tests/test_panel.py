from evolution_lab.panel import rolling_origins, sustained_entry

def test_sustained_entry():
    x = {2000: 0.4, 2001: 0.8, 2002: 1.1, 2003: 1.2, 2004: 0.5, 2005: 0.4}
    assert sustained_entry(x, 2000) is True

def test_no_entry():
    x = {2000: 0.4, **{y: 0.5 for y in range(2001, 2006)}}
    assert sustained_entry(x, 2000) is False

def test_missing_is_unknown():
    assert sustained_entry({2000: 0.2, 2001: 1.2}, 2000) is None

def test_no_lookahead_origins():
    assert rolling_origins(1995, 2024, 5)[-1] == 2019
