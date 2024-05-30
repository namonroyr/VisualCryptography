import sys
import os
import math
import cv2
import numpy as np
import string
import string
import itertools
import random
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDialog, QTableWidget, QMenu,
                             QTableWidgetItem, QAbstractItemView, QLineEdit, QTabWidget,
                             QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox, QStackedLayout,
                             QDateEdit, QComboBox, QPushButton, QFileDialog, QPlainTextEdit, QLineEdit,
                             QTextEdit, QSpinBox)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,
                         QRegExpValidator, QImage, QCursor)


from pixel_expansion.pixel_expansion import encrypt as pe_encrypt
from pixel_expansion.pixel_expansion import decrypt as pe_decrypt
from Watermark.weak_watermark import weak_watermark as weak_watermark_encrypt


# Modes of padding
PAD_NORMAL = 1
PAD_PKCS5 = 2


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, 'MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class PhotoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        # self.resize(300,650)
        self.setText('\n\n Drop image Here \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
            font: 17px;
        }''')

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')


class Template(QWidget):
    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        self.file = ""
        self.setAcceptDrops(True)
        grid = QGridLayout(self)
        grid.addWidget(self.photo, 0, 0)
        self.resize(self.sizeHint())

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.file = filename
            self.open_image(filename)
        else:
            event.ignore()

    def open_image(self, filename=None):
        pixmap = QPixmap(filename)

        self.photo.setPixmap(pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.FastTransformation))

def crearBoton(cifrado):
    if cifrado:
        boton = QPushButton(text="Encrypt")
    else:
        boton = QPushButton(text="Decrypt")
    boton.setStyleSheet(
        """
        QPushButton {
            border-radius:5%;
            padding:5px;
            background:#52F6E0;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #13A5EE;
            color:white;
            font: bold;
            }
        """)
    boton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    boton.setFixedWidth(150)
    return boton

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()

        # Set window title and fixed size
        self.setWindowTitle('PixelSafe')
        self.setFixedSize(1250, 702)

        # Set background image
        self.setStyleSheet("QDialog {background-image: url('resources/app_logo4_mod.png'); background-position: bottom left; "
                           "background-repeat: no-repeat;}")

        # Set up main layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignRight)

        # Logo display
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap('resources/app_name.png').scaled(450, 450, Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent;")  # Make logo background transparent


        # Button styles
        buttonStyle = """
        QPushButton {
            width: 200px;
            padding: 15px;
            margin: 10px;
            border-radius: 10px;
            background: #223C54;
            color: #8BEFFF;
            font-size: 14pt;
        }
        QPushButton:hover {
            background-color: #8BEFFF;
            color: #223C54;
        }
        """

        # Buttons
        self.watermark_button = QPushButton("Watermark")
        self.pixel_expansion_button = QPushButton("Pixel Expansion")

        self.watermark_button.setStyleSheet(buttonStyle)
        self.pixel_expansion_button.setStyleSheet(buttonStyle)

        # Connect buttons to their respective functions
        self.watermark_button.clicked.connect(self.go_to_watermark)
        self.pixel_expansion_button.clicked.connect(self.go_to_pixel_expansion)

        # Add logo, tagline, and buttons to the layout
        vbox.addWidget(self.logo_label)
        vbox.addWidget(self.watermark_button)
        vbox.addWidget(self.pixel_expansion_button)
        vbox.setContentsMargins(100, 50, 130, 50)
        self.setLayout(vbox)

    def go_to_watermark(self):
        print("Watermark button clicked")

    def go_to_pixel_expansion(self):
        widget.setCurrentIndex(1)

class PixelExpansion(QDialog):

    def __init__(self):
        super(PixelExpansion, self).__init__()

        def PixelExpButton(encriptar, encrypt_type, input, img_share_1,  img_share_2):
            # Set sizes

                if encriptar == True:
                    image_file_name = input.file
                    img_name = image_file_name.split('.')[0].split('/')[-1]
                    img_extension = image_file_name.split('.')[1]
                    if image_file_name != "":
                        # convert original img to bytes
                        img = Image.open(image_file_name).convert('1')
                        img_s_1, img_s_2, input_matrix = pe_encrypt(img, encrypt_type)
                        image1 = Image.fromarray(img_s_1.astype(np.uint8) * 255)
                        image1.save(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_1.png")

                        image2 = Image.fromarray(img_s_2.astype(np.uint8) * 255)
                        image2.save(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_2.png")
                        QMessageBox.information(None, 'Success',
                                                "You can find the shared secrets images in the output_images folder.",
                                                QMessageBox.Ok)

                        img_share_1.open_image(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_1.png")
                        img_share_2.open_image(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_2.png")
                    else:
                        QMessageBox.critical(None, 'There is no image',
                                             'Drop an image to process or one with a valid format (.jpg, .png)',
                                             QMessageBox.Ok)


                elif encriptar == False:
                    img_share_1_file_name = img_share_1.file
                    org_img_name = img_share_1_file_name.split('/')[-1].split('.')[0].split('_')[0]
                    img_extension_1 = img_share_1_file_name.split('.')[1]
                    img_share_2_file_name = img_share_2.file
                    img_extension_2 = img_share_2_file_name.split('.')[1]

                    if img_share_1_file_name != "" and img_share_2_file_name != "":

                        img1 = Image.open(img_share_1_file_name).convert('1')
                        img2 = Image.open(img_share_2_file_name).convert('1')
                        image_array_s1 = np.asarray(img1)
                        image_array_s2 = np.asarray(img2)
                        overlap_matrix, decription_matrix = pe_decrypt(image_array_s1, image_array_s2, encrypt_type)

                        decripted_image = Image.fromarray(decription_matrix.astype(np.uint8) * 255)
                        overlap_image = Image.fromarray(overlap_matrix.astype(np.uint8) * 255)
                        #overlap_image = overlap_image.resize(img.size)
                        overlap_image.save(f"pixel_expansion/output_images/{org_img_name}_{encrypt_type}_overlapped.png", mode='1')
                        decripted_image.save(f"pixel_expansion/output_images/{org_img_name}_{encrypt_type}_decrypted.png", mode='1')
                        QMessageBox.information(None, 'Success',
                                                'You can find the decrypted and overlapped image in the output_images folder.',
                                                QMessageBox.Ok)
                        input.open_image(f"pixel_expansion/output_images/{org_img_name}_{encrypt_type}_decrypted.png")
                    else:
                        QMessageBox.critical(None, 'There is no image',
                                             'Drop an image to process or one with a valid format (.jpg, .png)',
                                             QMessageBox.Ok)

        gridBlock = QGridLayout()
        gridBlock.setGeometry(QtCore.QRect(10, 10, 1400, 702))
        h1box = QHBoxLayout()
        h2box = QHBoxLayout()
        h3box = QHBoxLayout()

        encryption_label = QLabel()
        encryption_label.setPixmap(QPixmap('resources/encrypt.png').scaled(350, 350, Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation))
        decryption_label = QLabel()
        decryption_label.setPixmap(QPixmap('resources/decrypt.png').scaled(350, 350, Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation))

        txt_block = QLabel()
        txt_block.setText("Type: ")
        label_style = '''
        QLabel {
            font-size: 28px;
            font-family: Segoe UI;
        }'''
        txt_block.setStyleSheet(label_style)
        encrypt_types = ["2-pixeles-horizontal", "2-pixeles-vertical", "4-pixeles"]
        encrypt_types_combo = QComboBox()
        comboblock_style = """
        QComboBox {
            padding: 5px;
            border-radius:3%;
            font-size: 24px;
            background-color: #8BEFFF;
            color: #02182C;
        }
        QComboBox::drop-down
        {
            border: 0px;
            width: 20px;
        }
        QComboBox::down-arrow {
            image: url(resources/dropdown.png);
            width: 12px;
            height: 12px;
        }
        """
        encrypt_types_combo.setStyleSheet(comboblock_style)
        encrypt_types_combo.addItems(encrypt_types)
        h1box.addWidget(encryption_label)
        h2box.addWidget(decryption_label)
        h1box.setAlignment(Qt.AlignCenter)
        h2box.setAlignment(Qt.AlignCenter)

        h3box.addWidget(txt_block)
        h3box.addWidget(encrypt_types_combo)
        h3box.setAlignment(Qt.AlignCenter)

        img_c = Template()
        img_ss1 = Template()
        img_ss2 = Template()

        txt_img = QLabel()
        txt_img.setText("Image to encrypt / decrypted: ")
        txt_img.setAlignment(Qt.AlignCenter)
        txt_img.setStyleSheet('''
        QLabel {
            font-size: 30px;
            font-family: Segoe UI;
        }''')
        txt_img_ss1 = QLabel()
        txt_img_ss1.setText("Secret Share 1: ")
        txt_img_ss1.setAlignment(Qt.AlignCenter)
        txt_img_ss1.setStyleSheet('''
        QLabel {
            font-size: 30px;
            font-family: Segoe UI;
        }''')
        txt_img_ss2 = QLabel()
        txt_img_ss2.setText("Secret Share 2: ")
        txt_img_ss2.setAlignment(Qt.AlignCenter)
        txt_img_ss2.setStyleSheet('''
                QLabel {
                    font-size: 30px;
                    font-family: Segoe UI;
                }''')

        h4box = QHBoxLayout()
        h5box = QHBoxLayout()
        h6box = QHBoxLayout()
        h7box = QHBoxLayout()


        boton_cifrar_pe = crearBoton(cifrado=True)
        boton_descifrar_pe = crearBoton(cifrado=False)
        boton_cifrar_pe.clicked.connect(
            lambda: PixelExpButton(encriptar=True, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c, img_share_1=img_ss1, img_share_2=img_ss2))
        boton_descifrar_pe.clicked.connect(
            lambda: PixelExpButton(encriptar=False, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c, img_share_1=img_ss1, img_share_2=img_ss2))
        boton_limpiar = QPushButton(text="Clean")
        aux_style = """
        QPushButton {
            border-radius:5%;
            padding:5px;
            background:#9E6CFA;
            color:white;
        }
        QPushButton:hover {
            background-color:#4DB4FA;
            }
            """
        boton_limpiar.setStyleSheet(aux_style)
        boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar.setFixedWidth(150)
        boton_limpiar.clicked.connect(lambda: clean(gridBlock, img_c, img_ss1, img_ss2, h4box, h5box, boton_cifrar_pe, boton_descifrar_pe))

        def clean(gridBlock, img_c, img_ss1, img_ss2, h4box, h5box, boton_cifrar_pe, boton_descifrar_pe):
            boton_cifrar_pe.setParent(None)
            boton_descifrar_pe.setParent(None)
            img_c.setParent(None)
            img_ss1.setParent(None)
            img_ss2.setParent(None)
            h4box.setParent(None)
            h5box.setParent(None)
            img_c = Template()
            img_ss1 = Template()
            img_ss2 = Template()
            h4box = QHBoxLayout()
            h5box = QHBoxLayout()
            boton_cifrar_pe = crearBoton(cifrado=True)
            boton_descifrar_pe = crearBoton(cifrado=False)
            boton_cifrar_pe.clicked.connect(
                lambda: PixelExpButton(encriptar=True, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c, img_share_1=img_ss1, img_share_2=img_ss2))
            boton_descifrar_pe.clicked.connect(
                lambda: PixelExpButton(encriptar=False, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c,img_share_1=img_ss1, img_share_2=img_ss2))
            gridBlock.addWidget(img_c, 3, 0, 6, 1)
            gridBlock.addWidget(img_ss1, 3, 1, 6, 1)
            gridBlock.addWidget(img_ss2, 3, 2, 6, 1)
            h4box.addWidget(boton_cifrar_pe)
            h5box.addWidget(boton_descifrar_pe)
            gridBlock.addLayout(h4box, 10, 0, 1, 1)
            gridBlock.addLayout(h5box, 10, 1, 1, 2)


        txt_key2 = QLabel()
        txt_key2.setText('*Note: Clean fields before encrypting/decrypting')
        txt_key2.setStyleSheet('''
                QLabel {
                    font-size: 22px;
                    font-family: Segoe UI;
                }''')

        self.back_button = QPushButton("Back")
        back_buttonStyle = """
        QPushButton {
            width: 230px;
            border-radius: 5%;
            padding: 5px;
            background: #8DD3F6;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #4DB4FA;
            color: white;
        }
        """
        self.back_button.setStyleSheet(back_buttonStyle)
        self.back_button.clicked.connect(lambda: widget.setCurrentIndex(0))




        #gridBlock.addWidget(h3box, 1, 1)
        gridBlock.addLayout(h1box, 0, 0)
        gridBlock.addLayout(h2box, 0, 1, 1, 2)
        h2box.setAlignment(Qt.AlignCenter)
        gridBlock.addLayout(h3box, 1, 0, 1, 3)
        h3box.setAlignment(Qt.AlignCenter)
        gridBlock.addWidget(txt_img, 2, 0)
        gridBlock.addWidget(txt_img_ss1, 2, 1)
        gridBlock.addWidget(txt_img_ss2, 2, 2)
        gridBlock.addWidget(img_c, 3, 0, 6, 1)
        gridBlock.addWidget(img_ss1, 3, 1, 6, 1)
        gridBlock.addWidget(img_ss2, 3, 2, 6, 1)
        h4box.addWidget(boton_cifrar_pe)
        h5box.addWidget(boton_descifrar_pe)
        gridBlock.addLayout(h4box, 10, 0, 1, 1)
        gridBlock.addLayout(h5box, 10, 1, 1, 2)
        h6box.addWidget(self.back_button)
        h7box.addWidget(boton_limpiar)
        h7box.addWidget(txt_key2)
        gridBlock.addLayout(h6box, 11, 0, 1, 1)
        h6box.setAlignment(Qt.AlignCenter)
        gridBlock.addLayout(h7box, 11, 1, 1, 2)
        h7box.setAlignment(Qt.AlignCenter)
        self.setLayout(gridBlock)

class Watermark(QDialog):
    def __init__(self):
        super(PixelExpansion, self).__init__()

        def Watermark(encriptar, encrypt_type, org_img, water_img, alpha, Sy=None, Uw=None, Vw=None):
            # Set sizes

                if encriptar == True:
                    org_img_file_name = org_img.file
                    water_img_file_name = water_img.file
                    org_img_name = org_img_file_name.split('.')[0].split('/')[-1]
                    water_img_name = water_img_file_name('.')[0].split('/')[-1]
                    if org_img_file_name != "" and water_img_file_name != "":
                        # convert original img to bytes
                        org_image_array = np.array(Image.open(org_img_file_name).convert('L'))
                        water_image_array = np.array(Image.open(water_img_file_name).convert('L'))


                        img_s_1, img_s_2, input_matrix = pe_encrypt(img, encrypt_type)
                        image1 = Image.fromarray(img_s_1.astype(np.uint8) * 255)
                        image1.save(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_1.png")

                        image2 = Image.fromarray(img_s_2.astype(np.uint8) * 255)
                        image2.save(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_2.png")
                        QMessageBox.information(None, 'Success',
                                                "You can find the shared secrets images in the output_images folder.",
                                                QMessageBox.Ok)

                        img_share_1.open_image(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_1.png")
                        img_share_2.open_image(f"pixel_expansion/output_images/{img_name}_{encrypt_type}_img_share_2.png")
                    else:
                        QMessageBox.critical(None, 'There is no image',
                                             'Drop an image to process or one with a valid format (.jpg, .png)',
                                             QMessageBox.Ok)


                elif encriptar == False:
                    img_share_1_file_name = img_share_1.file
                    org_img_name = img_share_1_file_name.split('/')[-1].split('.')[0].split('_')[0]
                    img_extension_1 = img_share_1_file_name.split('.')[1]
                    img_share_2_file_name = img_share_2.file
                    img_extension_2 = img_share_2_file_name.split('.')[1]

                    if img_share_1_file_name != "" and img_share_2_file_name != "":

                        img1 = Image.open(img_share_1_file_name).convert('1')
                        img2 = Image.open(img_share_2_file_name).convert('1')
                        image_array_s1 = np.asarray(img1)
                        image_array_s2 = np.asarray(img2)
                        overlap_matrix, decription_matrix = pe_decrypt(image_array_s1, image_array_s2, encrypt_type)

                        decripted_image = Image.fromarray(decription_matrix.astype(np.uint8) * 255)
                        overlap_image = Image.fromarray(overlap_matrix.astype(np.uint8) * 255)
                        #overlap_image = overlap_image.resize(img.size)
                        overlap_image.save(f"pixel_expansion/output_images/{org_img_name}_{encrypt_type}_overlapped.png", mode='1')
                        decripted_image.save(f"pixel_expansion/output_images/{org_img_name}_{encrypt_type}_decrypted.png", mode='1')
                        QMessageBox.information(None, 'Success',
                                                'You can find the decrypted and overlapped image in the output_images folder.',
                                                QMessageBox.Ok)
                        input.open_image(f"pixel_expansion/output_images/{org_img_name}_{encrypt_type}_decrypted.png")
                    else:
                        QMessageBox.critical(None, 'There is no image',
                                             'Drop an image to process or one with a valid format (.jpg, .png)',
                                             QMessageBox.Ok)

        gridBlock = QGridLayout()
        gridBlock.setGeometry(QtCore.QRect(10, 10, 1400, 702))
        h1box = QHBoxLayout()
        h2box = QHBoxLayout()
        h3box = QHBoxLayout()

        encryption_label = QLabel()
        encryption_label.setPixmap(QPixmap('resources/encrypt.png').scaled(350, 350, Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation))
        decryption_label = QLabel()
        decryption_label.setPixmap(QPixmap('resources/decrypt.png').scaled(350, 350, Qt.KeepAspectRatio,
                                                                           Qt.SmoothTransformation))

        txt_block = QLabel()
        txt_block.setText("Type: ")
        label_style = '''
        QLabel {
            font-size: 28px;
            font-family: Segoe UI;
        }'''
        txt_block.setStyleSheet(label_style)
        encrypt_types = ["2-pixeles-horizontal", "2-pixeles-vertical", "4-pixeles"]
        encrypt_types_combo = QComboBox()
        comboblock_style = """
        QComboBox {
            padding: 5px;
            border-radius:3%;
            font-size: 24px;
            background-color: #8BEFFF;
            color: #02182C;
        }
        QComboBox::drop-down
        {
            border: 0px;
            width: 20px;
        }
        QComboBox::down-arrow {
            image: url(resources/dropdown.png);
            width: 12px;
            height: 12px;
        }
        """
        encrypt_types_combo.setStyleSheet(comboblock_style)
        encrypt_types_combo.addItems(encrypt_types)
        h1box.addWidget(encryption_label)
        h2box.addWidget(decryption_label)
        h1box.setAlignment(Qt.AlignCenter)
        h2box.setAlignment(Qt.AlignCenter)

        h3box.addWidget(txt_block)
        h3box.addWidget(encrypt_types_combo)
        h3box.setAlignment(Qt.AlignCenter)

        img_c = Template()
        img_ss1 = Template()
        img_ss2 = Template()

        txt_img = QLabel()
        txt_img.setText("Image to encrypt / decrypted: ")
        txt_img.setAlignment(Qt.AlignCenter)
        txt_img.setStyleSheet('''
        QLabel {
            font-size: 30px;
            font-family: Segoe UI;
        }''')
        txt_img_ss1 = QLabel()
        txt_img_ss1.setText("Secret Share 1: ")
        txt_img_ss1.setAlignment(Qt.AlignCenter)
        txt_img_ss1.setStyleSheet('''
        QLabel {
            font-size: 30px;
            font-family: Segoe UI;
        }''')
        txt_img_ss2 = QLabel()
        txt_img_ss2.setText("Secret Share 2: ")
        txt_img_ss2.setAlignment(Qt.AlignCenter)
        txt_img_ss2.setStyleSheet('''
                QLabel {
                    font-size: 30px;
                    font-family: Segoe UI;
                }''')

        h4box = QHBoxLayout()
        h5box = QHBoxLayout()
        h6box = QHBoxLayout()
        h7box = QHBoxLayout()


        boton_cifrar_pe = crearBoton(cifrado=True)
        boton_descifrar_pe = crearBoton(cifrado=False)
        boton_cifrar_pe.clicked.connect(
            lambda: PixelExpButton(encriptar=True, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c, img_share_1=img_ss1, img_share_2=img_ss2))
        boton_descifrar_pe.clicked.connect(
            lambda: PixelExpButton(encriptar=False, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c, img_share_1=img_ss1, img_share_2=img_ss2))
        boton_limpiar = QPushButton(text="Clean")
        aux_style = """
        QPushButton {
            border-radius:5%;
            padding:5px;
            background:#9E6CFA;
            color:white;
        }
        QPushButton:hover {
            background-color:#4DB4FA;
            }
            """
        boton_limpiar.setStyleSheet(aux_style)
        boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar.setFixedWidth(150)
        boton_limpiar.clicked.connect(lambda: clean(gridBlock, img_c, img_ss1, img_ss2, h4box, h5box, boton_cifrar_pe, boton_descifrar_pe))

        def clean(gridBlock, img_c, img_ss1, img_ss2, h4box, h5box, boton_cifrar_pe, boton_descifrar_pe):
            boton_cifrar_pe.setParent(None)
            boton_descifrar_pe.setParent(None)
            img_c.setParent(None)
            img_ss1.setParent(None)
            img_ss2.setParent(None)
            h4box.setParent(None)
            h5box.setParent(None)
            img_c = Template()
            img_ss1 = Template()
            img_ss2 = Template()
            h4box = QHBoxLayout()
            h5box = QHBoxLayout()
            boton_cifrar_pe = crearBoton(cifrado=True)
            boton_descifrar_pe = crearBoton(cifrado=False)
            boton_cifrar_pe.clicked.connect(
                lambda: PixelExpButton(encriptar=True, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c, img_share_1=img_ss1, img_share_2=img_ss2))
            boton_descifrar_pe.clicked.connect(
                lambda: PixelExpButton(encriptar=False, encrypt_type=str(encrypt_types_combo.currentText()), input=img_c,img_share_1=img_ss1, img_share_2=img_ss2))
            gridBlock.addWidget(img_c, 3, 0, 6, 1)
            gridBlock.addWidget(img_ss1, 3, 1, 6, 1)
            gridBlock.addWidget(img_ss2, 3, 2, 6, 1)
            h4box.addWidget(boton_cifrar_pe)
            h5box.addWidget(boton_descifrar_pe)
            gridBlock.addLayout(h4box, 10, 0, 1, 1)
            gridBlock.addLayout(h5box, 10, 1, 1, 2)


        txt_key2 = QLabel()
        txt_key2.setText('*Note: Clean fields before encrypting/decrypting')
        txt_key2.setStyleSheet('''
                QLabel {
                    font-size: 22px;
                    font-family: Segoe UI;
                }''')

        self.back_button = QPushButton("Back")
        back_buttonStyle = """
        QPushButton {
            width: 230px;
            border-radius: 5%;
            padding: 5px;
            background: #8DD3F6;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #4DB4FA;
            color: white;
        }
        """
        self.back_button.setStyleSheet(back_buttonStyle)
        self.back_button.clicked.connect(lambda: widget.setCurrentIndex(0))




        #gridBlock.addWidget(h3box, 1, 1)
        gridBlock.addLayout(h1box, 0, 0)
        gridBlock.addLayout(h2box, 0, 1, 1, 2)
        h2box.setAlignment(Qt.AlignCenter)
        gridBlock.addLayout(h3box, 1, 0, 1, 3)
        h3box.setAlignment(Qt.AlignCenter)
        gridBlock.addWidget(txt_img, 2, 0)
        gridBlock.addWidget(txt_img_ss1, 2, 1)
        gridBlock.addWidget(txt_img_ss2, 2, 2)
        gridBlock.addWidget(img_c, 3, 0, 6, 1)
        gridBlock.addWidget(img_ss1, 3, 1, 6, 1)
        gridBlock.addWidget(img_ss2, 3, 2, 6, 1)
        h4box.addWidget(boton_cifrar_pe)
        h5box.addWidget(boton_descifrar_pe)
        gridBlock.addLayout(h4box, 10, 0, 1, 1)
        gridBlock.addLayout(h5box, 10, 1, 1, 2)
        h6box.addWidget(self.back_button)
        h7box.addWidget(boton_limpiar)
        h7box.addWidget(txt_key2)
        gridBlock.addLayout(h6box, 11, 0, 1, 1)
        h6box.setAlignment(Qt.AlignCenter)
        gridBlock.addLayout(h7box, 11, 1, 1, 2)
        h7box.setAlignment(Qt.AlignCenter)
        self.setLayout(gridBlock)




# Main execution
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    welcome = WelcomeScreen()
    pixel_expansion = PixelExpansion()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    #widget.addWidget(watermark)
    widget.addWidget(pixel_expansion)
    #widget.setFixedHeight(702)
    #widget.setFixedWidth(1300)
    widget.setStyleSheet("background: #D0E7EB;")
    widget.setWindowTitle("Pixel Safe")
    widget.setCurrentIndex(0)
    widget.show()
    font = QtGui.QFont()
    font.setFamily("Segoe UI SemiLight")
    font.setPointSize(10)
    QApplication.setFont(font)
    sys.exit(app.exec_())

