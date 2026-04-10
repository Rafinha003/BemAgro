from pathlib import Path
import json

from config import PASTA_INPUT, PASTA_OUTPUT
from src.carregar_imagem import listar_imagens, carregar_imagem
from src.processamento import processar_imagem
from src.deteccao import detectar_mudas
from src.geo_localizacao import extrair_mudas_georreferenciadas
from src.estatistica_plantio import calcular_estasticas_plantio
from src.metricas_homogeneidade import calcular_metricas_homogeneidade
from src.visualizacao import visualizar_deteccao


def executar_pipeline(path_img: Path) -> None:
    nome = path_img.stem 
 
    img, src = carregar_imagem(path_img)
 
    mask_final = processar_imagem(img)
 
    markers = detectar_mudas(img, mask_final)
 
    gdf_wgs84 = extrair_mudas_georreferenciadas(markers, src, nome)
 
    calcular_estasticas_plantio(gdf_wgs84, src, nome)
 
    calcular_metricas_homogeneidade(gdf_wgs84, src, nome)

    visualizar_deteccao(img, markers, nome)
 
    src.close()


def main() -> None:
    PASTA_OUTPUT.mkdir(parents=True, exist_ok=True)

    imagens = listar_imagens(PASTA_INPUT)

    for path_img in imagens:
        executar_pipeline(path_img)

if __name__ == "__main__":
    main()