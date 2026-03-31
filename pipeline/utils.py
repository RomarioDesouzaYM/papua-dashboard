import json
import os
import datetime
import pandas as pd
import numpy as np

from config import PROCESSED_DIR, WEB_DIR, INDICATORS

def norm_minmax(series: pd.Series) -> pd.Series:
    """Normalize to [0, 100] using observed min/max of the 9 kabupaten."""
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([50.0] * len(series), index=series.index)
    return ((series - mn) / (mx - mn) * 100).round(2)

def save_indicator(name: str, df: pd.DataFrame, value_col: str, invert: bool = False):
    """
    Save one indicator to data/processed/ and web/public/indicators/.
    df must have columns: kab_name, ADM1_EN, [value_col]
    invert=True for accessibility (less time = better access)
    """
    series = df[value_col].copy()
    if invert:
        series = series.max() - series

    df = df.copy()
    df["normalized"] = norm_minmax(series)
    df["raw"] = df[value_col].round(3)

    out = {
        "indicator": name,
        "scope": "Provinsi Papua - 9 kabupaten/kota",
        "updated": datetime.date.today().isoformat(),
        "unit": INDICATORS[name]["unit"],
        "source": INDICATORS[name]["source"],
        "data": df[["kab_name", "ADM1_EN", "raw", "normalized"]].to_dict(orient="records"),
    }

    for folder in [PROCESSED_DIR, WEB_DIR]:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"  -> {path}")

def load_boundary():
    import geopandas as gpd
    from config import BOUNDARY
    gdf = gpd.read_file(BOUNDARY)
    print(f"Loaded {len(gdf)} kabupaten from boundary file")
    return gdf

def boundary_to_ee_features():
    """Convert GeoDataFrame rows to GEE FeatureCollection."""
    import ee
    gdf = load_boundary()
    features = []
    for _, row in gdf.iterrows():
        features.append(
            ee.Feature(
                ee.Geometry(row.geometry.__geo_interface__),
                {"kab_name": row["ADM2_EN"], "ADM1_EN": row["ADM1_EN"]},
            )
        )
    return ee.FeatureCollection(features)
