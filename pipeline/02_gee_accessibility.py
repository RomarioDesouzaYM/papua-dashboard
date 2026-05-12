import ee

from pipeline.config import init_ee, GEE_FRICTION, CITY_CENTERS
from pipeline.utils import load_boundary, kab_to_ee_features

init_ee()

# Load boundaries first
kab = load_boundary()
kab_ee = kab_to_ee_features(kab)

# Build one Papua geometry from all kabupaten
papua_geom = kab_ee.geometry().bounds()

# Load friction surface and clip to Papua bounding region
friction = ee.Image(GEE_FRICTION).clip(papua_geom)

# Build multi-source image from city centers
city_features = [
    ee.Feature(
        ee.Geometry.Point([c["lon"], c["lat"]]),
        {"name": c["name"]}
    )
    for c in CITY_CENTERS
]

cities_fc = ee.FeatureCollection(city_features)
source_img = ee.Image().byte().paint(cities_fc, 1).clip(papua_geom)

# Compute travel time only inside Papua region
travel_time = friction.cumulativeCost(
    source=source_img,
    maxDistance=2500000
).clip(papua_geom)

# Zonal mean travel time
stats = travel_time.reduceRegions(
    collection=kab_ee,
    reducer=ee.Reducer.mean(),
    scale=10000,
    tileScale=4
)

# Export only required fields, no geometry
def strip_feature(f):
    return ee.Feature(None, {
        "kab_name": f.get("kab_name"),
        "ADM1_EN": f.get("ADM1_EN"),
        "mean": f.get("mean"),
    })

export_table = stats.map(strip_feature)

task = ee.batch.Export.table.toDrive(
    collection=export_table,
    description="travel_time_nearest_city",
    fileFormat="CSV",
    selectors=["kab_name", "ADM1_EN", "mean"],
)

task.start()
print("Accessibility export started -> check GEE Tasks tab")