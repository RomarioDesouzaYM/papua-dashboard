import ee

from pipeline.config import init_ee, GEE_HANSEN
from pipeline.utils import load_boundary, kab_to_ee_features

init_ee()

kab = load_boundary()
kab_ee = kab_to_ee_features(kab)

gfc = ee.Image(GEE_HANSEN)

loss = gfc.select("lossyear").gt(0).rename("loss_pixels")
treecover = gfc.select("treecover2000").rename("treecover2000")

combined = loss.addBands(treecover)

stats = combined.reduceRegions(
    collection=kab_ee,
    reducer=ee.Reducer.sum(),
    scale=120,
    tileScale=4,
)

def strip_feature(f):
    return ee.Feature(None, {
        "kab_name": f.get("kab_name"),
        "ADM1_EN": f.get("ADM1_EN"),
        "loss_pixels": f.get("loss_pixels"),
        "treecover2000": f.get("treecover2000"),
    })

export_table = stats.map(strip_feature)

task = ee.batch.Export.table.toDrive(
    collection=export_table,
    description="forest_loss_papua",
    fileFormat="CSV",
    selectors=["kab_name", "ADM1_EN", "loss_pixels", "treecover2000"],
)

task.start()
print("Forest export started -> check GEE Tasks tab")