from enum import Enum

class Tipo(Enum):
    # Simbolos --------------------------------
    LLAVEIZQ = 1
    LLAVEDER = 2
    PCOMA = 3
    COMA = 4
    PUNTO = 5 
    PARENTESISIZQ = 6
    PARENTESISDER = 7
    COMILLAS = 8
    ASTERISCO = 9
    GUION = 10
    PORCENTAJE = 11
    DIAGONAL = 12
    ASIGNACION = 13
    MAS = 14
    MENORQ= 15
    MAYORQ= 16
    AND = 17
    POTENCIA= 18
    OR = 19
    COMILLASIMPLE= 20
    TILDE= 21
    GUIONBAJO= 22
    ADMIRACION=23
    CORCHETEIZQ= 24
    CORCHETEDER= 25
    EÑE= 26
    DPUNTOS = 72
    

    #Reservadas --------------------------------------
    VAR = 27
    CONTINUE = 28
    BREAK = 29
    RETURN = 30
    IF= 31
    ELSE= 32
    FOR= 33
    WHILE= 34 
    DO = 35
    FUNCTION= 36
    CLASS= 37
    CONSTRUCTOR= 38
    NULL= 39
    DELETE= 40 
    TRUE= 41
    FALSE= 42
    NEW= 43
    UNDEFINED= 44
    TYPEOF= 45
    VOID= 46
    CONSOLE= 47
    CONST= 53
    CASE= 54
    CATCH= 55
    DEFAULT= 56
    EXPORT= 57
    EXTENDS= 58
    FINALLY= 59
    IMPORT= 60
    IN= 61
    INSTANCEOF = 62
    SWITCH= 63
    THIS= 64
    THROW= 65
    TRY= 66
    WITH= 67
    STATIC= 68
    PRIVATE= 69
    PROTECTED= 70
    PUBLIC= 71
    

    #Expresiones --------------------------------------------
    NINGUNO= 48
    ID= 49
    NUMERO= 50
    CADENA= 51
    COMENTARIO= 52


    

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
