import json
import os
import datetime
import pandas as pd

from pipeline.config import PROCESSED_DIR, WEB_DIR, BOUNDARY, INDICATORS

def norm_minmax(series: pd.Series) -> pd.Series:
    """Normalize to [0, 100] using observed Papua-wide min/max."""
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([50.0] * len(series), index=series.index)
    return ((series - mn) / (mx - mn) * 100).round(2)


def save_indicator(name: str, df: pd.DataFrame, value_col: str, invert: bool = False):
    """
    Save one indicator to data/processed/ and web/public/indicators/.
    df must have columns: kab_name, ADM1_EN, [value_col]
    """
    series = df[value_col].copy()
    if invert:
        series = series.max() - series

    df = df.copy()
    df["normalized"] = norm_minmax(series)
    df["raw"] = df[value_col].round(3)

    out = {
        "indicator": name,
        "scope": "Papua and Papua Barat - 42 kabupaten/kota",
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
        print(f"Saved -> {path}")


def load_boundary():
    import geopandas as gpd

    gdf = gpd.read_file(BOUNDARY)
    print(f"Loaded {len(gdf)} kabupaten from boundary file")
    return gdf


def kab_to_ee_features(kab):
    """Convert a GeoDataFrame to a GEE FeatureCollection."""
    import ee

    features = []
    for _, row in kab.iterrows():
        features.append(
            ee.Feature(
                ee.Geometry(row.geometry.__geo_interface__),
                {
                    "kab_name": row["ADM2_EN"],
                    "ADM1_EN": row["ADM1_EN"],
                },
            )
        )

    return ee.FeatureCollection(features)


def boundary_to_ee_features():
    """Load boundary file and convert it to a GEE FeatureCollection."""
    return kab_to_ee_features(load_boundary())