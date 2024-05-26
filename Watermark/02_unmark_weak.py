# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from resize_image import resize_image
from get_watermark_weight import get_watermark_weight
from skimage.measure import shannon_entropy

# --------------------------------------------------- #
# ----- Unmark an image by linear combination ------- #
# --------------------------------------------------- #

# Read the image to mark
UN_marked_image_dir = r"C:\Users\diego\Desktop\Estevan_watermark\marked_image.png" # Marked Image direction
UN_marked_image = np.array(Image.open(UN_marked_image_dir).convert('L')) # Read in array format for operations


# Presents the entropy of the image
UN_marked_image_entropy = shannon_entropy(UN_marked_image)
print(f'Marked image entropy: {UN_marked_image_entropy}')


# Read the watermark
UN_watermark_dir = r"C:\Users\diego\Desktop\Estevan_watermark\Ciencias_UNAL.jpeg" # Watermark direction
UN_watermark = np.array(Image.open(UN_watermark_dir).convert('L')) # Read in array format for operations 


# Get the size of the image to mark
UN_marked_image_size = UN_marked_image.shape


# Change watermark size
UN_watermark_resized = resize_image(UN_watermark, UN_marked_image_size)
UN_watermark_size = UN_watermark_resized.shape


# Ask the user for the weight of the watermark
UN_alpha = get_watermark_weight()


# Weak marking process
UN_image = UN_marked_image - UN_alpha * UN_watermark_resized
# This process is an approximation, since it is not exactly 
# reversible. Some alterations may occur due to loss of 
# information during the embedding process.


# Presents the entropy of the marked image
UN_image_entropy = shannon_entropy(UN_image)
print(f'Image entropy: {UN_image_entropy}')


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


# Save marked image
plt.imsave('recovered_image.png', UN_image, cmap='gray')


# Print images
# Marked Image
plt.figure()
plt.imshow(UN_marked_image, cmap='gray')
plt.title('Marked image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Watermark resized
plt.figure()
plt.imshow(UN_watermark_resized, cmap='gray')
plt.title('Watermark') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Recovered image
plt.figure()
plt.imshow(UN_image, cmap='gray')
plt.title('Recovered image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()