import pytest
from evolution_lab.baselines import rca_presence, proximity_from_presence, density, purge_train_origins

def test_rca_missing_not_zero():
    assert rca_presence(None) is None
    assert rca_presence(0.8) == 0
    assert rca_presence(1.0) == 1

def test_proximity_conditional_minimum():
    panel = {
        "A": {"p": 1, "q": 1},
        "B": {"p": 1, "q": 0},
        "C": {"p": 0, "q": 1},
    }
    prox = proximity_from_presence(panel)
    assert prox["p", "q"] == pytest.approx(0.5)
    assert density("p", {"p": 0, "q": 1}, prox) == pytest.approx(1)

def test_proximity_ignores_missing_pair():
    panel = {"A": {"p": 1, "q": 1}, "B": {"p": 1, "q": None}}
    assert proximity_from_presence(panel)["p", "q"] == pytest.approx(1)

def test_density_requires_known_neighbor():
    assert density("p", {"q": None}, {("p", "q"): 0.8}) is None

def test_purged_train_labels():
    assert purge_train_origins(list(range(2000, 2011)), 2010, 5) == list(range(2000, 2005))
