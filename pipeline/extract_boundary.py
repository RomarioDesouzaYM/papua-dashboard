import geopandas as gpd

TARGET = [
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

gdf = gpd.read_file("data/raw/idn_admbnda_adm2_bps_20200401.shp")

papua = gdf[gdf["ADM2_EN"].isin(TARGET)].copy()

print(f"Total rows: {len(papua)}")
print("\nSelected ADM2 names:")
for name in sorted(papua["ADM2_EN"].unique()):
    print("-", name)

papua["geometry"] = papua.geometry.simplify(
    tolerance=0.005,
    preserve_topology=True
)

papua = papua[["ADM2_EN", "ADM1_EN", "Shape_Area", "geometry"]]
papua.to_file("web/public/kabupaten.geojson", driver="GeoJSON")

print(f"\nSaved {len(papua)} kabupaten to web/public/kabupaten.geojson")
