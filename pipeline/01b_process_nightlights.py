import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from config import RAW_DIR
from utils import save_indicator

df = pd.read_csv(f"{RAW_DIR}/ntl_2023.csv")

# Earth Engine export column
df = df.rename(columns={"mean": "ntl_radiance"})

if "ntl_radiance" not in df.columns:
    raise ValueError(f"Expected 'mean' column not found. Columns: {df.columns.tolist()}")

df["ntl_radiance"] = df["ntl_radiance"].fillna(0)

save_indicator("nightlights", df, "ntl_radiance", invert=False)

print("Done: nightlights indicator created")
