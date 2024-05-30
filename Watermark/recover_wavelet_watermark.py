# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy
import pywt

# ---------------------------------------------------- #
# ------- Recover watermark from marked image -------- #
# ---------------------------------------------------- #

def resize_image(image_array, size):
    image = Image.fromarray(image_array)
    resized_image = image.resize((size[1], size[0]))
    return np.array(resized_image)

def recover_wavelet_watermark(wa_marked_image, wa_recover_alpha, sy_path, uw_path, vw_path):
    # SVD decomposition matrices of the original watermark (need to be provided by the user)
    Sy_readed = np.loadtxt(sy_path).astype(np.float64)
    Uw_readed = np.loadtxt(uw_path).astype(np.float64)
    Vw_readed = np.loadtxt(vw_path).astype(np.float64)
    wa_recover_alpha = float(wa_recover_alpha)  # Ensure wa_recover_alpha is a float

    # Apply DWT to marked image
    LL1_w, (HL1_w, LH1_w, HH1_w) = pywt.dwt2(wa_marked_image, 'haar')
    LL2_w, (HL2_w, LH2_w, HH2_w) = pywt.dwt2(LL1_w, 'haar')

    # Apply SVD in component LL2_w
    Uw_w, Sw_w, Vw_w = np.linalg.svd(LL2_w, full_matrices=False)
    Sw_w = Sw_w.astype(np.float64)  # Ensure Sw_w is a float

    # Recover watermark components
    Sw_recovered = (Sw_w - Sy_readed) / wa_recover_alpha

    # Reconstruct the watermark image
    wa_recovered_watermark = np.dot(Uw_readed * Sw_recovered, Vw_readed)

    return wa_recovered_watermark