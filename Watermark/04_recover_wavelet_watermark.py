# Libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from resize_image import resize_image
from get_watermark_weight import get_watermark_weight
from skimage.measure import shannon_entropy
import pywt

# ---------------------------------------------------- #
# ------- Recover watermark from marked image -------- #
# ---------------------------------------------------- #

# Read the marked image
wa_marked_image_dir = r"C:\Users\diego\Desktop\Estevan_watermark\wa_marked_image.png" # Image direction
wa_marked_image = np.array(Image.open(wa_marked_image_dir).convert('L'))

# Embedding force parameter (must be provided by user)
wa_recover_alpha = get_watermark_weight()

# SVD decomposition matrices of the original watermark (need to be provided by the user)
Sy_readed = np.loadtxt(r'C:\Users\diego\Desktop\Estevan_watermark\Sy.txt')
Uw_readed = np.loadtxt(r'C:\Users\diego\Desktop\Estevan_watermark\Uw.txt')
Vw_readed = np.loadtxt(r'C:\Users\diego\Desktop\Estevan_watermark\Vw.txt')

# Apply DWT to marked image
LL1_w, (HL1_w, LH1_w, HH1_w) = pywt.dwt2(wa_marked_image, 'haar')
LL2_w, (HL2_w, LH2_w, HH2_w) = pywt.dwt2(LL1_w, 'haar')

# Apply SVD in component LL2_w
Uw_w, Sw_w, Vw_w = np.linalg.svd(LL2_w, full_matrices=False)

# Recover watermark components
Sw_recovered = (Sw_w - Sy_readed) / wa_recover_alpha

# Reconstruct the watermark image
wa_recovered_watermark = np.dot(Uw_readed * Sw_recovered, Vw_readed)


# Save recovered watermark
plt.imsave('recovered_watermark.png', wa_recovered_watermark, cmap='gray')


# Print images
# Marked Image
plt.figure()
plt.imshow(wa_marked_image, cmap='gray')
plt.title('Marked image') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()

# Recovered watermark
plt.figure()
plt.imshow(wa_recovered_watermark, cmap='gray')
plt.title('Recovered watermark') # Title
plt.xticks([]) # Without x axis
plt.yticks([]) # Without y axis
plt.show()