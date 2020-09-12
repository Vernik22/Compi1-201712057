from enum import Enum

class Tipo(Enum):
    #simbolos
    MENORQ= 1
    MAYORQ= 2
    DIAGONAL= 3
    COMILLADOBLE= 4
    ASIGNACION= 5
    GUION= 6
    ADMIRACION= 7

    #reservadas
    HTML= 8
    HEAD= 9
    TITLE= 10
    BODY= 11
    H1= 12
    H2= 13
    H3= 14
    H4= 15
    H5= 16
    H6= 17
    P= 18
    IMG= 19
    SRC= 20
    A= 21
    HREF= 22
    UL= 23
    LI= 24
    STYLE= 25
    TH= 26
    TR= 27
    TD= 28
    CAPTION= 29
    COL= 30
    THEAD= 31
    TBODY= 32
    TFOOT= 33
    TABLE= 34
    BR= 35
    DIV= 36
    STRONG= 37
    OL= 38
    SPAN= 39


    #Expresiones
    ID= 40
    CADENA= 41
    COMENTARIO= 42
    NINGUNO = 43


class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor ):
        self.tipoToken = tipo
        self.valorToken = valor

    def getTipo(self):
        return self.tipoToken
    
    def getValor(self):
        return self.valorToken


class Error:
    columna = 0
    fila = 0
    valor = ""
    def __init__(self,columna, fila,valor):
        self.columna = columna
        self.fila= fila
        self.valor = valor
    
    def getColumna(self):
        return self.columna
    def getFila(self):
        return self.fila
    def getValor(self):
        return self.valor