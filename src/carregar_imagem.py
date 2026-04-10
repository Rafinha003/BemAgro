from pathlib import Path
import rasterio

def carregar_imagem(path_img: Path):

    src = rasterio.open(path_img)

    img = src.read([1, 2, 3])

    img = img.transpose([1,2,0])

    img = img.astype("uint8")

    return img,src

def listar_imagens(pasta_input: Path) -> list[Path]:

    if not pasta_input.exists():
        raise FileNotFoundError(F"Pasta não foi encontrada: {pasta_input}")
    
    imagens = sorted(pasta_input.glob("*.tif"))

    if not imagens:
        raise ValueError(f"Nenhum arquivo .tif encontrado em {pasta_input}")
    
    return imagens