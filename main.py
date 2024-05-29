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
from itertools import cycle
#from pyqtgraph import PlotWidget, plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
#import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (Qt, QFile, QDate, QTime, QSize, QTimer, QRect, QRegExp, QTranslator,
                          QLocale, QLibraryInfo, QSize)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDialog, QTableWidget, QMenu,
                             QTableWidgetItem, QAbstractItemView, QLineEdit, QTabWidget,
                             QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox, QStackedLayout,
                             QDateEdit, QComboBox, QPushButton, QFileDialog, QPlainTextEdit, QLineEdit,
                             QTextEdit, QSpinBox)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,
                         QRegExpValidator, QImage, QCursor)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
        vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox1.setAlignment(Qt.AlignCenter)
        self.hbox2.setAlignment(Qt.AlignCenter)
        vbox.setAlignment(Qt.AlignCenter)
        self.image = QLabel()
        self.image.setPixmap(QPixmap(resource_path('resources/pixel_safe_logo.png')))
        buttonStyle = """
        QPushButton {
            width: 170px;
            border-radius: 5%;
            padding: 5px;
            background: #52F6E0;
            color: #283433;
            font: 14pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #4DB4FA;
            color: white;
        }
        """
        self.watermark_button = QPushButton("Watermark")
        self.pixel_expansion_button = QPushButton("Pixel Expansion")
        self.watermark_button.setStyleSheet(buttonStyle)
        self.pixel_expansion_button.setStyleSheet(buttonStyle)

        self.clasicos_button.clicked.connect(self.gotowatermark)
        self.bloque_button.clicked.connect(self.gotopixelexpansion)

        self.hbox1.addWidget(self.image)
        self.hbox2.addWidget(self.watermark_button)
        self.hbox2.addWidget(self.pixel_expansion_button)
        vbox.addLayout(self.hbox1)
        vbox.addLayout(self.hbox2)
        self.setLayout(vbox)
        #self.show()

    def gotowatermark(self):


    def gotopixelexpansion(self):
        widget.setCurrentIndex(2)

