# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from resize_image import resize_image
from get_watermark_weight import get_watermark_weight
from skimage.measure import shannon_entropy

# --------------------------------------------------- #
# ------ Mark an image by linear combination -------- #
# --------------------------------------------------- #

# Read the image to mark
image_dir = r"C:\Users\diego\Desktop\Estevan_watermark/Johann_Sebastian_Bach.jpg" # Image direction
image = np.array(Image.open(image_dir).convert('L')) # Read in array format for operations


# Presents the entropy of the image
image_entropy = shannon_entropy(image)
print(f'Image entropy: {image_entropy}')


# Read the watermark
watermark_dir = r"C:\Users\diego\Desktop\Estevan_watermark/Ciencias_UNAL.jpeg" # Watermark direction
watermark = np.array(Image.open(watermark_dir).convert('L')) # Read in array format for operations 


# Get the size of the image to mark
image_size = image.shape


# Change watermark size
watermark_resized = resize_image(watermark, image_size)
watermark_size = watermark_resized.shape


# Ask the user for the weight of the watermark
alpha = get_watermark_weight()


# Weak marking process
marked_image = image + alpha * watermark_resized


# Presents the entropy of the marked image
marked_image_entropy = shannon_entropy(marked_image)
print(f'Marked image entropy: {marked_image_entropy}')


# Similarity indices between images
# Mean Squared Error (MSE)
mse_value = np.mean((image - marked_image) ** 2)
print("Mean Squared Error (MSE):", mse_value)

# Peak Signal-to-Noise Ratio (PSNR)
if mse_value == 0:
    psnr_value = float('inf')
else:
    psnr_value = 20 * np.log10(255 / np.sqrt(mse_value))
print("Peak Signal-to-Noise Ratio (PSNR):", psnr_value)


# Save marked image
plt.imsave('marked_image.png', marked_image, cmap='gray')


# Print images
# Normal Image
plt.figure()
plt.imshow(image, cmap='gray')
plt.title('Image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Watermark resized
plt.figure()
plt.imshow(watermark_resized, cmap='gray')
plt.title('Watermark') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Marked image
plt.figure()
plt.imshow(marked_image, cmap='gray')
plt.title('Marked image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()