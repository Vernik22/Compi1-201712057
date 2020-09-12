from TokenJs import Error
from TokenJs import Token
from TokenJs import Tipo
from tkinter import *

class ScannerJs:
    listaTokens = list()
    listaErrores = list()
    pos_errores = list()
    lexema = ""
    posicionCar = 0
    fila= 1
    columna=1

    def __init__(self):
        self.listaErrores = list()
        self.listaTokens = list()
        self.pos_errores= list()
        lexema = ""
        posicionCar = 0
        fila= 1
        columna=1

    #---------------------------Estado A
    def estadoA(self, entrada, consola):
        self.cadena = entrada + "$"
        self.caracterActual = ""
        while self.posicionCar < len(self.cadena):
            self.caracterActual = self.cadena[self.posicionCar]

            if self.caracterActual == "/":
                self.estadoB(self.posicionCar, consola)
            elif self.caracterActual == "*":
                self.addToken(Tipo.ASTERISCO, "*")
            elif self.caracterActual == ":":
                self.addToken(Tipo.DPUNTOS, ":")
            elif self.caracterActual == ";":
                self.addToken(Tipo.PCOMA, ";")
            elif self.caracterActual == ".":
                self.addToken(Tipo.PUNTO, ".")
            elif self.caracterActual == "\"":
                self.addToken(Tipo.COMILLAS, "\"")
                self.posicionCar+=1
                sizeCadena= self.getSizeCadena(self.posicionCar)
                self.estadoE(self.posicionCar,self.posicionCar+sizeCadena, consola)
                self.posicionCar = self.posicionCar + sizeCadena
                self.estadoJ(self.posicionCar, consola)
            elif self.caracterActual == "'":
                self.addToken(Tipo.COMILLASIMPLE, "'")
                self.posicionCar+=1
                sizeCadena= self.getSizeCadena(self.posicionCar)
                self.estadoE(self.posicionCar,self.posicionCar+sizeCadena, consola)
                self.posicionCar = self.posicionCar + sizeCadena
                self.estadoJ(self.posicionCar, consola)
            elif self.caracterActual == "`":
                self.addToken(Tipo.TILDE, "`")
                self.posicionCar+=1
                sizeCadena= self.getSizeCadena(self.posicionCar)
                self.estadoE(self.posicionCar,self.posicionCar+sizeCadena, consola)
                self.posicionCar = self.posicionCar + sizeCadena
                self.estadoJ(self.posicionCar, consola)
            elif self.caracterActual == "+":
                self.addToken(Tipo.MAS, "+")
            elif self.caracterActual == "-":
                self.addToken(Tipo.GUION, "-")
            elif self.caracterActual == "=":
                self.addToken(Tipo.ASIGNACION, "=")
            elif self.caracterActual == "&":
                self.addToken(Tipo.AND, "&")
            elif self.caracterActual == "|":
                self.addToken(Tipo.OR, "|")
            elif self.caracterActual == "(":
                self.addToken(Tipo.PARENTESISIZQ, "(")
            elif self.caracterActual == ")":
                self.addToken(Tipo.PARENTESISDER, ")")
            elif self.caracterActual == "{":
                self.addToken(Tipo.LLAVEIZQ, "{")
            elif self.caracterActual == "}":
                self.addToken(Tipo.LLAVEDER, "}")
            elif self.caracterActual == "[":
                self.addToken(Tipo.CORCHETEIZQ, "[")
            elif self.caracterActual == "]":
                self.addToken(Tipo.CORCHETEDER, "]")
            elif self.caracterActual == ">":
                self.addToken(Tipo.MAYORQ, ">")
            elif self.caracterActual == "<":
                self.addToken(Tipo.MENORQ, "<")
            elif self.caracterActual == "!":
                self.addToken(Tipo.ADMIRACION, "!")
            #elif self.caracterActual == "~":
            #    self.addToken(Tipo.EÑE, "~")
            elif self.caracterActual == "%":
                self.addToken(Tipo.PORCENTAJE, "%")
            elif self.caracterActual == "_":
                self.addToken(Tipo.GUIONBAJO, "_")
            elif self.caracterActual == ",":
                self.addToken(Tipo.COMA, ",")


            #estado A a estado G (Numeros)
            elif self.caracterActual.isnumeric():            
                sizeLexema = self.getSizeLexema(self.posicionCar)
                self.estadoG(self.posicionCar,self.posicionCar+sizeLexema , consola)
                self.posicionCar = self.posicionCar + sizeLexema
            
            #estado A a estado C (Reservadas e IDs)
            elif self.caracterActual.isalpha():
                sizeLexema = self.getSizeLexema(self.posicionCar)
                self.estadoC(self.posicionCar,self.posicionCar+sizeLexema, consola)
                #self.reservadas(posicionCar, posicionCar+sizeLexema)
                self.posicionCar = self.posicionCar + sizeLexema
            
            #otros
            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                if self.caracterActual=="\n":
                    self.fila += 1
                self.posicionCar += 1 #incremento del contador del while
                
                continue
            
            #manejo de Errores
            else:                    
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and self.posicionCar == len(self.cadena)-1:
                    if len(self.listaErrores) > 0:
                        return "corregir los errores"
                    return "analisis exitoso...!!!"
                #  S0 -> ERROR_LEXICO
                else:
                    self.addError(self.columna,self.fila, self.caracterActual)
                    print("Error Lexico: ", self.caracterActual)
                    consola.insert('1.0', "Error Lexico: "+self.caracterActual+"\n")
                    for i in range(0,len(self.listaErrores)):
                        valor = self.listaErrores[i].getValor()
                        valor += str(self.listaErrores[i].getColumna())
                        valor += str(self.listaErrores[i].getFila())
                        print(valor)


            self.posicionCar +=1 #incremento contador while
        
        if len(self.listaErrores)>0:
            return "La entrada que ingresaste fue: Exiten Errores Lexicos" 
        else:
            return "La entrada que ingresaste fue:" + self.cadena + "\n Analisis Exitoso"

    #----------------------Estado B
    def estadoB(self,posActual,consola):
        c=self.cadena[posActual+1]              
        if c == '*':
            self.addToken(Tipo.DIAGONAL, "/")
            self.addToken(Tipo.ASTERISCO, "*")
            self.posicionCar = posActual+2
            sizeComentario= self.getSizeComentarioMulti(self.posicionCar)
            #print("pasa por B con "+c)
            self.estadoH(self.posicionCar, self.posicionCar+sizeComentario, consola)
            self.posicionCar = self.posicionCar +sizeComentario
            #print("va a L con "+c)
            self.estadoL(self.posicionCar, consola)
        elif c == '/':
            self.addToken(Tipo.DIAGONAL, "/")
            self.addToken(Tipo.DIAGONAL, "/")
            self.posicionCar = posActual+2
            sizeComentario= self.getSizeComentarioUni(self.posicionCar)
            self.estadoI(self.posicionCar, self.posicionCar+sizeComentario, consola)
            self.posicionCar = self.posicionCar +sizeComentario

        else:
            self.pos_errores.append(posActual)
            self.addError(self.columna,self.fila, c)
            print("Error Lexico: ", c)
            consola.insert('1.0', "Error Lexico: "+c+"\n")
        

            

    #----------------------Estado C
    def estadoC(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                        #print("paso por ID")
                    self.lexema = ""
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            elif c == '-':
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            elif c == '_':
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")


            posActual +=1 #incremento contador while

    #--------------------Estado D
    def estadoD(self,posActual,consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            self.caracterActual = self.cadena[self.posicionCar]



            posActual +=1 #incremento contador while

    #--------------------Estado E
    def estadoE(self,posActual,fin,consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.CADENA, self.lexema)
                self.lexema = ""
            
            posActual += 1

    #------------------------Estado F
   
    #-------------------------Estado G
    def estadoG(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            if c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.NUMERO, self.lexema)
                    self.lexema = ""
            elif c =='.':
                #mandar al estado J
                self.lexema += c
                posActual += 1
                self.estadoK(posActual,fin, consola)
                break
            else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")

            posActual +=1 #incremento contador while

    #-------------------------Estado H
    def estadoH(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.COMENTARIO, self.lexema)
                self.lexema = ""
            
            posActual += 1
    
    #------------------------Estado I
    def estadoI(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.COMENTARIO, self.lexema)
                self.lexema = ""
            
            posActual += 1

    #------------------------Estado J
    def estadoJ(self,posActual,consola):
        c=self.cadena[posActual]
        if c == '"':
            self.addToken(Tipo.COMILLAS, "\"")
            self.posicionCar += 1
            #for i in range(0,len(self.listaTokens)):
            #    valor = self.listaTokens[i].getValor()
            #    print(valor)
        elif c=='\'':
            self.addToken(Tipo.COMILLASIMPLE, "'")
            self.posicionCar += 1
        elif c=='`':
            self.addToken(Tipo.TILDE, "`")
            self.posicionCar += 1


    #------------------------Estado K
    def estadoK(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            if c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.NUMERO, self.lexema)
                    self.lexema = ""
            
            # estadoG -> Error Lexico o manejar los hexadecimales
            else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")

            posActual +=1 #incremento contador while
            
    #----------------------Estado L
    def estadoL(self,posActual,consola):
        if(posActual+1 < len(self.cadena)-1):
            c=self.cadena[posActual+1]
            
            if c == '/':
                self.addToken(Tipo.ASTERISCO, "*")
                self.posicionCar += 1
                self.estadoM(self.posicionCar, consola)
            else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, "Error, No se terminan los comentarios con */")
                print("Error, No se terminan los comentarios con */")
                consola.insert('1.0', "Error, No se terminan los comentarios con */")

    #------------------------Estado M
    def estadoM(self,posActual,consola):
        c=self.cadena[posActual]
        if c== '/':
            self.addToken(Tipo.DIAGONAL, "/")
            self.posicionCar += 1
            c=self.cadena[self.posicionCar]
            if c=="\n":
                    self.fila += 1
           # for i in range(0,len(self.listaTokens)):
           #    valor = self.listaTokens[i].getValor()
           #   print(valor)
        else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, "Error, No se terminan los comentarios con */")
                print("Error, No se terminan los comentarios con */")
                consola.insert('1.0', "Error, No se terminan los comentarios con */")

    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i] == " " or self.cadena[i] == "{" or self.cadena[i] == "}" or self.cadena[i] == "(" or self.cadena[i] == ")" or self.cadena[i] == "," or self.cadena[i] == "." or self.cadena[i] == ";" or self.cadena[i] == ":"or self.cadena[i] == "\"" or self.cadena[i] == "'" or self.cadena[i] == "`" or self.cadena[i] == "[" or self.cadena[i] == "]" or self.cadena[i] == "*" or self.cadena[i] == "+" or self.cadena[i] == "="or self.cadena[i] == "&" or self.cadena[i] == "|" or self.cadena[i] == "<" or self.cadena[i] == ">" or self.cadena[i] == "!" or self.cadena[i] == "~" or self.cadena[i] == "\n" or self.cadena[i] == "\t" or self.cadena[i] == "\r":# or self.entrada[i] == "$":
                if self.cadena[i]=="\n":
                    self.fila += 1
                break
            longitud+=1
        return longitud

    def getSizeComentarioMulti(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i]=="\n":
                self.fila += 1
            if self.cadena[i] == "*" and self.cadena[i+1] == "/":
                break
            longitud+=1
        return longitud

    def getSizeComentarioUni(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i]=="\n":
                self.fila += 1
                break
            longitud+=1
        return longitud

    def getSizeCadena(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i]=="\n":
                self.fila += 1
            if self.cadena[i] == "\"" or self.cadena[i] == "\'"or self.cadena[i] == "`":
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

    
    def reservadas(self, palabra):
        if palabra.lower() =="var":
            self.addToken(Tipo.VAR , "var")
            #print("paso por Color")
            return True
        elif palabra.lower() =="continue":
            self.addToken(Tipo.CONTINUE , "continue")
            return True
        elif palabra.lower() =="break":
            self.addToken(Tipo.BREAK , "break")
            return True
        elif palabra.lower() =="return":
            self.addToken(Tipo.RETURN , "return")
            return True
        elif palabra.lower() =="if":
            self.addToken(Tipo.IF , "if")
            return True
        elif palabra.lower() =="else":
            self.addToken(Tipo.ELSE , "else")
            return True
        elif palabra.lower() =="for":
            self.addToken(Tipo.FOR , "for")
            return True
        elif palabra.lower() =="while":
            self.addToken(Tipo.WHILE , "while")
            return True
        elif palabra.lower() =="do":
            self.addToken(Tipo.DO , "do")
            return True
        elif palabra.lower() =="function":
            self.addToken(Tipo.FUNCTION , "function")
            return True
        elif palabra.lower() =="class":
            self.addToken(Tipo.CLASS , "class")
            return True
        elif palabra.lower() =="constuctor":
            self.addToken(Tipo.CONSTRUCTOR , "constructor")
            return True
        elif palabra.lower() =="null":
            self.addToken(Tipo.NULL , "null")
            return True
        elif palabra.lower() =="delete":
            self.addToken(Tipo.DELETE , "delete")
            return True
        elif palabra.lower() =="true":
            self.addToken(Tipo.TRUE , "true")
            return True
        elif palabra.lower() =="false":
            self.addToken(Tipo.FALSE , "false")
            return True
        elif palabra.lower() =="new":
            self.addToken(Tipo.NEW , "new")
            return True
        elif palabra.lower() =="undefined":
            self.addToken(Tipo.UNDEFINED , "undefined")
            return True
        elif palabra.lower() =="typeof":
            self.addToken(Tipo.TYPEOF , "typeof")
            return True
        elif palabra.lower() =="void":
            self.addToken(Tipo.VOID , "void")
            return True
        elif palabra.lower() =="console":
            self.addToken(Tipo.CONSOLE , "console")
            return True
        elif palabra.lower() =="const":
            self.addToken(Tipo.CONST , "const")
            return True
        elif palabra.lower() =="case":
            self.addToken(Tipo.CASE , "case")
            return True
        elif palabra.lower() =="catch":
            self.addToken(Tipo.CATCH , "catch")
            return True
        elif palabra.lower() =="default":
            self.addToken(Tipo.DEFAULT , "default")
            return True
        elif palabra.lower() =="export":
            self.addToken(Tipo.EXPORT , "export")
            return True
        elif palabra.lower() =="extends":
            self.addToken(Tipo.EXTENDS , "extends")
            return True
        elif palabra.lower() =="finally":
            self.addToken(Tipo.FINALLY , "finally")
            return True
        elif palabra.lower() =="import":
            self.addToken(Tipo.IMPORT , "import")
            return True
        elif palabra.lower() =="in":
            self.addToken(Tipo.IN , "in")
            return True
        elif palabra.lower() =="instanceof":
            self.addToken(Tipo.INSTANCEOF , "instanceof")
            return True
        elif palabra.lower() =="switch":
            self.addToken(Tipo.SWITCH , "switch")
            return True
        elif palabra.lower() =="this":
            self.addToken(Tipo.THIS , "this")
            return True
        elif palabra.lower() =="throw":
            self.addToken(Tipo.THROW , "throw")
            return True
        elif palabra.lower() =="try":
            self.addToken(Tipo.TRY , "try")
            return True
        elif palabra.lower() =="with":
            self.addToken(Tipo.WITH , "with")
            return True
        elif palabra.lower() =="static":
            self.addToken(Tipo.STATIC , "static")
            return True
        elif palabra.lower() =="private":
            self.addToken(Tipo.PRIVATE , "private")
            return True
        elif palabra.lower() =="protected":
            self.addToken(Tipo.PROTECTED , "protected")
            return True
        elif palabra.lower() =="public":
            self.addToken(Tipo.PUBLIC , "public")
            return True
        else:
            return False
        
    