"""
Authoritative Vimshottari 5-Level Timeline Generator & Query Module.
Generates strict half-open interval timelines [start, end) and resolves arbitrary query datetimes.
"""
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Tuple, Optional

from apps.api.engines.dasha.exceptions import OutOfQueryRangeError, DashaCalculationError
from apps.api.engines.dasha.models import (
    BirthNakshatraInfo,
    DashaPeriodNode,
    ActiveDashaHierarchy
)
from apps.api.engines.dasha.calculator import (
    DASHA_YEARS,
    DASHA_SEQUENCE,
    DAYS_PER_YEAR,
    calculate_child_duration_days
)

def _get_ordered_lords_from(start_lord: str) -> List[str]:
    """Returns the 9 Vimshottari lords starting from start_lord."""
    idx = DASHA_SEQUENCE.index(start_lord)
    return [DASHA_SEQUENCE[(idx + i) % 9] for i in range(9)]

def _create_node(
    level: int,
    level_name: str,
    lord: str,
    seq_idx: int,
    start_dt: datetime,
    duration_days: float
) -> DashaPeriodNode:
    """Creates a DashaPeriodNode with exact UTC datetimes and durations."""
    end_dt = start_dt + timedelta(days=duration_days)
    return DashaPeriodNode(
        level=level,
        level_name=level_name,
        lord=lord,
        sequence_index=seq_idx,
        start_utc_iso=start_dt.isoformat(),
        end_utc_iso=end_dt.isoformat(),
        duration_days=round(duration_days, 6),
        duration_years=round(duration_days / DAYS_PER_YEAR, 6)
    )

def generate_mahadasha_nodes(
    birth_dt_utc: datetime,
    nakshatra_info: BirthNakshatraInfo
) -> List[DashaPeriodNode]:
    """
    Generates the 120-year top-level Mahadasha sequence.
    Handles exact remaining birth balance for the first Mahadasha.
    """
    birth_lord = nakshatra_info.nakshatra_lord
    rem_frac = nakshatra_info.remaining_fraction
    elap_frac = nakshatra_info.elapsed_fraction

    ordered_lords = _get_ordered_lords_from(birth_lord)
    md_nodes: List[DashaPeriodNode] = []

    # 1. Birth Mahadasha
    total_first_md_days = DASHA_YEARS[birth_lord] * DAYS_PER_YEAR
    elapsed_first_md_days = total_first_md_days * elap_frac
    remaining_first_md_days = total_first_md_days * rem_frac

    first_md_start = birth_dt_utc - timedelta(days=elapsed_first_md_days)
    first_node = _create_node(1, "Mahadasha", birth_lord, 1, first_md_start, total_first_md_days)
    md_nodes.append(first_node)

    # 2. Subsequent 8 Mahadashas
    curr_start = datetime.fromisoformat(first_node.end_utc_iso)
    for i in range(1, 9):
        lord = ordered_lords[i]
        md_days = DASHA_YEARS[lord] * DAYS_PER_YEAR
        node = _create_node(1, "Mahadasha", lord, i + 1, curr_start, md_days)
        md_nodes.append(node)
        curr_start = datetime.fromisoformat(node.end_utc_iso)

    return md_nodes

def generate_child_nodes(
    parent_node: DashaPeriodNode,
    child_level: int,
    child_level_name: str
) -> List[DashaPeriodNode]:
    """Generates all 9 nested child sub-period nodes for a parent period node."""
    parent_start = datetime.fromisoformat(parent_node.start_utc_iso)
    parent_days = parent_node.duration_days
    child_lords = _get_ordered_lords_from(parent_node.lord)

    child_nodes: List[DashaPeriodNode] = []
    curr_start = parent_start

    for i, child_lord in enumerate(child_lords):
        c_days = calculate_child_duration_days(parent_days, child_lord)
        node = _create_node(child_level, child_level_name, child_lord, i + 1, curr_start, c_days)
        child_nodes.append(node)
        curr_start = datetime.fromisoformat(node.end_utc_iso)

    return child_nodes

def query_dasha_hierarchy_at(
    query_dt_utc: datetime,
    md_nodes: List[DashaPeriodNode]
) -> ActiveDashaHierarchy:
    """
    Resolves the exact 5-level active Dasha hierarchy for an arbitrary query datetime.
    Strict half-open interval rule [start, end).
    """
    # 1. Active Mahadasha
    active_md: Optional[DashaPeriodNode] = None
    for md in md_nodes:
        s = datetime.fromisoformat(md.start_utc_iso)
        e = datetime.fromisoformat(md.end_utc_iso)
        if s <= query_dt_utc < e:
            active_md = md
            break

    if not active_md:
        raise OutOfQueryRangeError(
            f"Query datetime {query_dt_utc.isoformat()} is outside the valid 120-year Vimshottari timeline."
        )

    # 2. Active Antardasha
    ad_nodes = generate_child_nodes(active_md, 2, "Antardasha")
    active_ad = next(
        node for node in ad_nodes
        if datetime.fromisoformat(node.start_utc_iso) <= query_dt_utc < datetime.fromisoformat(node.end_utc_iso)
    )

    # 3. Active Pratyantardasha
    pd_nodes = generate_child_nodes(active_ad, 3, "Pratyantardasha")
    active_pd = next(
        node for node in pd_nodes
        if datetime.fromisoformat(node.start_utc_iso) <= query_dt_utc < datetime.fromisoformat(node.end_utc_iso)
    )

    # 4. Active Sookshma
    sookshma_nodes = generate_child_nodes(active_pd, 4, "Sookshma")
    active_sookshma = next(
        node for node in sookshma_nodes
        if datetime.fromisoformat(node.start_utc_iso) <= query_dt_utc < datetime.fromisoformat(node.end_utc_iso)
    )

    # 5. Active Prana
    prana_nodes = generate_child_nodes(active_sookshma, 5, "Prana")
    active_prana = next(
        node for node in prana_nodes
        if datetime.fromisoformat(node.start_utc_iso) <= query_dt_utc < datetime.fromisoformat(node.end_utc_iso)
    )

    # Calculate active Prana progress
    prana_start = datetime.fromisoformat(active_prana.start_utc_iso)
    prana_end = datetime.fromisoformat(active_prana.end_utc_iso)
    prana_total_days = active_prana.duration_days

    elapsed_sec = (query_dt_utc - prana_start).total_seconds()
    elapsed_days = elapsed_sec / 86400.0
    remaining_days = prana_total_days - elapsed_days

    pct_elapsed = (elapsed_days / prana_total_days) * 100.0 if prana_total_days > 0 else 0.0
    pct_remaining = 100.0 - pct_elapsed

    return ActiveDashaHierarchy(
        query_utc_iso=query_dt_utc.isoformat(),
        active_mahadasha=active_md,
        active_antardasha=active_ad,
        active_pratyantardasha=active_pd,
        active_sookshma=active_sookshma,
        active_prana=active_prana,
        elapsed_days_in_prana=round(elapsed_days, 6),
        remaining_days_in_prana=round(remaining_days, 6),
        percentage_elapsed_in_prana=round(pct_elapsed, 4),
        percentage_remaining_in_prana=round(pct_remaining, 4)
    )
