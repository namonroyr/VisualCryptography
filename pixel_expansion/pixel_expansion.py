import numpy as np
from PIL import Image

def pixel_combination_selection(encryp_type=None):
    if encryp_type == "vertical":
        pixel_options = [[0, 0, 1, 1], [1, 1, 0, 0]]
    elif encryp_type == "horizontal":
        pixel_options = [[1, 0, 1, 0], [0, 1, 0, 1]]
    elif encryp_type == "4-pixeles":
        pixel_options = [[1, 0, 0, 1], [0, 1, 1, 0]]
    else:
        pixel_options = [[0, 0, 1, 1], [1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [0, 1, 0, 1]]
    return np.array(pixel_options[np.random.randint(0, len(pixel_options))])

def encrypt(input_image, encryp_type):
    """
    Negro --> 0
    Blanco --> 1
    """

    # arreglo de pixeles de la imagen original
    input_matrix = np.asarray(input_image).astype(np.uint8)
    # dimensiones imagen original
    (row, column) = input_matrix.shape
    # se crean los arreglos para almacenar las imágenes a compartir (share 1 & share 2)
    img_share_1 = np.empty((2 * row, 2 * column)).astype('uint8')
    img_share_2 = np.empty((2 * row, 2 * column)).astype('uint8')

    # se modifican los pixeles de las imágenes a compartir de acuerdo a una selección aleatoria de combinaciones para cada pixel
    for i in range(row):
        for j in range(column):
            pixel_comb = pixel_combination_selection(encryp_type)
            img_share_1[2 * i][2 * j] = img_share_2[2 * i][2 * j] = pixel_comb[0]
            img_share_1[2 * i + 1][2 * j] = img_share_2[2 * i + 1][2 * j] = pixel_comb[1]
            img_share_1[2 * i][2 * j + 1] = img_share_2[2 * i][2 * j + 1] = pixel_comb[2]
            img_share_1[2 * i + 1][2 * j + 1] = img_share_2[2 * i + 1][2 * j + 1] = pixel_comb[3]
            #img_share_2 = img_share_1.copy()

            # Si el pixel original es negro, se reflejan los colores de los pixeles asociados de la imagen 1 a compartir
            # (img_share_1) en la imagen 2 a compartir (img_share_2)
            if input_matrix[i][j] == 0:
                img_share_2[2 * i][2 * j] = 1 - img_share_2[2 * i][2 * j]
                img_share_2[2 * i + 1][2 * j] = 1 - img_share_2[2 * i + 1][2 * j]
                img_share_2[2 * i][2 * j + 1] = 1 - img_share_2[2 * i][2 * j + 1]
                img_share_2[2 * i + 1][2 * j + 1] = 1 - img_share_2[2 * i + 1][2 * j + 1]

    overlap_matrix = img_share_1 & img_share_2

    return img_share_1, img_share_2, overlap_matrix, input_matrix


if __name__ == "__main__":
    # Se lee la imagen como binaria con un
    input_image = Image.open('input_images/cat_samplee.jpg').convert('1')
    input_image_name = "cat_samplee"
    encryp_type = "4-pixeles"
    img_share_1, img_share_2, overlap_matrix, input_matrix = encrypt(input_image, encryp_type)

    image1 = Image.fromarray(img_share_1.astype(np.uint8) * 255)
    image1.save(f"output_images/{input_image_name}_img_share_1.png")
    print("secret_share1 image size (in pixels) : ", image1.size)
    image2 = Image.fromarray(img_share_2.astype(np.uint8) * 255)
    image2.save(f"output_images/{input_image_name}_img_share_2.png")
    print("secret_share2 image size (in pixels) : ", image2.size)

    overlap_image = Image.fromarray(overlap_matrix.astype(np.uint8) * 255)
    overlap_image = overlap_image.resize(input_image.size)
    overlap_image.save(f"output_images/{input_image_name}_img_overlapped.png", mode='1')