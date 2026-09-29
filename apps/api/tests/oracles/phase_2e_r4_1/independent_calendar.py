"""
Independent Calendar & Time Period Lords for R4 Oracle.
"""
VARA_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
HORA_SEQUENCE = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

def get_independent_vara_lord(julian_day: float) -> str:
    weekday = int(julian_day + 1.5) % 7
    return VARA_LORDS[weekday]

def get_independent_hora_lord(julian_day: float, hour: int) -> str:
    vara_lord = get_independent_vara_lord(julian_day)
    hora_idx = (hour - 6) % 24
    start_hora_idx = HORA_SEQUENCE.index(vara_lord) if vara_lord in HORA_SEQUENCE else 0
    return HORA_SEQUENCE[(start_hora_idx + hora_idx) % 7]

def get_independent_masa_lord(julian_day: float, month: int) -> str:
    weekday = int(julian_day + 1.5) % 7
    return VARA_LORDS[(weekday + (month * 2)) % 7]

def get_independent_varsha_lord(julian_day: float, year: int) -> str:
    weekday = int(julian_day + 1.5) % 7
    return VARA_LORDS[(weekday + (year * 3)) % 7]
