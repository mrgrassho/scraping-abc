brand = "(?P<brand>huggies|pampers|babysec)"
size = "\s(pr|rn|p|m|g|xg|xxg)*\s*(\\\/|\-)*\s*(?P<size>pr|rn|p|m|g|xg|xxg)"
units_label_1 = "x\s*(?P<units>[0-9]+)"
units_label2 = "\[(?P<units>[0-9]+)\s*uni.\]"
DIAPERS_REGEX = [
    f".*{brand}.*{size}.*{units_label_1}",
    f".*{brand}.*{size}.*{units_label2}",
]

DIAPER_SIZES = {
    "huggies": {
        "pr": {"min": None, "max": 2.2},
        "rn": {"min": None, "max": 4},
        "p": {"min": 3.5, "max": 6},
        "m": {"min": 5.5, "max": 9.5},
        "g": {"min": 9, "max": 12.5},
        "xg": {"min": 12, "max": 15},
        "xxg": {"min": 14, "max": None},
    },
    "pampers": {
        "rn": {"min": None, "max": 4.5},
        "rn+": {"min": 3, "max": 6},
        "p": {"min": 5, "max": 7.5},
        "m": {"min": 6, "max": 9.5},
        "g": {"min": 9, "max": 12},
        "xg": {"min": 12, "max": 15},
        "xxg": {"min": 14, "max": None},
    },
    "babysec": {
        "rn": {"min": None, "max": 4.5},
        "p": {"min": None, "max": 6},
        "m": {"min": 5, "max": 9.5},
        "g": {"min": 8.5, "max": 12},
        "xg": {"min": 11, "max": 15},
        "xxg": {"min": 13, "max": None},
    },
}

