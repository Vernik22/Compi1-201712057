from enum import Enum

class Tipo(Enum):
    #Simbolos
    LLAVEIZQ = 1
    LLAVEDER = 2
    DPUNTOS = 3
    PCOMA = 4
    COMA = 5
    PUNTO = 6
    NUMERAL = 7
    PARENTESISIZQ = 8
    PARENTESISDER = 9
    COMILLAS = 10
    ASTERISCO = 11
    GUION = 12
    PORCENTAJE = 67
    DIAGONAL = 68

    #Reservadas
    PX = 13
    EM = 14
    VH = 15
    VW = 16
    IN = 17
    CM= 18
    MM = 19
    PT= 20
    PC=21
    REM=22

    COLOR = 23
    BGCOLOR = 24  #BACKGROUND-COLOR
    BGIMAGE = 25
    BORDER = 26
    OPACITY = 27
    BG=28
    TEXTALIGN =29
    FONTFAMILY = 30
    FONTSTYLE= 31
    FONTWEIGHT = 32
    FONTSIZE=33
    FONT = 34
    PADDINGL = 35
    PADDINGR= 36
    PADDINGB= 37
    PADDINGT= 38
    PADDING = 39
    DISPLAY = 40
    LINEHEIGHT = 41
    WIDTH = 42
    HEIGHT = 43
    MARGINT= 44
    MARGINR = 45
    MARGINB=46
    MARGINL = 47
    MARGIN = 48
    BORDERSTYLE=49
    POSITION = 50
    BOTTOM = 51
    TOP = 52
    RIGHT= 53
    LEFT=54
    FLOAT = 55
    CLEAR = 56
    MAXWIDTH = 57
    MINWHIDTH = 58
    MAXHEIGHT = 59
    MINHEIGHT = 60
    URL = 65
    CONTENT = 66
    
    #Expresiones
    NINGUNO = 61
    ID = 62
    NUMERO= 63
    HEXADECIMAL = 64
    COMENTARIO = 69
    CADENA = 70


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