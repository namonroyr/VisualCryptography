# Libraries
from PIL import Image
import numpy as np

# Function that resizes images in array format
def resize_image(image_array, size):
    image = Image.fromarray(image_array)
    resized_image = image.resize((size[1], size[0]))
    return np.array(resized_image)