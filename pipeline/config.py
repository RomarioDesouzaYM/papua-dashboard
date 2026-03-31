import os

# ── Scope ─────────────────────────────────────────
YEAR = "2023"
PROVINCE = "Papua"

# EXACT names from shapefile — do not change
KABUPATEN = [
    "Biak Numfor",
    "Jayapura",
    "Keerom",
    "Kepulauan Yapen",
    "Kota Jayapura",
    "Mamberamo Raya",
    "Sarmi",
    "Supiori",
    "Waropen",
]

# Bounding box (Papua region)
PAPUA_BBOX = [-5.0, 132.0, -0.5, 141.5]

# Accessibility anchor (MVP simplification)
CITY_CENTER = {
    "name": "Jayapura",
    "lon": 140.7167,
    "lat": -2.5333,
}

# ── Paths ─────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(ROOT, "data", "processed")
WEB_DIR = os.path.join(ROOT, "web", "public", "indicators")
BOUNDARY = os.path.join(ROOT, "web", "public", "kabupaten.geojson")

# ── GEE datasets ──────────────────────────────────
GEE_VIIRS = "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG"
GEE_FRICTION = "Oxford/MAP/friction_surface_2019"
GEE_HANSEN = "UMD/hansen/global_forest_change_2023_v1_11"

# ── Indicator metadata ────────────────────────────
INDICATORS = {
    "nightlights": {
        "label": "Nighttime light intensity",
        "unit": "mean radiance (normalized 0–100)",
        "source": "NOAA/VIIRS via GEE",
    },
    "infrastructure": {
        "label": "Road density",
        "unit": "km per km² (normalized 0–100)",
        "source": "OSM via OSMnx",
    },
    "accessibility": {
        "label": "Travel time to Jayapura",
        "unit": "minutes (inverted, normalized 0–100)",
        "source": "Oxford friction surface via GEE",
    },
    "social": {
        "label": "Health & education facilities",
        "unit": "count (normalized 0–100)",
        "source": "OSM Overpass API",
    },
    "forest": {
        "label": "Forest loss since 2000",
        "unit": "% loss (raw)",
        "source": "Hansen GFC via GEE",
    }
}
