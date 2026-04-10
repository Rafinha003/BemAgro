import cv2
import numpy as np
import rasterio
from rasterio.transform import xy
from shapely.geometry import Point
import geopandas as gpd

from config import PASTA_OUTPUT


def extrair_mudas_georreferenciadas(markers: np.ndarray, raster: rasterio.DatasetReader, nome_imagem: str) -> gpd.GeoDataFrame:

    transform = raster.transform
    crs = raster.crs

    geometrias = []
    ids = []

    for label in np.unique(markers):

        if label <= 1:
            continue

        regiao = (markers == label).astype(np.uint8) * 255

        momentos = cv2.moments(regiao)
        if momentos["m00"] == 0:
            continue

        cx = (momentos["m10"] / momentos["m00"])
        cy = (momentos["m01"] / momentos["m00"])

        x, y = xy(transform, cy, cx)

        geometrias.append(Point(x, y))
        ids.append(int(label))

        gdf = gpd.GeoDataFrame(
        {"id": ids},
        geometry=geometrias,
        crs=crs
        )

    gdf_wgs84 = gdf.to_crs("EPSG:4326")

    PASTA_OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = PASTA_OUTPUT / f"mudas_{nome_imagem}.geojson"
    gdf_wgs84.to_file(output_path, driver="GeoJSON")

    return gdf_wgs84