import numpy as np
import matplotlib.pyplot as plt

from config import PASTA_IMAGEM


def visualizar_deteccao(img: np.ndarray, markers: np.ndarray, nome_imagem: str) -> None:

    output = img.copy()
    output[markers == -1] = [255, 0, 0]

    plt.figure(figsize=(10, 5))
    plt.imshow(output)
    plt.title(f"Detecção: ")
    plt.axis("off")
    plt.tight_layout()

    PASTA_IMAGEM.mkdir(parents=True, exist_ok=True)
    output_path = PASTA_IMAGEM / f"deteccao_{nome_imagem}.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()