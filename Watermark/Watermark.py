import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Parámetros de marca de agua
alpha = 0.55  # Fuerza de incrustación

# Funciones para cargar imágenes
def load_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        img = Image.open(filepath)
        return img, filepath
    return None, None

def preprocess_image(img, size=(256, 256)):
    # Convertir a Blanco y Negro
    img = ImageOps.grayscale(img)
    # Redimensionar a 256x256
    img = img.resize(size)
    return img

def apply_watermark(base_img, watermark_img, alpha=alpha):
    base = preprocess_image(base_img)
    watermark = preprocess_image(watermark_img)
    # Convertir imágenes a arrays numpy
    base_array = np.array(base)
    watermark_array = np.array(watermark)
    # Aplicar la marca de agua
    combined_array = alpha * base_array + (1 - alpha) * watermark_array
    combined_image = Image.fromarray(np.uint8(combined_array))
    return combined_image

def show_images(images, titles):
    fig, axs = plt.subplots(1, len(images), figsize=(15, 5))
    for ax, img, title in zip(axs, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")

        # Botones de carga
        self.load_base_button = tk.Button(root, text="Load Image", command=self.load_base_image)
        self.load_base_button.pack()

        self.load_watermark_button = tk.Button(root, text="Load Watermark", command=self.load_watermark_image)
        self.load_watermark_button.pack()

        self.apply_watermark_button = tk.Button(root, text="Apply Watermark", command=self.apply_watermark)
        self.apply_watermark_button.pack()

        self.extract_watermark_button = tk.Button(root, text="Extract Watermark", command=self.extract_watermark)
        self.extract_watermark_button.pack()

        self.base_image = None
        self.watermark_image = None
        self.marked_image = None
        self.base_filepath = None
        self.watermark_filepath = None

    def load_base_image(self):
        self.base_image, self.base_filepath = load_image()
        if self.base_image:
            messagebox.showinfo("Image Loaded", "Base image loaded successfully!")

    def load_watermark_image(self):
        self.watermark_image, self.watermark_filepath = load_image()
        if self.watermark_image:
            messagebox.showinfo("Watermark Loaded", "Watermark image loaded successfully!")

    def apply_watermark(self):
        if self.base_image and self.watermark_image:
            self.marked_image = apply_watermark(self.base_image, self.watermark_image)
            self.show_image(self.marked_image, "Marked Image")

            # Mostrar imágenes originales y la imagen marcada
            images = [preprocess_image(self.base_image), preprocess_image(self.watermark_image), self.marked_image]
            titles = ['Base Image', 'Watermark Image', 'Marked Image']
            show_images(images, titles)

    def extract_watermark(self):
        if self.base_image and self.marked_image:
            watermark = self.calculate_difference(self.marked_image, self.base_image)
            self.show_image(watermark, "Extracted Watermark")

            # Mostrar imágenes originales, marcadas y la marca de agua extraída
            images = [preprocess_image(self.base_image), self.marked_image, watermark]
            titles = ['Base Image', 'Marked Image', 'Extracted Watermark']
            show_images(images, titles)

    def calculate_difference(self, img1, img2):
        img1_array = np.array(preprocess_image(img1))
        img2_array = np.array(preprocess_image(img2))
        difference_array = cv2.absdiff(img1_array, img2_array)
        difference_image = Image.fromarray(difference_array)
        return difference_image

    def show_image(self, img, title="Image"):
        img.show(title=title)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
