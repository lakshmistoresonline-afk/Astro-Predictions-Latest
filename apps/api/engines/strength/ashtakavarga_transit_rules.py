"""
Versioned Ashtakavarga Transit Favorability Ruleset for Astrovision.
Section 8, 9, 10 & 11 Compliance:
- Centralized favorability classification logic with documented BPHS transit bindu threshold rules.
- Explicit version constant: TRANSIT_ASHTAKAVARGA_RULESET_VERSION.
- Fail closed with UNAVAILABLE status when raw SAV or BAV bindus are None.
"""
from typing import Optional

TRANSIT_ASHTAKAVARGA_RULESET_VERSION = "2026.1_PARASHARI_ASHTAKAVARGA_TRANSIT_V1"

# BPHS Standard Transit Bindu Threshold Constants
HIGHLY_AUSPICIOUS_SAV_MIN = 30
HIGHLY_AUSPICIOUS_BAV_MIN = 5
AUSPICIOUS_SAV_MIN = 28
AUSPICIOUS_BAV_MIN = 4
CRITICAL_SAV_MAX = 25
CRITICAL_BAV_MAX = 3
CHALLENGING_SAV_MAX = 28
CHALLENGING_BAV_MAX = 4

def classify_transit_favorability(sav_bindus: Optional[int], bav_bindus: Optional[int]) -> str:
    """
    Classifies Ashtakavarga transit favorability based on live SAV and BAV bindus.
    Returns UNAVAILABLE if either SAV or BAV bindu count is None.
    """
    if sav_bindus is None or bav_bindus is None:
        return "UNAVAILABLE"

    if sav_bindus >= HIGHLY_AUSPICIOUS_SAV_MIN and bav_bindus >= HIGHLY_AUSPICIOUS_BAV_MIN:
        return "HIGHLY_AUSPICIOUS"
    elif sav_bindus >= AUSPICIOUS_SAV_MIN or bav_bindus >= AUSPICIOUS_BAV_MIN:
        return "AUSPICIOUS"
    elif sav_bindus < CRITICAL_SAV_MAX and bav_bindus < CRITICAL_BAV_MAX:
        return "CRITICAL"
    elif sav_bindus < CHALLENGING_SAV_MAX or bav_bindus < CHALLENGING_BAV_MAX:
        return "CHALLENGING"
    else:
        return "NEUTRAL"
