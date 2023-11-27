from .city_state import CityState

def compute_green_score(city_state: CityState):
    sextants = city_state.sextants
    gears = city_state.gears
    scripts = city_state.scripts
    any_symbols = city_state.any_symbols

    compute_score = lambda s1, s2, s3: 7*min(s1, s2, s3) + s1**2 + s2**2 + s3**2

    if any_symbols == 0:
        return compute_score(sextants, gears, scripts)
    else:
        max_score = 0
        for sextant, gear, script in zip(range(any_symbols), range(any_symbols), range(any_symbols)):
            if sextant + gear + script != any_symbols:
                continue
            score = compute_score(sextants+sextant, gears+gear, scripts+script)
            if score > max_score:
                max_score = score
        return max_score
