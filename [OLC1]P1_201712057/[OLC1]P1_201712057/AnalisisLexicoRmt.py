from TokenRmt import Tipo
from TokenRmt import Token
from TokenRmt import Error
from tkinter import *

class ScannerRmt:
    listaTokens = list()
    listaErrores = list()
    lexema = ""
    posicionCar = 0
    fila=0
    columna=0
    def __init__(self):
        self.listaErrores = list()
        self.listaTokens = list()
        lexema = ""
        posicionCar = 0

    #------------------------------Estado A
    def estadoA(self,entrada, consola):
        self.cadena = entrada + "$"
        self.caracterActual = ""

        while self.posicionCar < len(self.cadena):
            self.caracterActual = self.cadena[self.posicionCar]
            if self.caracterActual == "/":
                self.addToken(Tipo.SIGNO_DIV, "/")
            elif self.caracterActual == "*":
                self.addToken(Tipo.SIGNO_POR, "*")
            elif self.caracterActual == "-":
                self.addToken(Tipo.SIGNO_MEN, "-")
            elif self.caracterActual == "+":
                self.addToken(Tipo.SIGNO_MAS, "+")
            elif self.caracterActual == "^":
                self.addToken(Tipo.SIGNO_POW, "^")
            elif self.caracterActual == "(":
                self.addToken(Tipo.PARENTESIS_IZQ, "(")
            elif self.caracterActual == ")":
                self.addToken(Tipo.PARENTESIS_DER, ")")

            elif self.caracterActual.isalpha():
                sizeLexema = self.getSizeLexema(self.posicionCar)
                self.estadoC(self.posicionCar, self.posicionCar + sizeLexema,consola)
                self.posicionCar= self.posicionCar+sizeLexema

            elif self.caracterActual.isnumeric():
                sizeLexema = self.getSizeLexema(self.posicionCar)
                self.estadoB(self.posicionCar,self.posicionCar+sizeLexema , consola)
                self.posicionCar = self.posicionCar + sizeLexema

            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                if self.caracterActual=="\n":
                    self.fila += 1
                self.posicionCar += 1 #incremento del contador del while
                
                continue
            
            else:                    
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and self.posicionCar == len(self.cadena)-1:
                    
                    if len(self.listaErrores) > 0:
                        
                        return "corregir los errores, incorrecto"
                    
                    return "analisis exitoso...!!!"
                #  S0 -> ERROR_LEXICO
                else:
                    
                    print("Error Lexico: ", self.caracterActual)
                    consola.insert('1.0', "Error Lexico: "+self.caracterActual+"\n")
                    return "corregir los errores, incorrecto"
                    
            self.posicionCar +=1 #incremento contador while


        if len(self.listaErrores)>0:
            
            return "La entrada que ingresaste fue: Exiten Errores Lexicos" 
        else:
            
            return "La entrada que ingresaste fue:" + self.cadena + "\n Analisis Exitoso"


    #---------------------Estado B
    def estadoB(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            if c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    
                    self.addToken(Tipo.NUMERO_ENTERO, self.lexema)
                    self.lexema = ""
            elif c =='.':
                #mandar al estado J
                self.lexema += c
                posActual += 1
                self.estadoD(posActual,fin, consola)
                break
            else:
                
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")

            posActual +=1 #incremento contador while

    #--------------------------estadoD
    def estadoD(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            if c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    
                    self.addToken(Tipo.NUMERO_REAL, self.lexema)
                    self.lexema = ""
            
            # estadoG -> Error Lexico o manejar los hexadecimales
            else:
                              
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")

            posActual +=1 #incremento contador while

    #------------------------estado C
    def estadoC(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)   
                    self.lexema = ""
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            elif c == '_':
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            else:
                
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")


            posActual +=1 #incremento contador while


    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i] == " " or self.cadena[i] == "(" or self.cadena[i] == ")" or self.cadena[i] == "*" or self.cadena[i] == "+" or self.cadena[i] == "-" or self.cadena[i] == "/" or self.cadena[i] == "^" or self.cadena[i] == "\n" or self.cadena[i] == "\t" or self.cadena[i] == "\r":# or self.entrada[i] == "$":
                break
            longitud+=1
        return longitud

    def addToken(self, tipo, valor):
    
        nuevo = Token(tipo, valor)
        self.listaTokens.append(nuevo)
        self.caracterActual = ""
        self.estado = 0
        self.lexema = ""

    def addError(self, columna, fila, valor):
    
        nuevo = Error(columna, fila, valor)
        self.listaErrores.append(nuevo)
        #puede que tenga que agregar algo