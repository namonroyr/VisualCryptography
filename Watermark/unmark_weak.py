# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
#from resize_image import resize_image
from skimage.measure import shannon_entropy

# --------------------------------------------------- #
# ----- Unmark an image by linear combination ------- #
# --------------------------------------------------- #
def resize_image(image_array, size):
    image = Image.fromarray(image_array)
    resized_image = image.resize((size[1], size[0]))
    return np.array(resized_image)

def unmark_weak(UN_marked_image, UN_watermark_image, UN_alpha):
    UN_alpha = float(UN_alpha)
    UN_marked_image_entropy = shannon_entropy(UN_marked_image)
    # Get the size of the image to mark
    UN_marked_image_size = UN_marked_image.shape

    # Change watermark size
    UN_watermark_resized = resize_image(UN_watermark_image, UN_marked_image_size)
    UN_watermark_size = UN_watermark_resized.shape


    # Weak marking process
    UN_image = UN_marked_image - UN_alpha * UN_watermark_resized
    # This process is an approximation, since it is not exactly
    # reversible. Some alterations may occur due to loss of
    # information during the embedding process.


    # Presents the entropy of the marked image
    UN_image_entropy = shannon_entropy(UN_image)

    # Similarity indices between images
    # Mean Squared Error (MSE)
    UN_mse_value = np.mean((UN_image - UN_marked_image) ** 2)
    print("Mean Squared Error (MSE):", UN_mse_value)

    # Peak Signal-to-Noise Ratio (PSNR)
    if UN_mse_value == 0:
        UN_psnr_value = float('inf')
    else:
        UN_psnr_value = 20 * np.log10(255 / np.sqrt(UN_mse_value))
    print("Peak Signal-to-Noise Ratio (PSNR):", UN_psnr_value)

    return round(UN_image_entropy, 2), round(UN_marked_image_entropy, 2), round(UN_mse_value, 2), round(UN_psnr_value, 2), UN_image