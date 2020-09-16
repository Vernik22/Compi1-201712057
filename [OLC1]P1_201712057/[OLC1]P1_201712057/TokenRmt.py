from enum import Enum

class Tipo(Enum):
    NUMERO_ENTERO=1
    NUMERO_REAL=2
    SIGNO_MAS=3
    SIGNO_MEN= 4
    SIGNO_POR= 5
    SIGNO_DIV= 6
    SIGNO_POW= 7
    PARENTESIS_IZQ= 8
    PARENTESIS_DER= 9

    ID=11
 
    NINGUNO=10

class Token:
    tipoToken= Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor):
        self.tipoToken= tipo
        self.valorToken = valor

    def getTipo(self):
        return self.tipoToken
    
    def getValor(self):
        return self.valorToken
    
class Error:
    columna=0
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

 