class ClasicosScreen(QDialog):

    def __init__(self):
        super(ClasicosScreen, self).__init__()
        # Tab
        vbox1 = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.setAlignment(Qt.AlignRight)
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
        tabWidget = QtWidgets.QTabWidget(self)
        vbox1.addWidget(tabWidget)
        hbox1.addWidget(self.back_button)
        vbox1.addLayout(hbox1)
        self.setLayout(vbox1)
        tabWidget.setGeometry(QtCore.QRect(10, 20, 1150, 700))
        tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        tabWidget.setObjectName("tabWidget")
        tabWidget.setStyleSheet("""
        QTabWidget::tab-bar {
            left: 1px; /* move to the right by 5px */
        }
        QTabWidget::pane {
            top:-1px;
            background-color: #FFFFFF;
        }
        QTabBar::tab {
            background: #52F6E0;
            font-size: 15px;
            min-width: 200px;
            min-height: 30px;
            padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #13A5EE;
            color: white;
            font: bold;
        }
        QTabBar::tab:!selected {
            margin-top: 3px;
        }""")
        cifrado = QtWidgets.QWidget()
        tabWidget.addTab(cifrado, "Encryption/Decryption")
        gridcifrado = QGridLayout(cifrado)
        gridcifrado.setGeometry(QtCore.QRect(10, 10, 1030, 600))
        # Menu de criptosistemas
        menu = QComboBox(self)
        menu.setStyleSheet(
            """
            QComboBox {
                padding:5px;
                border:1px solid #161616;
                border-radius:3%;
                background-color:#8DD3F6;
                }
            QComboBox::drop-down {
                border:0px;
                width:20px;
                }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                }
            QComboBox::drop-down:hover {
                background-color: #D7DDE1;
                }
            """)
        self.txt_crypto = QLabel()
        self.txt_crypto.setText("Select a Cryptosystem:")
        criptosistemas = ["Affine cipher", "Shift cipher",
                          "Permutation cipher", "Substitution cipher",
                          "Vigenère cipher"]
        """
        Buttons ----------------------------------------------------------
        """

        def botonAfin(clave, input, output, encriptar):
            texto_cifrado = input.toPlainText().strip()
            criptosistema_afin = cc.CriptosistemaAfin(clave)
            if encriptar == True:
                output.setPlainText(criptosistema_afin.encriptar(texto_cifrado))
            elif encriptar == False:
                output.setPlainText(criptosistema_afin.desencriptar(texto_cifrado))

        def botonDesplazamiento(clave, input, output, encriptar):
            texto_cifrado = input.toPlainText().strip()
            criptosistema_desplazamiento = cc.CriptosistemaDesplazamiento(clave)
            if encriptar == True:
                output.setPlainText(criptosistema_desplazamiento.encriptar(texto_cifrado))
            elif encriptar == False:
                output.setPlainText(criptosistema_desplazamiento.desencriptar(texto_cifrado))

        def botonPermutacion(clave, input, output, encriptar):
            texto_cifrado = input.toPlainText().strip()
            criptosistema_permutacion = cc.CriptosistemaPermutacion(clave)
            if encriptar == True:
                output.setPlainText(criptosistema_permutacion.encriptar(texto_cifrado))
            elif encriptar == False:
                output.setPlainText(criptosistema_permutacion.desencriptar(texto_cifrado))

        def botonVigenere(clave, input, output, encriptar):
            texto_cifrado = input.toPlainText().strip()
            if encriptar:
                output.setPlainText(vg.encriptar(texto_cifrado, clave))
            else:
                output.setPlainText(vg.decriptar(texto_cifrado, clave))

        def botonSustitucion(clave, input, output, encriptar):
            clave = ''.join([i for i in clave if i != ' ']).lower().split(',')
            clave = {i.split(':')[0]: i.split(':')[1] for i in clave}
            texto_cifrado = input.toPlainText().strip()
            sus = sb.substitution(texto_cifrado)
            if encriptar:
                sus.permutar(clave)
                if len(set(k for j,k in sus.key.items())) < 26:
                    output.setPlainText("Invalid Permutation. Undefined keys are replaced by themselves. That said: make sure this map is injective")
                else:
                    output.setPlainText(sus.permutado.upper())
            else:
                sus.permutar({v: k for k, v in clave.items()})
                if len(set(k for j,k in sus.key.items())) < 26:
                    output.setPlainText("Invalid Permutation. Undefined keys are replaced by themselves. That said: make sure this map is injective")
                else:
                    output.setPlainText(sus.permutado.upper())

        self.txt_clave = QLabel()
        self.txt_clave.setText("Enter the two key digits of affine cipher separated by a space: ")
        self.res_clave = QLineEdit()
        self.res_clave.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        # Texto a cifrar
        self.txt_aCifrar = QLabel(text="Plain Text:")
        self.input_aCifrar = QPlainTextEdit()
        self.input_aCifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        # Texto cifrado
        self.txt_cifrado = QLabel(text="Cipher Text:")
        self.output_cifrado = QPlainTextEdit()
        self.output_cifrado.setDisabled(True)
        self.output_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")

        # Button
        self.boton_cifrar = crearBoton(cifrado=True)
        self.boton_cifrar.clicked.connect(lambda: botonAfin(self.res_clave.text().split(), self.input_aCifrar, self.output_cifrado, True))

        # Texto a descifrar
        self.txt_aDescifrar = QLabel(text="Cipher Text:")
        self.input_aDescifrar = QPlainTextEdit()
        self.input_aDescifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        # Texto descifrado
        self.txt_descifrado = QLabel(text="Plain Text:")
        self.output_descifrado = QPlainTextEdit()
        self.output_descifrado.setDisabled(True)
        self.output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        # Button
        self.boton_descifrar = crearBoton(cifrado=False)
        self.boton_descifrar.clicked.connect(lambda: botonAfin(self.res_clave.text().split(), self.input_aDescifrar, self.output_descifrado, False))

        def limpiarCampos():
            self.res_clave.setText("")
            for i in [self.input_aCifrar, self.input_aDescifrar, self.output_cifrado, self.output_descifrado]:
                i.setPlainText("")

        def escogerCriptosistema():
            if str(menu.currentText()) == "Affine cipher":
                # Clave afin
                self.txt_clave.setText("Enter the two key digits of affine cipher separated by a space: ")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonAfin(self.res_clave.text().split(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonAfin(self.res_clave.text().split(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)

            elif str(menu.currentText()) == "Shift cipher":
                # Clave por desplazamiento
                self.txt_clave.setText("Enter the digit key for shift cipher:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonDesplazamiento(self.res_clave.text(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonDesplazamiento(self.res_clave.text(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)

            elif str(menu.currentText()) == "Permutation cipher":
                self.txt_clave.setText("Enter the permutation digits of the matirx followed by space:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(
                    lambda: botonPermutacion([len(self.res_clave.text().split()), self.res_clave.text()], self.input_aCifrar, self.output_cifrado,
                                             True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonPermutacion([len(self.res_clave.text().split()), self.res_clave.text()], self.input_aDescifrar,
                                             self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)
            elif str(menu.currentText()) == "Vigenère cipher":
                self.txt_clave.setText("Enter the word key:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonVigenere(self.res_clave.text(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonVigenere(self.res_clave.text(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)
            elif str(menu.currentText()) == "Substitution cipher":
                self.txt_clave.setText(
                    "Enter the substitution rule (letter followed by \":\" and the substitution letter) separated by a comma:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonSustitucion(self.res_clave.text(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonSustitucion(self.res_clave.text(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)

        menu.addItems(criptosistemas)
        menu.currentTextChanged.connect(escogerCriptosistema)
        menu.setCurrentIndex(0)

        gridcifrado.addWidget(self.txt_crypto, 0, 0)
        gridcifrado.addWidget(menu, 1, 0)
        gridcifrado.addWidget(self.txt_clave, 2, 0)
        gridcifrado.addWidget(self.res_clave, 3, 0)
        gridcifrado.addWidget(self.txt_aCifrar, 4, 0)
        gridcifrado.addWidget(self.input_aCifrar, 5, 0)
        gridcifrado.addWidget(self.txt_cifrado, 6, 0)
        gridcifrado.addWidget(self.output_cifrado, 7, 0)
        gridcifrado.addWidget(self.boton_cifrar, 8, 0)
        gridcifrado.addWidget(self.txt_aDescifrar, 4, 1)
        gridcifrado.addWidget(self.input_aDescifrar, 5, 1)
        gridcifrado.addWidget(self.txt_descifrado, 6, 1)
        gridcifrado.addWidget(self.output_descifrado, 7, 1)
        gridcifrado.addWidget(self.boton_descifrar, 8, 1)

        """
        ****************-----------------Hill Tab-----------------------*********************
        """
        def botonHill(input, output_ref, encriptar):
            image_file_name = input.file
            img_name = image_file_name.split('.')[0]
            img_extension = image_file_name.split('.')[1]
            file_ext = ['jpg', 'png', 'jpeg']
            if image_file_name != "" and img_extension in file_ext:
                img = cv2.imread(image_file_name)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if encriptar == True:
                    criptosistema_Hill = hill.Hill(img_rgb, img_name)
                    encoded_img_name = criptosistema_Hill.encriptar(img_name)
                    QMessageBox.information(None, 'Sucess',
                                            'Encryption done, you can find the image here: ' + encoded_img_name + '\n' + 'La clave con la que se encriptó se encuentra en: ' + image_file_name + '_key.png',
                                            QMessageBox.Ok)
                    output_ref.open_image(encoded_img_name)
                elif encriptar == False and txt_key.text() != '':
                    key = txt_key.text()
                    img_dec_vec = hill.desencriptar(img_rgb, key)
                    decoded_img_name = '{0}-descifrada.{1}'.format(img_name, img_extension)
                    img_dec_gbr = cv2.cvtColor(img_dec_vec.astype(np.uint8), cv2.COLOR_RGB2BGR)
                    cv2.imwrite(decoded_img_name, img_dec_gbr)
                    QMessageBox.information(None, 'Success',
                                            'Decryption done, you can find the image here: ' + decoded_img_name,
                                            QMessageBox.Ok)
                    output_ref.open_image(decoded_img_name)
                else:
                    QMessageBox.critical(None, 'Missing Key',
                                         'Select the (.png) file with the key for decryption',
                                         QMessageBox.Ok)
            else:
                QMessageBox.critical(None, 'Error',
                                     'Drop and image to process or enter one with a valid format (.jpg, .png)',
                                     QMessageBox.Ok)

        Hill = QtWidgets.QWidget()
        tabWidget.addTab(Hill, "Hill - Image")
        gridHill = QGridLayout(Hill)
        gridHill.setGeometry(QtCore.QRect(10, 10, 1030, 600))
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
        txt_img_d.setText("Imagen to decrypt / encrypted: ")
        txt_img_d.setAlignment(Qt.AlignCenter)
        txt_img_d.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
        boton_cifrar_hill = crearBoton(cifrado=True)
        boton_descifrar_hill = crearBoton(cifrado=False)
        boton_cifrar_hill.clicked.connect(lambda: botonHill(img_c, img_d, True))
        boton_descifrar_hill.clicked.connect(lambda: botonHill(img_d, img_c, False))
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
        boton_limpiar.clicked.connect(lambda: clean(gridHill, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill))

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
            boton_cifrar_hill.clicked.connect(lambda: botonHill(img_c, img_d, True))
            boton_descifrar_hill.clicked.connect(lambda: botonHill(img_d, img_c, False))
            gridHill.addWidget(img_c, 1, 0, 4, 1)
            gridHill.addWidget(img_d, 1, 2, 4, 1)
            gridHill.addWidget(boton_cifrar_hill, 2, 1)
            gridHill.addWidget(boton_descifrar_hill, 3, 1)

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
        gridHill.addWidget(img_c, 1, 0, 6, 1)
        gridHill.addWidget(img_d, 1, 2, 6, 1)
        gridHill.addWidget(txt_img, 0, 0)
        gridHill.addWidget(txt_img_d, 0, 2)
        gridHill.addWidget(boton_cifrar_hill, 2, 1)
        gridHill.addWidget(boton_descifrar_hill, 3, 1)
        gridHill.addWidget(boton_limpiar, 5, 1)
        gridHill.addWidget(boton_key, 8, 0)
        gridHill.addWidget(txt_key2, 9, 0)
        gridHill.addWidget(boton_browsekey, 8, 2)
        gridHill.addWidget(txt_key, 9, 2)


        """
        ****************-----------------criptanalysis Tab-----------------------*********************
        """

        criptoitems = ["Affine cipher", "Shift cipher",
                          "Hill/Permutation cipher", "Substitution cipher",
                          "Vigenère cipher"]

        def vigenereAnalisis(input_criptoanalysis, output_descifrado):
            texto = input_criptoanalysis.toPlainText().strip()
            res = list(vg.vigenereAttack(texto))
            if len(res) == 0:
                output_descifrado.setPlainText("No se encontró ninguna palabra clave.")
            else:
                retorno = ''
                for j, k in res:
                    retorno = retorno + 'La clave podría ser ' + j.upper() + '. De ser ese el caso el texto descifrado es:\n' + k + '\n'
                output_descifrado.setPlainText(retorno)


        def desplazamientoAnalisis(input_criptoanalysis, output_descifrado):
            texto = input_criptoanalysis.toPlainText().strip()
            texto = texto.upper()
            texto = [i for i in texto if i in string.ascii_uppercase]
            output = ""
            for i in range(1, 26):
                lista = [(abc[k] + i) % 26 for k in texto]
                lista = [string.ascii_uppercase[k] for k in lista]
                output = output + "Con desplazamiento {}: \n".format(i) + ''.join(lista) + "\n"
            output_descifrado.setPlainText(output)


        def afinAnalisis(input_criptoanalysis, output_descifrado):
            texto = input_criptoanalysis.toPlainText().strip().upper()
            texto = [i for i in texto if i in string.ascii_uppercase]
            output = ""
            for i in range(1, 26):
                if math.gcd(i, 26) > 1:
                    continue
                inverse_m = [k for k in range(1, 26) if (i * k) % 26 == 1][0]
                for j in range(1, 26):
                    if math.gcd(i, j) > 1:
                        continue
                    inverse_s = 26 - j
                    if (i, j) == (3, 5):
                        output = output + "Para a = {} y b = {} el texto es:\n".format(i, j) + ''.join(
                        [string.ascii_uppercase[(inverse_m * (abc[k] + inverse_s)) % 26] for k in texto]) + '\n'
            output_descifrado.setPlainText(output)


        # ------menu---------------
        menu_cripto = QComboBox()
        menu_cripto.setStyleSheet(
            """
            QComboBox {
                padding:5px;
                border:1px solid #161616;
                border-radius:3%;
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
            """)
        menu_cripto.addItems(criptoitems)

        menu_cripto.setCurrentIndex(0)
        tabWidget.setCurrentIndex(0)
        criptanalysis = QWidget()
        tabWidget.addTab(criptanalysis, "Cryptanalysis")
        gridCripto = QVBoxLayout()
        criptanalysis.setLayout(gridCripto)
        gridCripto.setGeometry(QtCore.QRect(10, 10, 1030, 600))
        stackedLayout = QStackedLayout()
        # Afin**************************
        afin_ca = QWidget()
        afinLayout = QGridLayout()
        input_label = QLabel()
        input_label.setText("Cipher Text")
        input_criptoanalysisafin = QPlainTextEdit()
        input_criptoanalysisafin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        decript_label = QLabel()
        decript_label.setText("Key / Plain Text")
        output_descifradoafin = QPlainTextEdit()
        output_descifradoafin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifradoafin.setReadOnly(True)
        boton_submitafin = QPushButton(text="Submit")
        submit_style = """
        QPushButton {
            width: 70px;
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
        """
        boton_submitafin.setStyleSheet(submit_style)
        afinLayout.addWidget(input_label, 0, 1)
        afinLayout.addWidget(decript_label, 0, 2)
        afinLayout.addWidget(input_criptoanalysisafin, 1, 1)
        afinLayout.addWidget(output_descifradoafin, 1, 2)
        afinLayout.addWidget(boton_submitafin, 2, 1)
        afin_ca.setLayout(afinLayout)
        stackedLayout.addWidget(afin_ca)
        boton_submitafin.clicked.connect(lambda: afinAnalisis(input_criptoanalysisafin, output_descifradoafin))
        # Desplazamiento*********************************
        des_ca = QWidget()
        desLayout = QGridLayout()
        input_label = QLabel()
        input_label.setText("Cipher Text")
        input_criptoanalysisDesplazamiento = QPlainTextEdit()
        input_criptoanalysisDesplazamiento.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        decript_label = QLabel()
        decript_label.setText("Key / Plain Text")
        output_descifradoDesplazamiento = QPlainTextEdit()
        output_descifradoDesplazamiento.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifradoDesplazamiento.setReadOnly(True)
        boton_submitDesplazamiento = QPushButton(text="Submit")
        boton_submitDesplazamiento.setStyleSheet(submit_style)
        desLayout.addWidget(input_label, 0, 1)
        desLayout.addWidget(decript_label, 0, 2)
        desLayout.addWidget(input_criptoanalysisDesplazamiento, 1, 1)
        desLayout.addWidget(output_descifradoDesplazamiento, 1, 2)
        desLayout.addWidget(boton_submitDesplazamiento, 2, 1)
        des_ca.setLayout(desLayout)
        stackedLayout.addWidget(des_ca)
        boton_submitDesplazamiento.clicked.connect(
            lambda: desplazamientoAnalisis(input_criptoanalysisDesplazamiento, output_descifradoDesplazamiento))
        # Hill**************************
        hill_ca = QWidget()
        hillLayout = QGridLayout()
        txt_plano = QLabel()
        txt_plano.setText("Plain Text: ")
        input_plano = QPlainTextEdit()
        input_plano.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        txt_cifrado = QLabel()
        txt_cifrado.setText("Cipher Text: ")
        input_cifrado = QPlainTextEdit()
        input_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        boton_getkey = QPushButton(text="Get Key")
        boton_getkey.setStyleSheet(submit_style)
        boton_getkey.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_getkey.setFixedWidth(170)
        boton_getkey.clicked.connect(lambda: criptanalisisHill(input_plano, input_cifrado))

        boton_limpiar_caHill = QPushButton(text="Clean")
        boton_limpiar_caHill.setStyleSheet(aux_style)
        boton_limpiar_caHill.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar_caHill.setFixedWidth(170)


        def limpiarCampos_caHill():
            res_clave.setText("")
            for i in [input_plano, input_cifrado, output_m, output_keyfound]:
                i.setPlainText("")


        boton_limpiar_caHill.clicked.connect(limpiarCampos_caHill)
        txt_m = QLabel()
        txt_m.setText("m value: ")
        output_m = QPlainTextEdit()
        output_m.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_m.setReadOnly(True)
        txt_keyfound = QLabel()
        txt_keyfound.setText("Key: ")
        output_keyfound = QPlainTextEdit()
        output_keyfound.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_keyfound.setReadOnly(True)
        hillLayout.addWidget(txt_plano, 0, 0)
        hillLayout.addWidget(input_plano, 1, 0)
        hillLayout.addWidget(txt_cifrado, 2, 0)
        hillLayout.addWidget(input_cifrado, 3, 0)
        hillLayout.addWidget(boton_getkey, 0, 1, -1, 1)
        hillLayout.addWidget(boton_limpiar_caHill, 2, 1, -1, 1)
        hillLayout.addWidget(txt_m, 0, 2)
        hillLayout.addWidget(output_m, 1, 2)
        hillLayout.addWidget(txt_keyfound, 2, 2)
        hillLayout.addWidget(output_keyfound, 3, 2)
        hill_ca.setLayout(hillLayout)
        stackedLayout.addWidget(hill_ca)
        # Add the combo box and the stacked layout to the top-level layout
        gridCripto.addWidget(menu_cripto)
        gridCripto.addLayout(stackedLayout)

        def switchPage():
            stackedLayout.setCurrentIndex(menu_cripto.currentIndex())
        menu_cripto.currentTextChanged.connect(switchPage)

        # Sustitución*********************************
        alphabet_string = string.ascii_uppercase
        alpha = list(alphabet_string)
        alphabet_list = [1]
        alphabet_list[0] = '-'
        alphabet_list.extend(alpha)

        sustitucion_ca = QWidget()
        sus_layout = QHBoxLayout()
        crifrado_sus_label = QLabel()
        crifrado_sus_label.setText("Cipher Text:")
        crifrado_sus = QPlainTextEdit()
        crifrado_sus.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        boton_analizarsus = QPushButton(text="Analizar")
        boton_analizarsus.setFixedWidth(150)
        boton_analizarsus.clicked.connect(lambda: criptanalisisSus(crifrado_sus))
        boton_analizarsus.setStyleSheet(submit_style)
        decript_label = QLabel()
        decript_label.setText("Plain Text\n with selected substitutions:")
        output_descifrado_sus = QPlainTextEdit()
        output_descifrado_sus.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifrado_sus.setReadOnly(True)
        # letters
        a_label = QLabel()
        a_label.setText("A")
        b_label = QLabel()
        b_label.setText("B")
        c_label = QLabel()
        c_label.setText("C")
        d_label = QLabel()
        d_label.setText("D")
        e_label = QLabel()
        e_label.setText("E")
        f_label = QLabel()
        f_label.setText("F")
        g_label = QLabel()
        g_label.setText("G")
        h_label = QLabel()
        h_label.setText("H")
        i_label = QLabel()
        i_label.setText("I")
        j_label = QLabel()
        j_label.setText("J")
        k_label = QLabel()
        k_label.setText("K")
        l_label = QLabel()
        l_label.setText("L")
        m_label = QLabel()
        m_label.setText("M")
        n_label = QLabel()
        n_label.setText("N")
        o_label = QLabel()
        o_label.setText("O")
        p_label = QLabel()
        p_label.setText("P")
        q_label = QLabel()
        q_label.setText("Q")
        r_label = QLabel()
        r_label.setText("R")
        s_label = QLabel()
        s_label.setText("S")
        t_label = QLabel()
        t_label.setText("T")
        u_label = QLabel()
        u_label.setText("U")
        v_label = QLabel()
        v_label.setText("V")
        w_label = QLabel()
        w_label.setText("W")
        x_label = QLabel()
        x_label.setText("X")
        y_label = QLabel()
        y_label.setText("Y")
        z_label = QLabel()
        z_label.setText("Z")
        a_label.setAlignment(QtCore.Qt.AlignCenter)
        b_label.setAlignment(QtCore.Qt.AlignCenter)
        c_label.setAlignment(QtCore.Qt.AlignCenter)
        d_label.setAlignment(QtCore.Qt.AlignCenter)
        e_label.setAlignment(QtCore.Qt.AlignCenter)
        f_label.setAlignment(QtCore.Qt.AlignCenter)
        g_label.setAlignment(QtCore.Qt.AlignCenter)
        h_label.setAlignment(QtCore.Qt.AlignCenter)
        i_label.setAlignment(QtCore.Qt.AlignCenter)
        j_label.setAlignment(QtCore.Qt.AlignCenter)
        k_label.setAlignment(QtCore.Qt.AlignCenter)
        l_label.setAlignment(QtCore.Qt.AlignCenter)
        m_label.setAlignment(QtCore.Qt.AlignCenter)
        n_label.setAlignment(QtCore.Qt.AlignCenter)
        o_label.setAlignment(QtCore.Qt.AlignCenter)
        p_label.setAlignment(QtCore.Qt.AlignCenter)
        q_label.setAlignment(QtCore.Qt.AlignCenter)
        r_label.setAlignment(QtCore.Qt.AlignCenter)
        s_label.setAlignment(QtCore.Qt.AlignCenter)
        t_label.setAlignment(QtCore.Qt.AlignCenter)
        u_label.setAlignment(QtCore.Qt.AlignCenter)
        v_label.setAlignment(QtCore.Qt.AlignCenter)
        w_label.setAlignment(QtCore.Qt.AlignCenter)
        x_label.setAlignment(QtCore.Qt.AlignCenter)
        y_label.setAlignment(QtCore.Qt.AlignCenter)
        z_label.setAlignment(QtCore.Qt.AlignCenter)

        sus_a = QComboBox()
        sus_a.addItems(alphabet_list)
        sus_b = QComboBox()
        sus_b.addItems(alphabet_list)
        sus_c = QComboBox()
        sus_c.addItems(alphabet_list)
        sus_d = QComboBox()
        sus_d.addItems(alphabet_list)
        sus_e = QComboBox()
        sus_e.addItems(alphabet_list)
        sus_f = QComboBox()
        sus_f.addItems(alphabet_list)
        sus_g = QComboBox()
        sus_g.addItems(alphabet_list)
        sus_h = QComboBox()
        sus_h.addItems(alphabet_list)
        sus_i = QComboBox()
        sus_i.addItems(alphabet_list)
        sus_j = QComboBox()
        sus_j.addItems(alphabet_list)
        sus_k = QComboBox()
        sus_k.addItems(alphabet_list)
        sus_l = QComboBox()
        sus_l.addItems(alphabet_list)
        sus_m = QComboBox()
        sus_m.addItems(alphabet_list)
        sus_n = QComboBox()
        sus_n.addItems(alphabet_list)
        sus_o = QComboBox()
        sus_o.addItems(alphabet_list)
        sus_p = QComboBox()
        sus_p.addItems(alphabet_list)
        sus_q = QComboBox()
        sus_q.addItems(alphabet_list)
        sus_r = QComboBox()
        sus_r.addItems(alphabet_list)
        sus_s = QComboBox()
        sus_s.addItems(alphabet_list)
        sus_t = QComboBox()
        sus_t.addItems(alphabet_list)
        sus_u = QComboBox()
        sus_u.addItems(alphabet_list)
        sus_v = QComboBox()
        sus_v.addItems(alphabet_list)
        sus_w = QComboBox()
        sus_w.addItems(alphabet_list)
        sus_x = QComboBox()
        sus_x.addItems(alphabet_list)
        sus_y = QComboBox()
        sus_y.addItems(alphabet_list)
        sus_z = QComboBox()
        sus_z.addItems(alphabet_list)
        boton_applysus = QPushButton(text="Apply")
        boton_applysus.clicked.connect(lambda: aplicar(lista_caracteres, crifrado_sus, output_descifrado_sus))
        boton_applysus.setFixedWidth(100)
        boton_applysus.setStyleSheet(submit_style)

        monfreq_eng = QLabel()
        monfreq_eng.setText('Probability of occurrence \nde english letters')
        monoeng_table = QTableWidget()
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(8)
        monoeng_table.setFont(font)
        monoeng_table.setColumnCount(4)
        monoeng_table.setRowCount(13)
        monoeng_table.resizeRowsToContents()
        monoeng_table.setHorizontalHeaderLabels(["Letter", "Proba.", "Letter", "Proba."])
        monoeng_table.resizeRowsToContents()
        monoeng_table.resizeColumnsToContents()
        monoeng_table.verticalHeader().hide()
        header = monoeng_table.horizontalHeader()

        for row in range(1,14):
            item = alphabet_list[row]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            monoeng_table.setItem(row-1, 0, cell)

        for row in range(13):
            item = alphabet_list[row + 14]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            monoeng_table.setItem(row-1, 2, cell)

        letters_prob = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070,
                        0.002, 0.008, 0.040, 0.240, 0.067, 0.075, 0.019, 0.001, 0.060,
                        0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001]

        for row in range(13):
            item = str(letters_prob[row])
            cell = QTableWidgetItem(item)
            cell.setTextAlignment(Qt.AlignRight)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            monoeng_table.setItem(row, 1, cell)

        for row in range(13):
            item = str(letters_prob[row + 13])
            cell = QTableWidgetItem(item)
            cell.setTextAlignment(Qt.AlignRight)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            monoeng_table.setItem(row, 3, cell)

        digrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST',
                   'EN', 'AT', 'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS',
                   'OR', 'TI', 'IS', 'ET', 'IT', 'AR', 'TE', 'SE', 'HI', 'OF']

        difreq_eng = QLabel()
        difreq_eng.setText('Most frequent digrams \nin English')
        digeng_table = QTableWidget()
        digeng_table.setFont(font)
        digeng_table.setColumnCount(5)
        digeng_table.setRowCount(6)
        digeng_table.resizeRowsToContents()
        digeng_table.resizeColumnsToContents()
        digeng_table.verticalHeader().hide()
        digeng_table.horizontalHeader().hide()

        for row in range(6):
            item = digrams[row]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            digeng_table.setItem(row, 0, cell)
        for row in range(6):
            item = digrams[row + 6]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            digeng_table.setItem(row, 1, cell)
        for row in range(6):
            item = digrams[row + 12]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            digeng_table.setItem(row, 2, cell)
        for row in range(6):
            item = digrams[row + 18]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            digeng_table.setItem(row, 3, cell)
        for row in range(6):
            item = digrams[row + 24]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            digeng_table.setItem(row, 4, cell)

        trigrams = ['THE', 'ING', 'AND', 'HER', 'ERE', 'ENT', 'THA', 'NTH', 'WAS', 'ETH', 'FOR', 'DTH']

        trifreq_eng = QLabel()
        trifreq_eng.setText('Most frequent trigrams \nin English')
        trigeng_table = QTableWidget()
        trigeng_table.setFont(font)
        trigeng_table.setColumnCount(5)
        trigeng_table.setRowCount(2)
        trigeng_table.resizeRowsToContents()
        trigeng_table.resizeColumnsToContents()
        trigeng_table.verticalHeader().hide()
        trigeng_table.horizontalHeader().hide()

        for row in range(2):
            item = trigrams[row]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            trigeng_table.setItem(row, 0, cell)
        for row in range(2):
            item = trigrams[row + 2]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            trigeng_table.setItem(row, 1, cell)
        for row in range(2):
            item = trigrams[row + 4]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            trigeng_table.setItem(row, 2, cell)
        for row in range(2):
            item = trigrams[row + 6]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            trigeng_table.setItem(row, 3, cell)
        for row in range(2):
            item = trigrams[row + 8]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            trigeng_table.setItem(row, 4, cell)

        monfreq_txt = QLabel()
        monfreq_txt.setText('Monograms frequency \nin the text')
        monofreq_out = QTableWidget()
        difreq_txt = QLabel()
        difreq_txt.setText('Digrams frequency \nin the text')
        difreq_out = QTableWidget()
        trifreq_txt = QLabel()
        trifreq_txt.setText('Trigrams frequency \nin the text')
        trifreq_out = QTableWidget()

        sus1_ly = QVBoxLayout()
        sus1_ly.addWidget(crifrado_sus_label)
        sus1_ly.addWidget(crifrado_sus)
        sus1_ly.addWidget(boton_analizarsus)
        sus1_ly.addWidget(decript_label)
        sus1_ly.addWidget(output_descifrado_sus)

        sus2_ly = QGridLayout()
        sus2_ly.addWidget(monfreq_eng, 0, 0)
        sus2_ly.addWidget(monoeng_table, 1, 0)
        sus2_ly.addWidget(difreq_eng, 2, 0)
        sus2_ly.addWidget(digeng_table, 3, 0)
        sus2_ly.addWidget(trifreq_eng, 4, 0)
        sus2_ly.addWidget(trigeng_table, 5, 0)
        sus2_ly.addWidget(monfreq_txt, 0, 1)
        sus2_ly.addWidget(monofreq_out, 1, 1)
        sus2_ly.addWidget(difreq_txt, 2, 1)
        sus2_ly.addWidget(difreq_out, 3, 1)
        sus2_ly.addWidget(trifreq_txt, 4, 1)
        sus2_ly.addWidget(trifreq_out, 5, 1)

        d_k = QLabel()
        d_k.setText('dₖ(y)')
        d_k.setAlignment(QtCore.Qt.AlignCenter)
        y = QLabel()
        y.setText('y')
        y.setAlignment(QtCore.Qt.AlignCenter)
        d_k1 = QLabel()
        d_k1.setText('dₖ(y)')
        d_k1.setAlignment(QtCore.Qt.AlignCenter)
        y1 = QLabel()
        y1.setText('y')
        y1.setAlignment(QtCore.Qt.AlignCenter)
        d_k2 = QLabel()
        d_k2.setText('dₖ(y)')
        d_k2.setAlignment(QtCore.Qt.AlignCenter)
        y2 = QLabel()
        y2.setText('y')
        y2.setAlignment(QtCore.Qt.AlignCenter)

        sustitucionLayout = QGridLayout()

        sustitucionLayout.addWidget(d_k, 1, 0)
        sustitucionLayout.addWidget(a_label, 2, 0)
        sustitucionLayout.addWidget(b_label, 3, 0)
        sustitucionLayout.addWidget(c_label, 4, 0)
        sustitucionLayout.addWidget(d_label, 5, 0)
        sustitucionLayout.addWidget(e_label, 6, 0)
        sustitucionLayout.addWidget(f_label, 7, 0)
        sustitucionLayout.addWidget(g_label, 8, 0)
        sustitucionLayout.addWidget(h_label, 9, 0)
        sustitucionLayout.addWidget(i_label, 10, 0)
        sustitucionLayout.addWidget(y, 1, 1)
        sustitucionLayout.addWidget(sus_a, 2, 1)
        sustitucionLayout.addWidget(sus_b, 3, 1)
        sustitucionLayout.addWidget(sus_c, 4, 1)
        sustitucionLayout.addWidget(sus_d, 5, 1)
        sustitucionLayout.addWidget(sus_e, 6, 1)
        sustitucionLayout.addWidget(sus_f, 7, 1)
        sustitucionLayout.addWidget(sus_g, 8, 1)
        sustitucionLayout.addWidget(sus_h, 9, 1)
        sustitucionLayout.addWidget(sus_i, 10, 1)
        sustitucionLayout.addWidget(d_k1, 1, 2)
        sustitucionLayout.addWidget(j_label, 2, 2)
        sustitucionLayout.addWidget(k_label, 3, 2)
        sustitucionLayout.addWidget(l_label, 4, 2)
        sustitucionLayout.addWidget(m_label, 5, 2)
        sustitucionLayout.addWidget(n_label, 6, 2)
        sustitucionLayout.addWidget(o_label, 7, 2)
        sustitucionLayout.addWidget(p_label, 8, 2)
        sustitucionLayout.addWidget(q_label, 9, 2)
        sustitucionLayout.addWidget(r_label, 10, 2)
        sustitucionLayout.addWidget(y1, 1, 3)
        sustitucionLayout.addWidget(sus_j, 2, 3)
        sustitucionLayout.addWidget(sus_k, 3, 3)
        sustitucionLayout.addWidget(sus_l, 4, 3)
        sustitucionLayout.addWidget(sus_m, 5, 3)
        sustitucionLayout.addWidget(sus_n, 6, 3)
        sustitucionLayout.addWidget(sus_o, 7, 3)
        sustitucionLayout.addWidget(sus_p, 8, 3)
        sustitucionLayout.addWidget(sus_q, 9, 3)
        sustitucionLayout.addWidget(sus_r, 10, 3)
        sustitucionLayout.addWidget(d_k2, 1, 4)
        sustitucionLayout.addWidget(s_label, 2, 4)
        sustitucionLayout.addWidget(t_label, 3, 4)
        sustitucionLayout.addWidget(u_label, 4, 4)
        sustitucionLayout.addWidget(v_label, 5, 4)
        sustitucionLayout.addWidget(w_label, 6, 4)
        sustitucionLayout.addWidget(x_label, 7, 4)
        sustitucionLayout.addWidget(y_label, 8, 4)
        sustitucionLayout.addWidget(z_label, 9, 4)

        sustitucionLayout.addWidget(y2, 1, 5)
        sustitucionLayout.addWidget(sus_s, 2, 5)
        sustitucionLayout.addWidget(sus_t, 3, 5)
        sustitucionLayout.addWidget(sus_u, 4, 5)
        sustitucionLayout.addWidget(sus_v, 5, 5)
        sustitucionLayout.addWidget(sus_w, 6, 5)
        sustitucionLayout.addWidget(sus_x, 7, 5)
        sustitucionLayout.addWidget(sus_y, 8, 5)
        sustitucionLayout.addWidget(sus_z, 9, 5)
        nn_l = QLabel()
        nn_l.setText('')
        sustitucionLayout.addWidget(nn_l, 0, 6)
        sustitucionLayout.addWidget(boton_applysus, 11, 2, 1, 2)

        sus_layout.addLayout(sus1_ly)
        sus_layout.addLayout(sustitucionLayout)
        sus_layout.addLayout(sus2_ly)
        sus_layout.addStretch(1)

        sustitucion_ca.setLayout(sus_layout)
        stackedLayout.addWidget(sustitucion_ca)
        lista_caracteres = [sus_a, sus_b, sus_c, sus_d, sus_e, sus_f, sus_g, sus_h, sus_i,
                            sus_j, sus_k, sus_l, sus_m, sus_n, sus_o, sus_p, sus_q, sus_r,
                            sus_s, sus_t, sus_u, sus_v, sus_w, sus_x, sus_y, sus_z]

        # Vigenere*********************************
        vigenere_ca = QWidget()
        vigenereLayout = QGridLayout()
        input_label = QLabel()
        input_label.setText("Cipher Text")
        input_criptoanalysisVigenere = QPlainTextEdit()
        input_criptoanalysisVigenere.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        decript_label = QLabel()
        decript_label.setText("Key / Plain text")
        output_descifradoVigenere = QPlainTextEdit()
        output_descifradoVigenere.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifradoVigenere.setReadOnly(True)
        boton_submitVigenere = QPushButton(text="Submit")
        boton_submitVigenere.setStyleSheet(submit_style)
        vigenereLayout.addWidget(input_label, 0, 1)
        vigenereLayout.addWidget(decript_label, 0, 2)
        vigenereLayout.addWidget(input_criptoanalysisVigenere, 1, 1)
        vigenereLayout.addWidget(output_descifradoVigenere, 1, 2)
        vigenereLayout.addWidget(boton_submitVigenere, 2, 1)
        vigenere_ca.setLayout(vigenereLayout)
        stackedLayout.addWidget(vigenere_ca)
        boton_submitVigenere.clicked.connect(lambda: vigenereAnalisis(input_criptoanalysisVigenere, output_descifradoVigenere))
        # --------------------------funciones criptoanalisis--------------------------
        def criptanalisisHill(txt_plano, txt_cifrado):
            p = txt_plano.toPlainText().strip().upper()
            c = txt_cifrado.toPlainText().strip().upper()
            texto_cifrado = []
            texto_plano = []
            for i in c:
                i_cifrado = abc[i.upper()] % 26
                texto_cifrado.append(i_cifrado)
            for i in p:
                i_plano = abc[i.upper()] % 26
                texto_plano.append(i_plano)
            if len(texto_cifrado) == len(texto_plano):
                v, m, k = hill.attack(texto_plano, texto_cifrado)
                if not v:
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('No se encontró una clave para los textos ingresados')
                else:
                    output_m.setPlainText(str(m))
                    output_keyfound.setPlainText(str(k))
            else:
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Los textos ingresados deben tener la misma longitud de caracteres')


        def criptanalisisSus(txt):
            alphabet_lower = string.ascii_lowercase
            txt_cifrado = txt.toPlainText().strip()
            cipher = sb.substitution(txt_cifrado)
            freq_mono = cipher.mono()
            freq_di = cipher.digrams()
            freq_tri = cipher.trigrams()
            # *-*-*-*-*-*-
            monofreq_out.setFont(font)
            monofreq_out.setColumnCount(2)
            monofreq_out.setRowCount(26)
            monofreq_out.resizeRowsToContents()
            monofreq_out.setHorizontalHeaderLabels(["Letter", "Freq."])
            monofreq_out.resizeRowsToContents()
            monofreq_out.resizeColumnsToContents()
            monofreq_out.verticalHeader().hide()
            alphabet_list = sorted(freq_mono, key=lambda x: freq_mono[x])
            alphabet_list.reverse()
            for row in range(26):
                item = alphabet_list[row].upper()
                cell = QTableWidgetItem(item)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                monofreq_out.setItem(row, 0, cell)

            for row in range(26):
                try:
                    item = str(freq_mono[alphabet_list[row]])
                except:
                    item = str(0)
                cell = QTableWidgetItem(item)
                cell.setTextAlignment(Qt.AlignRight)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                monofreq_out.setItem(row, 1, cell)

            difreq_out.setFont(font)
            difreq_out.setColumnCount(2)
            difreq_out.setRowCount(len(freq_di))
            difreq_out.resizeRowsToContents()
            difreq_out.setHorizontalHeaderLabels(["Digrama", "Freq."])
            difreq_out.resizeRowsToContents()
            difreq_out.resizeColumnsToContents()
            difreq_out.verticalHeader().hide()
            digrams_order = sorted(freq_di, key=lambda x: freq_di[x])
            digrams_order.reverse()

            for row in range(len(freq_di)):
                item = digrams_order[row].upper()
                cell = QTableWidgetItem(item)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                difreq_out.setItem(row, 0, cell)
            for row in range(len(freq_di)):
                try:
                    item = str(freq_di[digrams_order[row]])
                except:
                    item = ""
                cell = QTableWidgetItem(item)
                cell.setTextAlignment(Qt.AlignRight)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                difreq_out.setItem(row, 1, cell)

            trifreq_out.setFont(font)
            trifreq_out.setColumnCount(2)
            trifreq_out.setRowCount(len(freq_tri))
            trifreq_out.resizeRowsToContents()
            trifreq_out.setHorizontalHeaderLabels(["Trigrama", "Freq."])
            trifreq_out.resizeRowsToContents()
            trifreq_out.resizeColumnsToContents()
            trifreq_out.verticalHeader().hide()
            trigrams_order = sorted(freq_tri, key=lambda x: freq_tri[x])
            trigrams_order.reverse()
            for row in range(len(freq_tri)):
                item = trigrams_order[row].upper()
                cell = QTableWidgetItem(item)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                trifreq_out.setItem(row, 0, cell)
            for row in range(len(freq_tri)):
                try:
                    item = str(freq_tri[trigrams_order[row]])
                except:
                    item = ""
                cell = QTableWidgetItem(item)
                cell.setTextAlignment(Qt.AlignRight)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                trifreq_out.setItem(row, 1, cell)

        def aplicar(lista_caracteres, txt_in, txt_out):
            llave = {string.ascii_lowercase[i]: str(lista_caracteres[i].currentText()).lower() for i in range(26)}
            #if len(set(j for i,j in llave.items())) < 26:
            #    txt_out.setPlainText("Esta sustitución no es válida. La función de esta sustitución no es inyectiva. Por favor inténtelo de nuevo")
            #    return
            cypher = sb.substitution(txt_in.toPlainText().strip())
            cypher.permutar(llave)
            txt_out.setPlainText(str(cypher.permutado))
            #criptanalisisSus(txt_out)


class BlockScreen(QDialog):

    def __init__(self):
        super(BlockScreen, self).__init__()
        def BlockButton(input, output_ref, encriptar, cryptosys, op_mode):
            # Set sizes
            image_file_name = input.file
            img_name = image_file_name.split('.')[0]
            img_extension = image_file_name.split('.')[1]
            if image_file_name != "":
                img = cv2.imread(image_file_name)
                row, column, depth = img.shape
                if encriptar == True:


                    cv2.imwrite(img_cryp_name, imageEncrypted)
                    QMessageBox.information(None, 'Success',
                                            'You can find the encrypted image here: ' + img_cryp_name +"\n"+
                                            'And the key used in the file: '+img_name+"_key"+cryptosys+op_mode+".txt",
                                            QMessageBox.Ok)
                    output_ref.open_image(img_cryp_name)
                elif encriptar == False:

        gridBlock = QGridLayout()
        gridBlock.setGeometry(QtCore.QRect(10, 10, 1030, 600))
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
        boton_cifrar_hill = crearBoton(cifrado=True)
        boton_descifrar_hill = crearBoton(cifrado=False)
        boton_cifrar_hill.clicked.connect(lambda: BlockButton(img_c, img_d, True, str(combo_img.currentText()), str(combo_modes.currentText())))
        boton_descifrar_hill.clicked.connect(lambda: BlockButton(img_d, img_c, False, str(combo_img.currentText()), str(combo_modes.currentText())))
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
        gridBlock.addWidget(boton_cifrar_hill, 3, 1)
        gridBlock.addWidget(boton_descifrar_hill, 4, 1)
        gridBlock.addWidget(boton_limpiar, 6, 1)
        gridBlock.addWidget(boton_key, 9, 0)
        gridBlock.addWidget(txt_key2, 10, 0)
        gridBlock.addWidget(boton_browsekey, 9, 2)
        gridBlock.addWidget(txt_key, 10, 2)
        gridBlock.addWidget(self.back_button, 11, 1)
        self.setLayout(gridBlock)



class PublicKeyScreen(QDialog):
    def __init__(self):
        super(PublicKeyScreen, self).__init__()
        vbox1 = QVBoxLayout()
        hbox1 = QHBoxLayout()
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
        self.back_button.setFixedWidth(150)
        tabPublicWidget = QtWidgets.QTabWidget(self)
        vbox1.addWidget(tabPublicWidget)
        hbox1.addWidget(self.back_button)
        vbox1.addLayout(hbox1)
        self.setLayout(vbox1)
        tabPublicWidget.setGeometry(QtCore.QRect(10, 20, 1150, 700))
        tabPublicWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        tabPublicWidget.setObjectName("tabPublicWidget")
        tabPublicWidget.setStyleSheet("""
        QTabWidget::tab-bar {
            left: 1px; /* move to the right by 5px */
        }
        QTabWidget::pane {
            top:-1px;
            background-color: #FFFFFF;
        }
        QTabBar::tab {
            background: #52F6E0;
            font-size: 15px;
            min-width: 200px;
            min-height: 30px;
            padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #13A5EE;
            color: white;
            font: bold;
        }
        QTabBar::tab:!selected {
            margin-top: 3px;
        }""")
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
        """
        ********************************RSA Tab***********************************
        """
        def gen_prime_numsRSA():
            p1 = find_prime(iNumBits=128, iConfidence=16)
            p2 = find_prime(iNumBits=128, iConfidence=16)
            prime1.setPlainText(str(p1))
            prime2.setPlainText(str(p2))
        def calculate_parametersRSA():
            p1 = prime1.toPlainText()
            p2 = prime2.toPlainText()
            if p1 == '' or p2 == '':
                QMessageBox.critical(None, 'Missing Prime Numbers',
                                     'Please insert/calculate prime numbers first',
                                     QMessageBox.Ok)
                return
            elif not (is_prime(int(p1), 5) and is_prime(int(p2), 5)):
                QMessageBox.critical(None, 'Not Prime Numbers',
                                     'Both numbers must be prime.',
                                     QMessageBox.Ok)
                return
            elif p1 == p2:
                QMessageBox.critical(None, 'Equal Numbers',
                                     'Both numbers cannot be equal.',
                                     QMessageBox.Ok)
                return
            phi, n, e, d = RSA.generate_key_pair(int(p1), int(p2))
            phi_pt.setPlainText(str(phi))
            n_pt.setPlainText(str(n))
            b_pt.setPlainText(str(e))
            a_pt.setPlainText(str(d))
        def encrypt_RSA():
            if prime1.toPlainText() == '' or prime2.toPlainText() == '':
                QMessageBox.critical(None, 'Missing Prime Numbers',
                                     'Please insert/calculate prime numbers first',
                                     QMessageBox.Ok)
                return
            elif b_pt.toPlainText() == '':
                QMessageBox.critical(None, 'Missing Parameters',
                                     'Calculate parameters first',
                                     QMessageBox.Ok)
                return
            key = int(b_pt.toPlainText())
            n = int(n_pt.toPlainText())
            public_k_pair = (key, n)
            p_text = plaintxtPublic.toPlainText()
            cipher = RSA.encrypt(public_k_pair, p_text)
            cipher_txt = str(cipher).strip('[]')
            ciphertxtPublic.setPlainText(cipher_txt)
        def decrypt_RSA():
            if a_pt.toPlainText() == '' or n_pt.toPlainText() == '':
                QMessageBox.critical(None, 'Missing Parameters',
                                     'Insert private key parameters first',
                                     QMessageBox.Ok)
                return
            key = int(a_pt.toPlainText())
            n = int(n_pt.toPlainText())
            private_k_pair = (key, n)
            c_text = ciphertxtPublic.toPlainText().split(",")
            c_text_int = [int(a.strip()) for a in c_text]
            plain = RSA.decrypt(private_k_pair, c_text_int)
            plaintxtPublic.setPlainText(plain)
        def clean_RSA():
            prime1.setPlainText('')
            prime2.setPlainText('')
            phi_pt.setPlainText('')
            n_pt.setPlainText('')
            b_pt.setPlainText('')
            a_pt.setPlainText('')
            plaintxtPublic.setPlainText('')
            ciphertxtPublic.setPlainText('')
        RSAWidget = QtWidgets.QWidget()
        tabPublicWidget.addTab(RSAWidget, "RSA Cryptosystem")
        vboxRSA = QVBoxLayout()
        h1boxRSA = QHBoxLayout()
        h2boxRSA = QHBoxLayout()
        RSAWidget.setLayout(vboxRSA)
        ###h1boxRSA-----------------------
        #Group Box Prime Numbers
        groupBox_prime = QGroupBox('Prime Numbers')
        groupBoxLayout_numbers = QVBoxLayout(groupBox_prime)
        groupBoxLayout_p1 = QHBoxLayout()
        groupBoxLayout_p2 = QHBoxLayout()
        groupBoxLayout_auto = QHBoxLayout()
        txt_p1 = QLabel('Prime 1 = ')
        txt_p2 = QLabel('Prime 2 = ')
        prime1 = QPlainTextEdit()
        prime2 = QPlainTextEdit()
        groupBoxLayout_p1.addWidget(txt_p1)
        groupBoxLayout_p1.addWidget(prime1)
        groupBoxLayout_p2.addWidget(txt_p2)
        groupBoxLayout_p2.addWidget(prime2)
        boton_auto = QPushButton(text="Auto-Generate")
        boton_auto.setStyleSheet(aux_style)
        boton_auto.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_auto.setFixedWidth(150)
        boton_auto.clicked.connect(gen_prime_numsRSA)
        groupBoxLayout_numbers.addLayout(groupBoxLayout_p1)
        groupBoxLayout_numbers.addLayout(groupBoxLayout_p2)
        groupBoxLayout_auto.addWidget(boton_auto)
        groupBoxLayout_auto.setAlignment(QtCore.Qt.AlignCenter)
        groupBoxLayout_numbers.addLayout(groupBoxLayout_auto)
        h1boxRSA.addWidget(groupBox_prime)
        #Group Box Parameters
        groupBox_parameters = QGroupBox('Parameters')
        groupBoxLayout_parameters = QVBoxLayout(groupBox_parameters)
        groupBoxLayout_parameters.setAlignment(QtCore.Qt.AlignCenter)
        h1_param = QHBoxLayout()
        h2_param = QHBoxLayout()
        h3_param = QHBoxLayout()
        h4_param = QHBoxLayout()
        h5_button = QHBoxLayout()
        boton_genPar = QPushButton(text="Calculate")
        boton_genPar.setStyleSheet(aux_style)
        boton_genPar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_genPar.setFixedWidth(150)
        h5_button.setAlignment(Qt.AlignCenter)
        h5_button.addWidget(boton_genPar)
        txt_publick = QLabel('Public Key: ')
        txt_privatek = QLabel('Private Key: ')
        txt_phi = QLabel('Φ(n) = ')
        txt_n = QLabel('    n = ')
        txt_b = QLabel('    b = ')
        txt_a = QLabel('    a = ')
        phi_pt = QPlainTextEdit()
        n_pt = QPlainTextEdit()
        a_pt = QPlainTextEdit()
        b_pt = QPlainTextEdit()
        h1_param.addWidget(txt_phi)
        h1_param.addWidget(phi_pt)
        h2_param.addWidget(txt_n)
        h2_param.addWidget(n_pt)
        h3_param.addWidget(txt_b)
        h3_param.addWidget(b_pt)
        h4_param.addWidget(txt_a)
        h4_param.addWidget(a_pt)
        groupBoxLayout_parameters.addLayout(h1_param)
        groupBoxLayout_parameters.addWidget(txt_publick)
        groupBoxLayout_parameters.addLayout(h2_param)
        groupBoxLayout_parameters.addLayout(h3_param)
        groupBoxLayout_parameters.addWidget(txt_privatek)
        groupBoxLayout_parameters.addLayout(h4_param)
        groupBoxLayout_parameters.addLayout(h5_button)
        h1boxRSA.addWidget(groupBox_parameters)
        boton_genPar.clicked.connect(calculate_parametersRSA)
        vboxRSA.addLayout(h1boxRSA,1)
        ###h2boxRSA------------------
        groupBox_plaintxtPublic = QGroupBox('Plain Text')
        plaintxtPublic_layout = QVBoxLayout()
        plaintxtPublic = QPlainTextEdit()
        plain_ins = QLabel('To encrypt, please make sure you introduced/generated two big different \nprime numbers and the button to calculate parameters has been pressed.')
        plaintxtPublic_layout.addWidget(plain_ins)
        plaintxtPublic_layout.addWidget(plaintxtPublic)
        groupBox_plaintxtPublic.setLayout(plaintxtPublic_layout)
        h2boxRSA.addWidget(groupBox_plaintxtPublic)
        publicButtons_layout = QVBoxLayout()
        boton_cipher_pk = crearBoton(cifrado=True)
        boton_decipher_pk = crearBoton(cifrado=False)
        boton_limpiar_pk = QPushButton(text="Clean All")
        boton_limpiar_pk.setStyleSheet(aux_style)
        boton_limpiar_pk.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar_pk.setFixedWidth(150)
        boton_cipher_pk.clicked.connect(encrypt_RSA)
        boton_decipher_pk.clicked.connect(decrypt_RSA)
        boton_limpiar_pk.clicked.connect(clean_RSA)
        publicButtons_layout.addWidget(boton_cipher_pk)
        publicButtons_layout.addWidget(boton_decipher_pk)
        publicButtons_layout.addWidget(boton_limpiar_pk)
        publicButtons_layout.setAlignment(Qt.AlignCenter)
        h2boxRSA.addLayout(publicButtons_layout)
        groupBox_ciphertxtPublic = QGroupBox('Cipher Text')
        ciphertxtPublic_layout = QVBoxLayout()
        ciphertxtPublic = QPlainTextEdit()
        cipher_ins = QLabel('To decrypt, please make sure you introduced n and a parameters. Also, separate \neach value by a comma.')
        ciphertxtPublic_layout.addWidget(cipher_ins)
        ciphertxtPublic_layout.addWidget(ciphertxtPublic)
        groupBox_ciphertxtPublic.setLayout(ciphertxtPublic_layout)
        h2boxRSA.addWidget(groupBox_ciphertxtPublic)
        vboxRSA.addLayout(h2boxRSA, 9)
        """
        ********************************Gamal Tab***********************************
        """
        def gen_prime_numGamal():
            p1 = elgamal.find_prime()
            primeGamal.setPlainText(str(p1))
        def calculate_parametersGamal():
            prime = primeGamal.toPlainText()
            if prime == '':
                QMessageBox.critical(None, 'Missing Prime Number',
                                     'Please insert/calculate a 256 bit prime number first.',
                                     QMessageBox.Ok)
                return
            elif not (is_prime(int(prime), 5)):
                QMessageBox.critical(None, 'Not a Prime Number',
                                     'The number must be prime.',
                                     QMessageBox.Ok)
                return
            p = int(prime)
            alpha = elgamal.find_primitive_root(p)
            a = random.randint( 1, (p - 1) // 2 )
            beta = modexp(alpha, a, p)
            alpha_pt.setPlainText(str(alpha))
            beta_pt.setPlainText(str(beta))
            a_ptGamal.setPlainText(str(a))
        def clean_Gamal():
            primeGamal.setPlainText('')
            alpha_pt.setPlainText('')
            beta_pt.setPlainText('')
            a_ptGamal.setPlainText('')
            plaintxtPublicGamal.setPlainText('')
            ciphertxtPublicGamal.setPlainText('')
        def encrypt_Gamal():
            if primeGamal.toPlainText() == '':
                QMessageBox.critical(None, 'Missing Prime Number',
                                     'Please insert/calculate a 256-bit prime number first',
                                     QMessageBox.Ok)
                return
            elif a_ptGamal.toPlainText() == '':
                QMessageBox.critical(None, 'Missing Parameters',
                                     'Calculate parameters first',
                                     QMessageBox.Ok)
                return
            p = int(primeGamal.toPlainText())
            alpha = int(alpha_pt.toPlainText())
            beta = int(beta_pt.toPlainText())
            p_text = plaintxtPublicGamal.toPlainText()
            cipher = elgamal.encrypt(p, alpha, beta, p_text)
            ciphertxtPublicGamal.setPlainText(cipher)
        def decrypt_Gamal():
            if a_ptGamal.toPlainText() == '' or primeGamal.toPlainText() == '':
                QMessageBox.critical(None, 'Missing Parameters',
                                     'Insert private key parameters and prime number first',
                                     QMessageBox.Ok)
                return
            p = int(primeGamal.toPlainText())
            a = int(a_ptGamal.toPlainText())
            cipher = ciphertxtPublicGamal.toPlainText()
            plain = elgamal.decrypt(p, a, cipher)
            plaintxtPublicGamal.setPlainText(plain)
        ElGamalWidget = QtWidgets.QWidget()
        tabPublicWidget.addTab(ElGamalWidget, "ElGamal Cryptosystem")
        hboxElGamal = QHBoxLayout()
        v1boxElGamal = QVBoxLayout()
        v2boxElGamal = QVBoxLayout()
        ElGamalWidget.setLayout(hboxElGamal)
        ###v1boxElGamal-----------------------
        #Group Box Prime Number
        groupBox_primegamal = QGroupBox('Prime Number')
        groupBoxLayout_primegamal = QVBoxLayout(groupBox_primegamal)
        txt_pg = QLabel('Please enter a prime number that has 256 bits in its binary representation or \ngenerate it with the button below for ease.')
        groupBoxLayout_pgamal = QHBoxLayout()
        groupBoxLayout_genprimegamal = QHBoxLayout()
        txt_pgamal = QLabel('Prime = ')
        primeGamal = QPlainTextEdit()
        groupBoxLayout_pgamal.addWidget(txt_pgamal)
        groupBoxLayout_pgamal.addWidget(primeGamal)
        boton_autogamal = QPushButton(text="Auto-Generate")
        boton_autogamal.setStyleSheet(aux_style)
        boton_autogamal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_autogamal.setFixedWidth(150)
        boton_autogamal.clicked.connect(gen_prime_numGamal)
        groupBoxLayout_genprimegamal.addWidget(boton_autogamal)
        groupBoxLayout_genprimegamal.setAlignment(QtCore.Qt.AlignCenter)
        groupBoxLayout_primegamal.addWidget(txt_pg)
        groupBoxLayout_primegamal.addLayout(groupBoxLayout_pgamal)
        groupBoxLayout_primegamal.addLayout(groupBoxLayout_genprimegamal)
        v1boxElGamal.addWidget(groupBox_primegamal)
        #Group Box ----------  Parameters
        groupBox_parametersGamal = QGroupBox('Parameters')
        groupBoxLayout_parametersGamal = QVBoxLayout(groupBox_parametersGamal)
        groupBoxLayout_parametersGamal.setAlignment(QtCore.Qt.AlignCenter)
        h1_paramGamal = QHBoxLayout()
        h2_paramGamal = QHBoxLayout()
        h3_paramGamal = QHBoxLayout()
        h5_buttonGamal = QHBoxLayout()
        boton_genParGamal = QPushButton(text="Calculate")
        boton_genParGamal.setStyleSheet(aux_style)
        boton_genParGamal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_genParGamal.setFixedWidth(150)
        h5_buttonGamal.setAlignment(Qt.AlignCenter)
        h5_buttonGamal.addWidget(boton_genParGamal)
        txt_publickGamal = QLabel('Public Key: ')
        txt_privatekGamal = QLabel('Private Key: ')
        txt_alpha = QLabel('    α = ')
        txt_beta = QLabel('    β = ')
        txt_aGamal = QLabel('    a = ')
        alpha_pt = QPlainTextEdit()
        beta_pt = QPlainTextEdit()
        a_ptGamal = QPlainTextEdit()
        h1_paramGamal.addWidget(txt_alpha)
        h1_paramGamal.addWidget(alpha_pt)
        h2_paramGamal.addWidget(txt_beta)
        h2_paramGamal.addWidget(beta_pt)
        h3_paramGamal.addWidget(txt_aGamal)
        h3_paramGamal.addWidget(a_ptGamal)
        groupBoxLayout_parametersGamal.addWidget(txt_publickGamal)
        groupBoxLayout_parametersGamal.addLayout(h1_paramGamal)
        groupBoxLayout_parametersGamal.addLayout(h2_paramGamal)
        groupBoxLayout_parametersGamal.addWidget(txt_privatekGamal)
        groupBoxLayout_parametersGamal.addLayout(h3_paramGamal)
        groupBoxLayout_parametersGamal.addLayout(h5_buttonGamal)
        v1boxElGamal.addWidget(groupBox_parametersGamal)
        boton_genParGamal.clicked.connect(calculate_parametersGamal)
        groupBox_buttonsGamal = QGroupBox('')
        buttonsGamal_layout = QVBoxLayout(groupBox_buttonsGamal)
        boton_cipher_Gamal = crearBoton(cifrado=True)
        boton_decipher_Gamal = crearBoton(cifrado=False)
        boton_limpiar_Gamal = QPushButton(text="Clean All")
        boton_limpiar_Gamal.setStyleSheet(aux_style)
        boton_limpiar_Gamal.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar_Gamal.setFixedWidth(150)
        boton_cipher_Gamal.clicked.connect(encrypt_Gamal)
        boton_decipher_Gamal.clicked.connect(decrypt_Gamal)
        boton_limpiar_Gamal.clicked.connect(clean_Gamal)
        buttonsGamal_layout.addWidget(boton_cipher_Gamal)
        buttonsGamal_layout.addWidget(boton_decipher_Gamal)
        buttonsGamal_layout.addWidget(boton_limpiar_Gamal)
        buttonsGamal_layout.setAlignment(Qt.AlignCenter)
        v1boxElGamal.addWidget(groupBox_buttonsGamal)

        groupBox_plaintxtPublicGamal = QGroupBox('Plain Text')
        plaintxtPublic_layoutGamal = QVBoxLayout()
        plaintxtPublicGamal = QPlainTextEdit()
        plain_insGamal = QLabel('To encrypt, please make sure you introduced/generated a 256 bit prime number and the button to calculate the \nparameters has been pressed.')
        plaintxtPublic_layoutGamal.addWidget(plain_insGamal)
        plaintxtPublic_layoutGamal.addWidget(plaintxtPublicGamal)
        groupBox_plaintxtPublicGamal.setLayout(plaintxtPublic_layoutGamal)
        v2boxElGamal.addWidget(groupBox_plaintxtPublicGamal)
        groupBox_ciphertxtPublicGamal = QGroupBox('Cipher Text')
        ciphertxtPublic_layoutGamal = QVBoxLayout()
        ciphertxtPublicGamal = QPlainTextEdit()
        cipher_insGamal = QLabel('To decrypt, please make sure you introduced the prime number used and the a parameter.')
        ciphertxtPublic_layoutGamal.addWidget(cipher_insGamal)
        ciphertxtPublic_layoutGamal.addWidget(ciphertxtPublicGamal)
        groupBox_ciphertxtPublicGamal.setLayout(ciphertxtPublic_layoutGamal)
        v2boxElGamal.addWidget(groupBox_ciphertxtPublicGamal)

        hboxElGamal.addLayout(v1boxElGamal, 4)
        hboxElGamal.addLayout(v2boxElGamal, 6)
        """
        ********************************DSS Tab***********************************
        """
        def browse_file():
            fname = QFileDialog.getOpenFileName(None, 'Select file', QtCore.QDir.rootPath())
            txt_file.setText(fname[0])

        DSSWidget = QtWidgets.QWidget()
        tabPublicWidget.addTab(DSSWidget, "Digital Standard System")
        vboxDSS = QVBoxLayout()
        #h1boxDSS = QHBoxLayout()
        #h2boxDSS = QHBoxLayout()
        DSSWidget.setLayout(vboxDSS)
        ###Sign
        groupBox_SignDSS = QGroupBox('Sign')
        groupBoxLayout_SignDSS = QVBoxLayout(groupBox_SignDSS)
        hsignDSS_box = QHBoxLayout()
        vKeysDSS_box = QVBoxLayout()
        vHashDSS_box = QVBoxLayout()
        hfileDSS_box = QHBoxLayout()
        boton_browsefile = QPushButton(text="Load File")
        boton_browsefile.setStyleSheet(aux_style)
        boton_browsefile.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_browsefile.setFixedWidth(150)
        boton_browsefile.clicked.connect(lambda: browse_file())
        txt_file = QLabel()
        txt_file.setStyleSheet('''
        QLabel {
            border:1px solid #161616;
        }''')
        hfileDSS_box.addWidget(boton_browsefile)
        hfileDSS_box.addWidget(txt_file)
        vKeysDSS_box.addLayout(hfileDSS_box)
        hgenKeysDSS_box = QHBoxLayout()
        boton_genKeysDSS = QPushButton(text="Generate Keys")
        boton_genKeysDSS.setStyleSheet(aux_style)
        boton_genKeysDSS.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_genKeysDSS.setFixedWidth(150)
        hgenKeysDSS_box.setAlignment(Qt.AlignCenter)
        hgenKeysDSS_box.addWidget(boton_genKeysDSS)
        #boton_genKeysDSS.clicked.connect(lambda: genKeys_DSS())
        txt_ver = QLabel('Verification Key: ')
        txt_sign = QLabel('Signing Key: ')
        txt_DSSp = QLabel('    p = ')
        txt_DSSq = QLabel('    q = ')
        txt_DSSg = QLabel('    g = ')
        txt_DSSh = QLabel('    h = ')
        txt_DSSa = QLabel('    a = ')
        DSSp_pt = QPlainTextEdit()
        DSSq_pt = QPlainTextEdit()
        DSSg_pt = QPlainTextEdit()
        DSSh_pt = QPlainTextEdit()
        DSSa_pt = QPlainTextEdit()
        h1_keysDSS = QHBoxLayout()
        h2_keysDSS = QHBoxLayout()
        h3_keysDSS = QHBoxLayout()
        h4_keysDSS = QHBoxLayout()
        h5_keysDSS = QHBoxLayout()
        h1_keysDSS.addWidget(txt_DSSp)
        h1_keysDSS.addWidget(DSSp_pt)
        h2_keysDSS.addWidget(txt_DSSq)
        h2_keysDSS.addWidget(DSSq_pt)
        h3_keysDSS.addWidget(txt_DSSg)
        h3_keysDSS.addWidget(DSSg_pt)
        h4_keysDSS.addWidget(txt_DSSh)
        h4_keysDSS.addWidget(DSSh_pt)
        h5_keysDSS.addWidget(txt_DSSa)
        h5_keysDSS.addWidget(DSSa_pt)
        vKeysDSS_box.addWidget(txt_ver)
        vKeysDSS_box.addLayout(h1_keysDSS)
        vKeysDSS_box.addLayout(h2_keysDSS)
        vKeysDSS_box.addLayout(h3_keysDSS)
        vKeysDSS_box.addLayout(h4_keysDSS)
        vKeysDSS_box.addWidget(txt_sign)
        vKeysDSS_box.addLayout(h5_keysDSS)
        vKeysDSS_box.addLayout(hgenKeysDSS_box)
        hsignDSS_box.addLayout(vKeysDSS_box)
        hhashDSS_box = QHBoxLayout()
        boton_signDSS = QPushButton(text="Sign File")
        boton_signDSS.setStyleSheet(
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
        boton_signDSS.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_signDSS.setFixedWidth(150)
        hhashDSS_box.setAlignment(Qt.AlignCenter)
        txt_hash = QLabel('SHA-Hash:')
        hash_pt = QPlainTextEdit()
        txt_signature = QLabel('Signature:')
        signature_pt = QPlainTextEdit()
        hhashDSS_box.addWidget(boton_signDSS)
        vHashDSS_box.addLayout(hhashDSS_box)
        vHashDSS_box.addWidget(txt_hash)
        vHashDSS_box.addWidget(hash_pt)
        vHashDSS_box.addWidget(txt_signature)
        vHashDSS_box.addWidget(signature_pt)
        hcleanDSS_box = QHBoxLayout()
        boton_cleansignDSS = QPushButton(text="Clean Fields")
        boton_cleansignDSS.setStyleSheet(aux_style)
        boton_cleansignDSS.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_cleansignDSS.setFixedWidth(150)
        hcleanDSS_box.setAlignment(Qt.AlignCenter)
        hcleanDSS_box.addWidget(boton_cleansignDSS)
        hcleanDSS_box.setAlignment(Qt.AlignCenter)
        vHashDSS_box.addLayout(hcleanDSS_box)
        hsignDSS_box.addLayout(vHashDSS_box)
        groupBoxLayout_SignDSS.addLayout(hsignDSS_box)
        vboxDSS.addWidget(groupBox_SignDSS)
"""
Interfaz & Layout
"""
# Crea la ventana
app = QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
welcome = WelcomeScreen()
clasicos = ClasicosScreen()
bloque = BlockScreen()
gamma = GammaScreen()
public_key = PublicKeyScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.addWidget(clasicos)
widget.addWidget(bloque)
widget.addWidget(gamma)
widget.addWidget(public_key)
widget.setFixedHeight(770)
widget.setFixedWidth(1200)
widget.setStyleSheet("background: #ffffff;")
widget.setWindowTitle("CrypTool")
widget.setCurrentIndex(0)
widget.show()
font = QtGui.QFont()
font.setFamily("Segoe UI SemiLight")
font.setPointSize(10)
QApplication.setFont(font)
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
