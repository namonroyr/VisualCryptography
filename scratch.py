import sys
import os
import math
import cv2
import numpy as np
import string
import string
#import image_sdes
import itertools
import random
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
        self.photo.setPixmap(QPixmap(filename))

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
        #self.setFixedSize(1000, 702)

        # Set background image
        self.setStyleSheet("QDialog {background-image: url('resources/app_logo4_mod.png'); background-position: left; "
                           "background-repeat: no-repeat;}")

        # Set up main layout
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignRight)

        # Logo display
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap('resources/app_name.png').scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        self.setLayout(vbox)

    def go_to_watermark(self):
        print("Watermark button clicked")

    def go_to_pixel_expansion(self):
        print("Pixel Expansion button clicked")
        widget.setCurrentIndex(1)

class PixelExpansion(QDialog):

    def __init__(self):
        super(PixelExpansion, self).__init__()
        def ExpandButton(input, encrypt_type):
            # Set sizes
            image_file_name = input.file
            img_name = image_file_name.split('.')[0]
            img_extension = image_file_name.split('.')[1]
            if image_file_name != "":
                img = cv2.imread(image_file_name)
                row, column, depth = img.shape
                # if encriptar == True:
                #
                #
                #     cv2.imwrite(img_cryp_name, imageEncrypted)
                #     QMessageBox.information(None, 'Success',
                #                             'You can find the encrypted image here: ' + img_cryp_name +"\n"+
                #                             'And the key used in the file: '+img_name+"_key"+cryptosys+op_mode+".txt",
                #                             QMessageBox.Ok)
                #     output_ref.open_image(img_cryp_name)

        self.setFixedSize(1200, 702)
        gridBlock = QGridLayout()
        gridBlock.setGeometry(QtCore.QRect(10, 10, 1200, 702))
        h1box = QVBoxLayout()
        h2box = QVBoxLayout()
        txt_block = QLabel()
        txt_block.setText("Select Block Cipher: ")
        label_style = '''
        QLabel {
            font-size: 18px;
            font-family: Segoe UI;
        }'''
        txt_block.setStyleSheet(label_style)
        txt_block1 = QLabel()
        txt_block1.setText("Select Operation Mode: ")
        txt_block1.setStyleSheet(label_style)
        cripto_img = ["DES", "S-DES", "3-DES","AES"]
        op_modes = ["ECB","CBC","OFB","CTR"]
        combo_img = QComboBox()
        combo_modes = QComboBox()
        comboblock_style = """
        QComboBox {
            padding:5px;
            border:1px solid #161616;
            border-radius:3%;
            font-size: 18px;
            background-color:#8DD3F6;
        }
        QComboBox::drop-down
        {
            border: 0px;
            width:20px;
        }
        QComboBox::down-arrow {
            image: url(resources/dropdown.png);
            width: 12px;
            height: 12px;
        }
        QComboBox::drop-down:hover {
           background-color:#E3E3E3;
        }
        """
        combo_img.setStyleSheet(comboblock_style)
        combo_modes.setStyleSheet(comboblock_style)
        combo_img.addItems(cripto_img)
        combo_modes.addItems(op_modes)
        h1box.addWidget(txt_block)
        h1box.addWidget(combo_img)
        h2box.addWidget(txt_block1)
        h2box.addWidget(combo_modes)
        img_c = Template()
        img_d = Template()
        txt_img = QLabel()
        txt_img.setText("Image to encrypt / decrypted: ")
        txt_img.setAlignment(Qt.AlignCenter)
        txt_img.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
        txt_img_d = QLabel()
        txt_img_d.setText("Image to decrypt / encrypted: ")
        txt_img_d.setAlignment(Qt.AlignCenter)
        txt_img_d.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
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
            font: bold;
            }
            """
        boton_limpiar.setStyleSheet(aux_style)
        boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar.setFixedWidth(150)
        boton_limpiar.clicked.connect(lambda: clean(gridBlock, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill))

        def clean(layout, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill):
            txt_key.setText('')
            boton_cifrar_hill.setParent(None)
            boton_descifrar_hill.setParent(None)
            img_c.setParent(None)
            img_d.setParent(None)
            img_c = Template()
            img_d = Template()
            boton_cifrar_hill = crearBoton(cifrado=True)
            boton_descifrar_hill = crearBoton(cifrado=False)
            boton_cifrar_hill.clicked.connect(lambda: BlockButton(img_c, img_d, True, str(combo_img.currentText()), str(combo_modes.currentText())))
            boton_descifrar_hill.clicked.connect(lambda: BlockButton(img_d, img_c, False, str(combo_img.currentText()), str(combo_modes.currentText())))
            gridBlock.addWidget(img_c, 2, 0, 6, 1)
            gridBlock.addWidget(img_d, 2, 2, 6, 1)
            gridBlock.addWidget(boton_cifrar_hill, 3, 1)
            gridBlock.addWidget(boton_descifrar_hill, 4, 1)

        boton_browsekey = QPushButton(text="Key")
        boton_browsekey.setStyleSheet(aux_style)
        boton_browsekey.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_browsekey.setFixedWidth(150)
        boton_browsekey.clicked.connect(lambda: browse_key())


        def browse_key():
            fname = QFileDialog.getOpenFileName(None, 'Select key file', QtCore.QDir.rootPath())
            txt_key.setText(fname[0])


        txt_key = QLabel()
        txt_key.setStyleSheet('''
        QLabel {
            border:1px solid #161616;
        }''')
        boton_key = QPushButton(text="Key")
        boton_key.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_key.setFixedWidth(150)
        boton_key.clicked.connect(lambda: info())
        def info():
            QMessageBox.information(None, 'Info',
                                    'The encryption key is automatically generated and saved in a .png file',
                                    QMessageBox.Ok)

        txt_key2 = QLabel()
        txt_key2.setText('*Note: Clean fields before \n encrypting/decrypting')

        self.back_button = QPushButton("Back to Main Menu")
        back_buttonStyle = """
        QPushButton {
            width: 170px;
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

        gridBlock.addLayout(h1box, 0, 0)
        gridBlock.addLayout(h2box, 0, 1)
        gridBlock.addWidget(combo_img, 0, 1)
        gridBlock.addWidget(txt_img, 1, 0)
        gridBlock.addWidget(txt_img_d, 1, 2)
        gridBlock.addWidget(img_c, 2, 0, 6, 1)
        gridBlock.addWidget(img_d, 2, 2, 6, 1)
        gridBlock.addWidget(boton_limpiar, 6, 1)
        gridBlock.addWidget(boton_key, 9, 0)
        gridBlock.addWidget(txt_key2, 10, 0)
        gridBlock.addWidget(boton_browsekey, 9, 2)
        gridBlock.addWidget(txt_key, 10, 2)
        gridBlock.addWidget(self.back_button, 11, 1)
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

