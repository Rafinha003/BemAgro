import cv2
import numpy as np

from config import MIN_AREA


def processar_imagem(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask_terreno = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)

    img_preprocessada = aplicar_pre_processamento(gray, clip_limit=2.0, tile_size=(8, 8), blur_ksize=7)

    mask_segmentada = segmentar_adaptativo(img_preprocessada, block_size=81, c_value=35)

    mask_filtrada_terreno = cv2.bitwise_and(mask_segmentada, mask_terreno)

    mask_morfologica = limpar_morfologia(mask_filtrada_terreno, kernel_size=(5, 5))
    
    mask_final = filtrar_por_area(mask_morfologica, MIN_AREA)

    return mask_final

def aplicar_pre_processamento(cinza: np.ndarray, clip_limit=2.0, tile_size=(8,8), blur_ksize=7) -> np.ndarray:

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    cinza_aprimorado = clahe.apply(cinza)
    
    return cv2.medianBlur(cinza_aprimorado, blur_ksize)

def segmentar_adaptativo(img_blur: np.ndarray, block_size=81, c_value=35) -> np.ndarray:

    return cv2.adaptiveThreshold(
        img_blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        block_size, c_value
    )

def limpar_morfologia(mask: np.ndarray, kernel_size=(5,5)) -> np.ndarray:

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)

    mask_sem_ruido = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    mask_close = cv2.morphologyEx(mask_sem_ruido, cv2.MORPH_CLOSE, kernel, iterations=2)

    return mask_close

def filtrar_por_area(mask: np.ndarray, min_area: int) -> np.ndarray:
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    nova_mask = np.zeros_like(mask)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            nova_mask[labels == i] = 255
    return nova_mask