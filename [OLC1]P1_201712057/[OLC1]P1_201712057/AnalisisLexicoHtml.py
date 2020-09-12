from TokenHtml import Error
from TokenHtml import Token
from TokenHtml import Tipo
from tkinter import *

class ScannerHtml:
    listaTokens = list()
    listaErrores= list()
    pos_errores= ""
    posicionCar= 0
    fila= 1
    columna= 1

    def __init__(self):
        self.listaErrores = list()
        self.listaTokens = list()
        self.pos_errores= list()
        lexema = ""
        posicionCar = 0
        fila= 1
        columna=1

