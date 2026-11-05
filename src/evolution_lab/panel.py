"""Explicit, leakage-aware outcome construction for RCA panels."""
from __future__ import annotations

def sustained_entry(rca_by_year: dict[int, float | None], origin: int, horizon: int = 5, sustain: int = 2) -> bool | None:
    """Whether RCA crosses >=1 and remains >=1 for >=sustain consecutive years.

    Entry must occur after origin and by origin+horizon. Missing observations
    are not treated as zero; return None when the required future window is
    incomplete. Origin RCA must be observed and <1.
    """
    if horizon < 1 or sustain < 1 or sustain > horizon:
        raise ValueError("Require horizon >= sustain >= 1")
    base = rca_by_year.get(origin)
    if base is None:
        return None
    if base >= 1:
        return False
    future = [rca_by_year.get(year) for year in range(origin + 1, origin + horizon + 1)]
    if any(value is None for value in future):
        return None
    return any(all(value >= 1 for value in future[i:i+sustain]) for i in range(horizon-sustain+1))

def rolling_origins(first_year: int, last_year: int, horizon: int = 5) -> list[int]:
    """Origins for which the full future label window is observed."""
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return list(range(first_year, last_year - horizon + 1))
