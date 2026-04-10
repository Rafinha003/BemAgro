import json
import rasterio
import geopandas as gpd

from config import PASTA_OUTPUT


def calcular_estasticas_plantio(gdf_wgs84: gpd.GeoDataFrame, raster: rasterio.DatasetReader, nome_imagem: str) -> dict:

    total_mudas = len(gdf_wgs84)

    gsd_x, gsd_y = raster.res
    pixel_area = abs(gsd_x * gsd_y)
    area_m2 = raster.width * raster.height * pixel_area
    area_ha = area_m2 / 10000

    plantas_por_ha = total_mudas / area_ha if area_ha > 0 else 0

    estatisticas = {
        "total_mudas": int(total_mudas),
        "area_analisada_ha": round(area_ha, 2),
        "plantas_por_hectare": round(plantas_por_ha, 2),
    }

    PASTA_OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = PASTA_OUTPUT / f"estatisticas_{nome_imagem}.json"

    with open(output_path, "w") as f:
        json.dump(estatisticas, f, indent=4)

    return estatisticas