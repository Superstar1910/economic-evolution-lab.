"""Transparent, leakage-aware baseline feature engineering.

These are deterministic building blocks, not fitted empirical results.
"""
from __future__ import annotations
import math
from collections.abc import Mapping


def rca_presence(rca: float | None, threshold: float = 1.0) -> int | None:
    """Binary RCA specialization; missing is unknown, not zero."""
    if rca is None:
        return None
    if not math.isfinite(float(rca)) or rca < 0:
        raise ValueError("RCA must be finite and nonnegative")
    return int(rca >= threshold)


def proximity_from_presence(presence: Mapping[str, Mapping[str, int | None]]) -> dict[tuple[str, str], float]:
    """Pairwise Hidalgo-Hausmann conditional co-occurrence proximity.

    Country rows are historical *training-period* observations only. Missing
    entries are excluded pairwise. A production model must estimate proximity
    strictly before each forecast origin and never reuse a future network.
    """
    products = sorted({p for row in presence.values() for p in row})
    result = {}
    for i, a in enumerate(products):
        for b in products[i + 1:]:
            valid = [(row[a], row[b]) for row in presence.values()
                     if a in row and b in row and row[a] is not None and row[b] is not None]
            n_a = sum(x for x, _ in valid)
            n_b = sum(y for _, y in valid)
            n_both = sum(x * y for x, y in valid)
            phi = min(n_both / n_a, n_both / n_b) if n_a and n_b else 0.0
            result[a, b] = result[b, a] = phi
    return result


def density(target: str, country_presence: Mapping[str, int | None],
            proximity: Mapping[tuple[str, str], float]) -> float | None:
    """Relatedness density for target given an ex-ante proximity network.

    Returns None when proximity coverage or country presence is insufficient.
    """
    neighbors = [(other, weight) for (product, other), weight in proximity.items()
                 if product == target and other != target and weight > 0]
    if not neighbors:
        return None
    if any(country_presence.get(other) is None for other, _ in neighbors):
        return None
    denom = sum(weight for _, weight in neighbors)
    return sum(weight * country_presence[other] for other, weight in neighbors) / denom


def purge_train_origins(train_origins: list[int], test_start: int, horizon: int = 5) -> list[int]:
    """Drop training origins whose forward labels reach the test period."""
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return [t for t in train_origins if t + horizon < test_start]
