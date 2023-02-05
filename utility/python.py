def safe_pop(d: dict, key):
    try:
        return d.pop(key)
    except KeyError:
        return None


def safe_multipop(d: dict, *keys):
    pops = []
    for key in keys:
        pops.append(safe_pop(d, key))
    return pops
