import os
import ee

# ── Earth Engine ──────────────────────────────────
GEE_PROJECT = "papua-dashboard-491902"

def init_ee():
    ee.Initialize(project=GEE_PROJECT)

# ── Scope ─────────────────────────────────────────
YEAR = "2023"

# Boundary file uses 2020 province names
PROVINCES = ["Papua", "Papua Barat"]

# Bounding box for full Papua + Papua Barat region
PAPUA_BBOX = [-9, 130, 0, 141]

# Multi-city accessibility anchors
CITY_CENTERS = [
    {"name": "Jayapura", "lon": 140.7167, "lat": -2.5333},
    {"name": "Timika", "lon": 136.8872, "lat": -4.5272},
    {"name": "Merauke", "lon": 140.3667, "lat": -8.4667},
    {"name": "Sorong", "lon": 131.2500, "lat": -0.8833},
    {"name": "Wamena", "lon": 138.9500, "lat": -4.0833},
]

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
        "label": "Accessibility to nearest major city",
        "unit": "minutes travel time (inverted, normalized 0–100)",
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
    },
}