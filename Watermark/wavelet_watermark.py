# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
#from resize_image import resize_image
#from get_watermark_weight import get_watermark_weight
from skimage.measure import shannon_entropy
import pywt

# ---------------------------------------------------- #
# Mark an image using Discrete Wavelet Transform (DWT) # 
# ----- and Singular Value Decomposition (SVD) ------- #
# ---------------------------------------------------- #

def resize_image(image_array, size):
    image = Image.fromarray(image_array)
    resized_image = image.resize((size[1], size[0]))
    return np.array(resized_image)

def wavelet_watermark(original_image, watermark_image, wa_alpha):
    image_entropy = shannon_entropy(original_image)
    # DWT and SVD marking process
    #Apply two-level DWT
    wa_alpha = float(wa_alpha)
    LL1, (HL1, LH1, HH1) = pywt.dwt2(original_image, 'haar')
    LL2, (HL2, LH2, HH2) = pywt.dwt2(LL1, 'haar')

    # Get LL2 sizes
    p = LL2.shape

    # Apply SVD in LL2
    Uy, Sy, Vy = np.linalg.svd(LL2, full_matrices=False)

    # Change watermark size
    wa_watermark_resized = resize_image(watermark_image, p)
    wa_watermark_size = wa_watermark_resized.shape

    # Apply SVD on watermark
    Uw, Sw, Vw = np.linalg.svd(wa_watermark_resized, full_matrices=False)
    # Embed watermark
    Smark = Sy + wa_alpha * Sw

    # Rebuild the sub-bands using SVD
    LL2_1 = np.dot(Uy * Smark, Vy)

    # Apply inverse dwt to get watermarked image
    LL1_1 = pywt.idwt2((LL2_1, (HL2, LH2, HH2)), 'haar')
    wa_marked_image = pywt.idwt2((LL1_1, (HL1, LH1, HH1)), 'haar')[:-1, :]

    # Presents the entropy of the marked image
    wa_marked_image_entropy = shannon_entropy(wa_marked_image)
    # Similarity indices between images
    # Mean Squared Error (MSE)
    # Ensure the shapes of the images match
    print(original_image.dtype)
    print(wa_marked_image.dtype)
    wa_marked_image_mod = wa_marked_image
    if original_image.shape != wa_marked_image.shape:
        wa_marked_image_mod = resize_image(wa_marked_image, original_image.shape)

    # Ensure both images are the same data type
    if original_image.dtype != wa_marked_image.dtype:
        wa_marked_image_mod = wa_marked_image.astype(original_image.dtype)
        print("Here")


    if np.any(np.isnan(original_image)) or np.any(np.isnan(wa_marked_image)):
        raise ValueError("One of the images contains NaN values.")
    if np.any(np.isinf(original_image)) or np.any(np.isinf(wa_marked_image)):
        raise ValueError("One of the images contains Inf values.")

        # Check for complex numbers
    if np.iscomplexobj(original_image) or np.iscomplexobj(wa_marked_image):
        raise ValueError("One of the images contains complex numbers.")

    wa_mse_value = np.mean((original_image - wa_marked_image_mod) ** 2)

    # Peak Signal-to-Noise Ratio (PSNR)
    if wa_mse_value == 0:
        wa_psnr_value = float('inf')
    else:
        wa_psnr_value = 20 * np.log10(255 / np.sqrt(wa_mse_value))

    return round(image_entropy, 2), round(wa_marked_image_entropy, 2), round(wa_mse_value,2), round(wa_psnr_value,2), wa_marked_image, Sy, Uw, Vw
