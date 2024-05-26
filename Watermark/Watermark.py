import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Parámetros de marca de agua
alpha = 0.55  # Fuerza de incrustación
beta = 0.75

# Funciones para cargar imágenes
def cargar_imagen():
    filepath = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg")])
    if filepath:
        img = Image.open(filepath)
        return img, filepath
    return None, None

def preprocesar_imagen(img, size=(256, 256)):
    # Convertir a Blanco y Negro
    img = ImageOps.grayscale(img)
    # Redimensionar a 256x256
    img = img.resize(size)
    return img

def aplicar_marca_agua(base_img, watermark_img, alpha=alpha):
    base = preprocesar_imagen(base_img)
    watermark = preprocesar_imagen(watermark_img)
    # Convertir imágenes a arrays numpy
    base_array = np.array(base, dtype=float) / 255.0
    watermark_array = np.array(watermark, dtype=float) / 255.0
    # Aplicar la marca de agua (la imagen principal será más oscura y la marca de agua más clara)
    combined_array = base_array * (beta) + watermark_array * (1-alpha)
    combined_array = np.clip(combined_array, 0, 1)  # Asegurar que los valores estén en el rango [0, 1]
    combined_image = Image.fromarray(np.uint8(combined_array * 255))
    return combined_image

def mostrar_imagenes(images, titles):
    fig, axs = plt.subplots(1, len(images), figsize=(15, 5))
    for ax, img, title in zip(axs, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

class AplicacionMarcaAgua:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Marca de Agua")

        # Botones de carga
        self.load_base_button = tk.Button(root, text="Cargar Imagen", command=self.cargar_imagen_base)
        self.load_base_button.pack()

        self.load_watermark_button = tk.Button(root, text="Cargar Marca de Agua", command=self.cargar_imagen_marca)
        self.load_watermark_button.pack()

        self.apply_watermark_button = tk.Button(root, text="Aplicar Marca de Agua", command=self.aplicar_marca_agua)
        self.apply_watermark_button.pack()

        self.extract_watermark_button = tk.Button(root, text="Extraer Marca de Agua", command=self.extraer_marca_agua)
        self.extract_watermark_button.pack()

        self.download_button = tk.Button(root, text="Descargar Imagen Marcada", command=self.descargar_imagen)
        self.download_button.pack()

        self.base_image = None
        self.watermark_image = None
        self.marked_image = None
        self.base_filepath = None
        self.watermark_filepath = None

    def cargar_imagen_base(self):
        self.base_image, self.base_filepath = cargar_imagen()
        if self.base_image:
            messagebox.showinfo("Imagen Cargada", "¡Imagen base cargada exitosamente!")

    def cargar_imagen_marca(self):
        self.watermark_image, self.watermark_filepath = cargar_imagen()
        if self.watermark_image:
            messagebox.showinfo("Marca de Agua Cargada", "¡Imagen de marca de agua cargada exitosamente!")

    def aplicar_marca_agua(self):
        if self.base_image and self.watermark_image:
            self.marked_image = aplicar_marca_agua(self.base_image, self.watermark_image)
            self.mostrar_imagen(self.marked_image, "Imagen Marcada")

            # Mostrar imágenes originales y la imagen marcada
            images = [preprocesar_imagen(self.base_image), preprocesar_imagen(self.watermark_image), self.marked_image]
            titles = ['Imagen Base', 'Marca de Agua', 'Imagen Marcada']
            mostrar_imagenes(images, titles)

    def extraer_marca_agua(self):
        if self.base_image and self.marked_image:
            watermark = self.calcular_diferencia(self.marked_image, self.base_image)
            self.mostrar_imagen(watermark, "Marca de Agua Extraída")

            # Mostrar imágenes originales, marcadas y la marca de agua extraída
            images = [preprocesar_imagen(self.base_image), self.marked_image, watermark]
            titles = ['Imagen Base', 'Imagen Marcada', 'Marca de Agua Extraída']
            mostrar_imagenes(images, titles)

    def calcular_diferencia(self, img1, img2):
        img1_array = np.array(preprocesar_imagen(img1), dtype=float)
        img2_array = np.array(preprocesar_imagen(img2), dtype=float)
        difference_array = np.abs(img1_array - img2_array)
        difference_image = Image.fromarray(np.uint8(difference_array))
        return difference_image

    def mostrar_imagen(self, img, title="Imagen"):
        img.show(title=title)

    def descargar_imagen(self):
        if self.marked_image:
            filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("Archivos PNG", "*.png"), ("Todos los archivos", "*.*")])
            if filepath:
                self.marked_image.save(filepath)
                messagebox.showinfo("Imagen Guardada", "¡Imagen marcada guardada exitosamente!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionMarcaAgua(root)
    root.mainloop()