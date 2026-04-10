import json
import numpy as np
import rasterio
import geopandas as gpd
from scipy.spatial import cKDTree
from pyproj import Transformer

from config import PASTA_OUTPUT


def _gini(arr: np.ndarray) -> float:
    arr = np.sort(arr.astype(float))
    n = len(arr)

    if n == 0 or np.sum(arr) == 0:
        return 0.0

    index = np.arange(1, n + 1)
    return float(
        (2 * np.sum(index * arr) - (n + 1) * arr.sum())
        / (n * arr.sum())
    )


def calcular_metricas_homogeneidade(gdf_wgs84: gpd.GeoDataFrame, raster: rasterio.DatasetReader, nome_imagem: str) -> dict:


    transformacao_raster = raster.transform
    raster_crs = raster.crs

    transformer = Transformer.from_crs(
        "EPSG:4326",
        raster_crs,
        always_xy=True
    )

    longitudes = gdf_wgs84.geometry.x.values
    latitudes = gdf_wgs84.geometry.y.values

    x_proj, y_proj = transformer.transform(longitudes, latitudes)

    transformacao_inversa = ~transformacao_raster

    cols, rows = zip(*[
        transformacao_inversa * (x, y)
        for x, y in zip(x_proj, y_proj)
    ])

    coords_px = np.array(list(zip(cols, rows)))

    kd_tree = cKDTree(coords_px)
    distancias_knn, _ = kd_tree.query(coords_px, k=2)
    distancias_vizinho_proximo = distancias_knn[:, 1]

    espacamento_medio_px = float(np.mean(distancias_vizinho_proximo))
    variacao_espacamento_px = float(np.std(distancias_vizinho_proximo, ddof=1))


    raios_influencia = distancias_vizinho_proximo / 2.0
    areas_influencia = np.pi * raios_influencia ** 2

    area_media_influencia_px = float(np.mean(areas_influencia))
    variacao_area_influencia_px = float(np.std(areas_influencia, ddof=1))

    cv_percent = (
        float((variacao_area_influencia_px / area_media_influencia_px) * 100)
        if area_media_influencia_px > 0 else 0.0
    )

    indice_uniformidade = float(max(0.0, 1.0 - (cv_percent / 100)))
    indice_desigualdade = _gini(areas_influencia)

    metricas = {
        "area_media_influencia_px": round(area_media_influencia_px, 2),
        "variacao_area_influencia_px": round(variacao_area_influencia_px, 2),
        "variacao_espacamento_percentual": round(cv_percent, 2),
        "indice_uniformidade_plantio": round(indice_uniformidade, 3),
        "indice_desigualdade_espacial": round(indice_desigualdade, 3),
        "espacamento_medio_mudas": round(espacamento_medio_px, 2),
        "variacao_espacamento_mudas": round(variacao_espacamento_px, 2),
    }

    PASTA_OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = PASTA_OUTPUT / f"metricas_homogeneidade_{nome_imagem}.json"

    with open(output_path, "w") as f:
        json.dump(metricas, f, indent=4)

    return metricas