import ee, sys, os
sys.path.insert(0, os.path.dirname(__file__))

from config import GEE_VIIRS, YEAR
from utils import boundary_to_ee_features

# Initialize Earth Engine with your project
ee.Initialize(project="papua-dashboard-491902")

# Convert boundaries to EE
kab_ee = boundary_to_ee_features()

# Load VIIRS nighttime lights
viirs = (ee.ImageCollection(GEE_VIIRS)
           .filterDate(f"{YEAR}-01-01", f"{YEAR}-12-31")
           .select("avg_rad")
           .mean())

# Compute mean radiance per kabupaten
stats = viirs.reduceRegions(
    collection=kab_ee,
    reducer=ee.Reducer.mean(),
    scale=500
)

# Export to Google Drive
task = ee.batch.Export.table.toDrive(
    collection=stats,
    description=f"ntl_papua9_{YEAR}",
    fileFormat="CSV"
)

task.start()
print("NTL export started. Check Earth Engine Tasks tab.")
