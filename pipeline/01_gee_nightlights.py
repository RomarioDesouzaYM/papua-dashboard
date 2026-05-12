import ee
import pandas as pd
import os

from pipeline.config import init_ee, GEE_VIIRS, YEAR, RAW_DIR
from pipeline.utils import load_boundary, kab_to_ee_features, save_indicator

init_ee()

# Load boundary and convert to GEE features
kab = load_boundary()
kab_ee = kab_to_ee_features(kab)

# VIIRS annual mean for YEAR
viirs = (
    ee.ImageCollection(GEE_VIIRS)
    .filterDate(f"{YEAR}-01-01", f"{YEAR}-12-31")
    .select("avg_rad")
    .mean()
)

# Zonal stats (mean radiance per kabupaten)
stats = viirs.reduceRegions(
    collection=kab_ee,
    reducer=ee.Reducer.mean(),
    scale=500
)

# Export to Google Drive as CSV
task = ee.batch.Export.table.toDrive(
    collection=stats,
    description=f"ntl_papua_{YEAR}",
    fileFormat="CSV"
)

task.start()
print("NTL export started → check https://code.earthengine.google.com Tasks tab")