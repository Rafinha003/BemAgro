import cv2
import numpy as np


def detectar_mudas(img: np.ndarray, mask_final: np.ndarray) -> np.ndarray:
    foreground_mask = calcular_distance_transform(mask_final, distance_factor=0.4)

    markers = definir_regioes_marcadores(mask_final, foreground_mask)

    img_ws = preparar_imagem_watershed(img)

    markers = cv2.watershed(img_ws, markers)

    return markers

def calcular_distance_transform(mask: np.ndarray, distance_factor=0.4) -> np.ndarray:
    mask_binaria = (mask > 0).astype(np.uint8)
    dist_transform = cv2.distanceTransform(mask_binaria, cv2.DIST_L2, 5)

    threshold_val = distance_factor * dist_transform.max()

    _, foreground_mask = cv2.threshold(dist_transform, threshold_val, 255, 0)
    return np.uint8(foreground_mask)

def definir_regioes_marcadores(mask: np.ndarray, foreground_mask: np.ndarray) -> np.ndarray:
    
    kernel = np.ones((3,3), np.uint8)
    background_mask = cv2.dilate(mask, kernel, iterations=2)
    regiao_desconhecida = cv2.subtract(background_mask, foreground_mask)

    _, markers = cv2.connectedComponents(foreground_mask)

    markers = markers + 1
    markers[regiao_desconhecida > 0] = 0
    
    return markers

def preparar_imagem_watershed(img: np.ndarray) -> np.ndarray:
    img_preparada = img.copy()

    if img_preparada.dtype != np.uint8:
        img_preparada = cv2.normalize(img_preparada, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    return img_preparada

