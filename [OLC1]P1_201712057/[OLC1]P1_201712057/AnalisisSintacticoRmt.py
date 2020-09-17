from TokenRmt import Tipo
from TokenRmt import Token

class SintacticoRmt:

    controlToken=0
    listaTokens=list()
    listaError= list()
    tokenActual=Tipo.NINGUNO

    def __init__(self, listTokens):
        self.controlToken=0
        self.listaTokens= listTokens
        self.tokenActual=Tipo.NINGUNO
        self.listaError = list()
        self.agregarUltimo()

    def E(self):
        self.T()
        self.EP()

    def EP(self):
        if self.listaTokens[self.controlToken].getTipo() == Tipo.SIGNO_MAS:
            self.emparejar(Tipo.SIGNO_MAS)
            self.T()
            self.EP()
        elif self.listaTokens[self.controlToken].getTipo() == Tipo.SIGNO_MEN:
            self.emparejar(Tipo.SIGNO_MEN)
            self.T()
            self.EP()
        else:
            return
        

    def T(self):
        self.F()
        self.TP()

    def TP(self):
        if self.listaTokens[self.controlToken].getTipo() == Tipo.SIGNO_POR:
            self.emparejar(Tipo.SIGNO_POR)
            self.F()
            self.TP()
        elif self.listaTokens[self.controlToken].getTipo() == Tipo.SIGNO_DIV:
            self.emparejar(Tipo.SIGNO_DIV)
            self.F()
            self.TP()
        elif self.listaTokens[self.controlToken].getTipo() == Tipo.SIGNO_POW:
            self.emparejar(Tipo.SIGNO_POW)
            self.F()
            self.TP()
        else:
            return
        
    
    def F(self):
        if self.listaTokens[self.controlToken].getTipo() == Tipo.PARENTESIS_IZQ:
            self.emparejar(Tipo.PARENTESIS_IZQ)
            self.E()
            self.emparejar(Tipo.PARENTESIS_DER)
        elif self.listaTokens[self.controlToken].getTipo() == Tipo.NUMERO_ENTERO:
            self.emparejar(Tipo.NUMERO_ENTERO)
           
        elif self.listaTokens[self.controlToken].getTipo() == Tipo.NUMERO_REAL:
            self.emparejar(Tipo.NUMERO_REAL)
            


    def emparejar(self,tipo):
        if self.listaTokens[self.controlToken].getTipo() != tipo:
            self.listaError.append("Se esperaba"+str(tipo))
            if self.listaTokens[self.controlToken].getTipo() != Tipo.ULTIMO:
                if self.controlToken< len(self.listaTokens):
                    self.controlToken+=1
        else:
            if self.controlToken< len(self.listaTokens):
                self.controlToken+=1
        #if 

    
    def agregarUltimo(self):
        self.addToken(Tipo.ULTIMO, "ultimo")

    def getErrores(self):
        return self.listaError

    def addToken(self, tipo, valor):
    
        nuevo = Token(tipo, valor)
        self.listaTokens.append(nuevo)
        self.caracterActual = ""
        self.estado = 0
        self.lexema = ""
