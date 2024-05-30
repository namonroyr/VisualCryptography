# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from resize_image import resize_image
from get_watermark_weight import get_watermark_weight
from skimage.measure import shannon_entropy
import pywt

# ---------------------------------------------------- #
# Mark an image using Discrete Wavelet Transform (DWT) # 
# ----- and Singular Value Decomposition (SVD) ------- #
# ---------------------------------------------------- #

# Read the image to mark
wa_image_dir = r"C:\Users\diego\Desktop\Estevan_watermark\Johann_Sebastian_Bach.jpg" # Image direction
wa_image = np.array(Image.open(wa_image_dir).convert('L')) # Read in array format for operations


# Presents the entropy of the image
wa_image_entropy = shannon_entropy(wa_image)
print(f'Image entropy: {wa_image_entropy}')


# Read the watermark
wa_watermark_dir = r"C:\Users\diego\Desktop\Estevan_watermark\Ciencias_UNAL.jpeg" # Watermark direction
wa_watermark = np.array(Image.open(wa_watermark_dir).convert('L')) # Read in array format for operations 


# Ask the user for the weight of the watermark
wa_alpha = get_watermark_weight()


# DWT and SVD marking process
#Apply two-level DWT
LL1, (HL1, LH1, HH1) = pywt.dwt2(wa_image, 'haar')
LL2, (HL2, LH2, HH2) = pywt.dwt2(LL1, 'haar')

# Get LL2 sizes
p = LL2.shape

# Apply SVD in LL2
Uy, Sy, Vy = np.linalg.svd(LL2, full_matrices=False)

# Change watermark size
wa_watermark_resized = resize_image(wa_watermark, p)
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
print(f'Marked image entropy: {wa_marked_image_entropy}')


# Similarity indices between images
# Mean Squared Error (MSE)
wa_mse_value = np.mean((wa_image - wa_marked_image) ** 2)
print("Mean Squared Error (MSE):", wa_mse_value)

# Peak Signal-to-Noise Ratio (PSNR)
if wa_mse_value == 0:
    wa_psnr_value = float('inf')
else:
    wa_psnr_value = 20 * np.log10(255 / np.sqrt(wa_mse_value))
print("Peak Signal-to-Noise Ratio (PSNR):", wa_psnr_value)


# Save marked image
plt.imsave('wa_marked_image.png', wa_marked_image, cmap='gray')


# The following values ​​are necessary to 
# be able to recover the watermark
print()
print("Save the following if you want to recover the watermark used")
print("weight of the watermark, alpha=", wa_alpha)
print("Singular values of image with DWT, Matrix Sy.")
np.savetxt('Sy.txt', Sy)
print("U matrix of SVD in watermark resized, Matrix Uw.")
np.savetxt('Uw.txt', Uw)
print("V matrix of SVD in watermark resized, Matrix Vw.")
np.savetxt('Vw.txt', Vw)


# Print images
# Normal Image
plt.figure()
plt.imshow(wa_image, cmap='gray')
plt.title('Image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Watermark resized
plt.figure()
plt.imshow(wa_watermark, cmap='gray')
plt.title('Watermark') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Marked image
plt.figure()
plt.imshow(wa_marked_image, cmap='gray')
plt.title('Marked image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()