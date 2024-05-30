# Libraries
from PIL import Image
import numpy as np
from skimage.measure import shannon_entropy

# --------------------------------------------------- #
# ------ Mark an image by linear combination -------- #
# --------------------------------------------------- #
def resize_image(image_array, size):
    image = Image.fromarray(image_array)
    resized_image = image.resize((size[1], size[0]))
    return np.array(resized_image)
def weak_watermark(original_image, watermark_image, alpha):
    # Presents the entropy of the image
    image_entropy = shannon_entropy(original_image)
    print(f'Image entropy: {image_entropy}')
    image_size = original_image.shape
    # Change watermark size
    watermark_resized = resize_image(watermark_image, image_size)
    watermark_size = watermark_resized.shape
    # Weak marking process
    marked_image = original_image + alpha * watermark_resized
    # Entropy
    marked_image_entropy = shannon_entropy(marked_image)
    # Similarity indices between images
    # Mean Squared Error (MSE)
    mse_value = np.mean((original_image - marked_image) ** 2)


    # Peak Signal-to-Noise Ratio (PSNR)
    if mse_value == 0:
        psnr_value = float('inf')
    else:
        psnr_value = 20 * np.log10(255 / np.sqrt(mse_value))

    return marked_image_entropy, mse_value, psnr_value, marked_image