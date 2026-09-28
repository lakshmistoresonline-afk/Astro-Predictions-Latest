"""
Independent Aspect Logic for Oracle.
"""
def independent_house_distance(source_house: int, target_house: int) -> int:
    return (target_house - source_house) % 12

def independent_is_conjunct(source_house: int, target_house: int) -> bool:
    return source_house == target_house

def independent_casts_aspect(planet: str, source_house: int, target_house: int) -> bool:
    if source_house == target_house:
        return False # Conjunction is not aspect

    dist_0 = independent_house_distance(source_house, target_house)
    offset = dist_0 + 1

    if offset == 7:
        return True
    if planet == "Mars" and offset in [4, 7, 8]:
        return True
    if planet == "Jupiter" and offset in [5, 7, 9]:
        return True
    if planet == "Saturn" and offset in [3, 7, 10]:
        return True
    if planet in ["Rahu", "Ketu"] and offset in [5, 7, 9]:
        return True

    return False
