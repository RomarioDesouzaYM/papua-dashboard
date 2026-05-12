import geopandas as gpd

# Load ADM2 shapefile (kabupaten)
gdf = gpd.read_file("data/raw/idn_admbnda_adm2_bps_20200401.shp")

# Filter Papua provinces
SCOPE = [
    "Papua",
    "Papua Barat"
]

papua = gdf[gdf["ADM1_EN"].isin(SCOPE)].copy()

print(f"Kabupaten count: {len(papua)}")

# Simplify geometry for web performance
papua["geometry"] = papua.geometry.simplify(
    tolerance=0.005,
    preserve_topology=True
)

# Keep only required fields
papua = papua[["ADM2_EN", "ADM1_EN", "Shape_Area", "geometry"]]

# Save as GeoJSON for frontend
papua.to_file("web/public/kabupaten.geojson", driver="GeoJSON")

print("Saved → web/public/kabupaten.geojson")