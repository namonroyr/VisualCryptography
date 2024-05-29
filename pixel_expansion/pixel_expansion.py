import numpy as np
from PIL import Image

def pixel_combination_selection(encryp_type=None):
    if encryp_type == "vertical":
        pixel_options = [[0, 1], [1, 0]]
    elif encryp_type == "horizontal":
        pixel_options = [[0, 1], [1, 0]]
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

    if encryp_type == "vertical":

        img_share_1 = np.empty((row, 2 * column)).astype('uint8')
        img_share_2 = np.empty((row, 2 * column)).astype('uint8')

        # se modifican los pixeles de las imágenes a compartir de acuerdo a una selección aleatoria de combinaciones para cada pixel
        for i in range(row):
            for j in range(column):
                pixel_comb = pixel_combination_selection(encryp_type)
                img_share_1[i][2 * j] = img_share_2[i][2 * j] = pixel_comb[0]
                img_share_1[i][2 * j+1] = img_share_2[i][2 * j+1] = pixel_comb[1]

                # Si el pixel original es negro, se reflejan los colores de los pixeles asociados de la imagen 1 a compartir
                # (img_share_1) en la imagen 2 a compartir (img_share_2)
                if input_matrix[i][j] == 0:
                    img_share_2[i][2 * j] = 1 - img_share_2[i][2 * j]
                    img_share_2[i][2 * j+1] = 1 - img_share_2[i][2 * j+1]

    elif encryp_type == "horizontal":

        img_share_1 = np.empty((2 * row, column)).astype('uint8')
        img_share_2 = np.empty((2 * row, column)).astype('uint8')

        # se modifican los pixeles de las imágenes a compartir de acuerdo a una selección aleatoria de combinaciones para cada pixel
        for i in range(row):
            for j in range(column):
                pixel_comb = pixel_combination_selection(encryp_type)
                img_share_1[2 * i][j] = img_share_2[2 * i][j] = pixel_comb[0]
                img_share_1[2 * i + 1][j] = img_share_2[2 * i + 1][j] = pixel_comb[1]

                # Si el pixel original es negro, se reflejan los colores de los pixeles asociados de la imagen 1 a compartir
                # (img_share_1) en la imagen 2 a compartir (img_share_2)
                if input_matrix[i][j] == 0:
                    img_share_2[2 * i][j] = 1 - img_share_2[2 * i][j]
                    img_share_2[2 * i + 1][j] = 1 - img_share_2[2 * i + 1][j]

    else:
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

                # Si el pixel original es negro, se reflejan los colores de los pixeles asociados de la imagen 1 a compartir
                # (img_share_1) en la imagen 2 a compartir (img_share_2)
                if input_matrix[i][j] == 0:
                    img_share_2[2 * i][2 * j] = 1 - img_share_2[2 * i][2 * j]
                    img_share_2[2 * i + 1][2 * j] = 1 - img_share_2[2 * i + 1][2 * j]
                    img_share_2[2 * i][2 * j + 1] = 1 - img_share_2[2 * i][2 * j + 1]
                    img_share_2[2 * i + 1][2 * j + 1] = 1 - img_share_2[2 * i + 1][2 * j + 1]

    return img_share_1, img_share_2, input_matrix


def decrypt(img_share_1, img_share_2):
    '''
    Black -> 0
    White -> 1
    '''
    overlap_matrix = img_share_1 & img_share_2
    (row, column) = img_share_1.shape

    if encryp_type == "vertical":
        row = int(row)
        column = int(column / 2)
        decription_matrix = np.ones((row, column))

        for i in range(row):
            for j in range(column):
                cnt = overlap_matrix[i][2 * j] + overlap_matrix[i][2 * j + 1]
                if cnt == 0:
                    decription_matrix[i][j] = 0

    elif encryp_type == "horizontal":
        row = int(row / 2)
        column = int(column)
        decription_matrix = np.ones((row, column))

        for i in range(row):
            for j in range(column):
                cnt = overlap_matrix[2 * i][j] + overlap_matrix[2 * i + 1][j]
                if cnt == 0:
                    decription_matrix[i][j] = 0

    else:
        row = int(row / 2)
        column = int(column / 2)
        decription_matrix = np.ones((row, column))

        for i in range(row):
            for j in range(column):
                cnt = overlap_matrix[2 * i][2 * j] + overlap_matrix[2 * i + 1][2 * j] + overlap_matrix[2 * i][
                    2 * j + 1] + overlap_matrix[2 * i + 1][2 * j + 1]
                if cnt == 0:
                    decription_matrix[i][j] = 0

    return overlap_matrix, decription_matrix


if __name__ == "__main__":
    # Se lee la imagen como binaria con un
    input_image = Image.open('input_images/lionbw.jpg').convert('1')
    input_image_name = "lionbw"
    encryp_type = "vertical"
    img_share_1, img_share_2, input_matrix = encrypt(input_image, encryp_type)

    image1 = Image.fromarray(img_share_1.astype(np.uint8) * 255)
    image1.save(f"output_images/{input_image_name}_{encryp_type}_img_share_1_.png")
    print("img_share_1 image size (in pixels) : ", image1.size)
    image2 = Image.fromarray(img_share_2.astype(np.uint8) * 255)
    image2.save(f"output_images/{input_image_name}_{encryp_type}_img_share_2.png")
    print("img_share_2 image size (in pixels) : ", image2.size)

    overlap_matrix, decription_matrix = decrypt(img_share_1, img_share_2)
    decripted_image = Image.fromarray(decription_matrix.astype(np.uint8) * 255)
    overlap_image = Image.fromarray(overlap_matrix.astype(np.uint8) * 255)

    overlap_image = overlap_image.resize(input_image.size)
    overlap_image.save(f"output_images/{input_image_name}_img_overlapped.png", mode='1')
    decripted_image.save(f"output_images/{input_image_name}_img_decrypted.png", mode='1')
    