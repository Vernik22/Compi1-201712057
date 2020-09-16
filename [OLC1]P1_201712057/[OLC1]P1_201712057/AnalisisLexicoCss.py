from TokenCss import Token
from TokenCss import Tipo
from TokenCss import Error
from tkinter import *
from ReporteHtml import reporteHtml
from CorreccionErrores import Correccion
import os

class ScannerCss :
    listaTokens = list()
    listaErrores = list()
    pos_errores = list()
    estado = 0
    lexema = ""
    bitacora = ""
    posicionCar = 0
    fila= 1
    columna=1
    cadena=""
    rutaDestino1=""

    def __init__(self):
        self.listaErrores = list()
        self.listaTokens = list()
        self.pos_errores = list()
        estado= 0
        lexema = ""
        bitacora = ""
        posicionCar = 0
        fila= 1
        columna=1
        cadena=""
        rutaDestino1=""

    def borrarTokenYErrores(self):
        self.rutaDestino1=self.rutaDestino()
        if os.path.isfile(self.rutaDestino1+"Tokens.html"):
            os.remove(self.rutaDestino1+"Tokens.html")

        if os.path.isfile(self.rutaDestino1+"reporteErrores.html"):
            os.remove(self.rutaDestino1+"reporteErrores.html")

    def reporteBitacora(self):
        return self.bitacora

    def getFilas(self):
        return self.fila
    #----------------------estado A 
    def estadoA(self,entrada, consola):
        self.cadena = entrada + "$"
        self.caracterActual = ""
        self.borrarTokenYErrores()

        
        while self.posicionCar < len(self.cadena):
            self.caracterActual = self.cadena[self.posicionCar]
            

            #estado A a estado B para comentarios
            if self.caracterActual == "/":
                self.bitacora +=" ->estadoA->B[/]\n"
               # self.addToken(Tipo.DIAGONAL, "/")  #mandar a estado B por comentario
                self.estadoB(self.posicionCar, consola)
            elif self.caracterActual == "{":
                self.bitacora +=" ->estadoA->#D[{]\n"
                self.addToken(Tipo.LLAVEIZQ, "{")
            elif self.caracterActual == "}":
                self.bitacora +=" ->estadoA->#D[}]\n"
                self.addToken(Tipo.LLAVEDER, "}")
            elif self.caracterActual == ":":
                self.bitacora +=" ->estadoA->#D[:]\n"
                self.addToken(Tipo.DPUNTOS, ":")
            elif self.caracterActual == ";":
                self.bitacora +=" ->estadoA->#D[;]\n"
                self.addToken(Tipo.PCOMA, ";")
            elif self.caracterActual == ",":
                self.bitacora +=" ->estadoA->#D[,]\n"
                self.addToken(Tipo.COMA, ",")
            elif self.caracterActual == ".":
                self.bitacora +=" ->estadoA->#D[.]\n"
                self.addToken(Tipo.PUNTO, ".")
            elif self.caracterActual == "#":
                self.bitacora +=" ->estadoA->#D[#]\n"
                self.addToken(Tipo.NUMERAL, "#")
            elif self.caracterActual == "(":
                self.bitacora +=" ->estadoA->#D[(]\n"
                self.addToken(Tipo.PARENTESISIZQ, "(")
            elif self.caracterActual == ")":
                self.bitacora +=" ->estadoA->#D[)]\n"
                self.addToken(Tipo.PARENTESISDER, ")")
            elif self.caracterActual == '"':
                self.bitacora +=" ->estadoA->E[\"]\n"
                self.addToken(Tipo.COMILLAS, '"')
                self.posicionCar+=1
                sizeCadena= self.getSizeCadena(self.posicionCar)
                self.estadoE(self.posicionCar,self.posicionCar+sizeCadena, consola)
                self.posicionCar = self.posicionCar + sizeCadena
                self.estadoI(self.posicionCar, consola)
            elif self.caracterActual == "*":
                self.bitacora +=" ->estadoA->#D[*]\n"
                self.addToken(Tipo.ASTERISCO, "*")
            elif self.caracterActual == "-":
                self.bitacora +=" ->estadoA->#D[-]\n"
                self.addToken(Tipo.GUION, "-") #mandar a estado F por numero negativo
            elif self.caracterActual == "%":
                self.bitacora +=" ->estadoA->#D[%]\n"
                self.addToken(Tipo.PORCENTAJE , "%")

            #estado A a estado G (Numeros)
            elif self.caracterActual.isnumeric():            
                self.bitacora +=" ->estadoA->#G[Num]\n"
                sizeLexema = self.getSizeLexema(self.posicionCar)
                self.estadoG(self.posicionCar,self.posicionCar+sizeLexema , consola)
                self.posicionCar = self.posicionCar + sizeLexema

            #estado A a estado C (Reservadas e IDs)
            elif self.caracterActual.isalpha():
                self.bitacora +=" ->estadoA->#C[Let]\n"
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
                    reporte = reporteHtml()
                    correccion = Correccion()
                    if len(self.listaErrores) > 0:
                        reporte.vistaTokens(self.listaTokens,self.rutaDestino1)    
                        reporte.reporteEnHtml(self.listaErrores,self.rutaDestino1)
                        correccion.eliminarC(self.rutaDestino1,entrada,"css",self.pos_errores)
                        return "corregir los errores"
                    reporte.vistaTokens(self.listaTokens,self.rutaDestino1)
                    return "analisis exitoso...!!!"
                #  S0 -> ERROR_LEXICO
                else:
                    self.addError(self.columna,self.fila, self.caracterActual)
                    self.pos_errores.append(self.posicionCar)
                    print("Error Lexico: ", self.caracterActual)
                    consola.insert('1.0', "Error Lexico: "+self.caracterActual+"\n")
                    for i in range(0,len(self.listaErrores)):
                        valor = self.listaErrores[i].getValor()
                        valor += str(self.listaErrores[i].getColumna())
                        valor += str(self.listaErrores[i].getFila())
                        print(valor)
            self.posicionCar +=1 #incremento contador while


        if len(self.listaErrores)>0:
            reporte = reporteHtml() 
            correccion= Correccion()
            reporte.reporteEnHtml(self.listaErrores,self.rutaDestino1)
            reporte.vistaTokens(self.listaTokens,self.rutaDestino1)
            correccion.eliminarC(self.rutaDestino1,entrada,"css",self.pos_errores)
            return "La entrada que ingresaste fue: Exiten Errores Lexicos" 
        else:
            reporte = reporteHtml()
            reporte.vistaTokens(self.listaTokens,self.rutaDestino1)
            return "La entrada que ingresaste fue:" + self.cadena + "\n Analisis Exitoso"

    #-----------------------estado B
    def estadoB(self,posActual,consola):
        c=self.cadena[posActual+1]
        
        if c == '*':
            self.bitacora +=" ->estadoB->H[*]\n"
            self.addToken(Tipo.DIAGONAL, "/")
            self.addToken(Tipo.ASTERISCO, "*")
            self.posicionCar = posActual+2
            sizeComentario= self.getSizeComentario(self.posicionCar)
            #print("pasa por B con "+c)
            self.estadoH(self.posicionCar, self.posicionCar+sizeComentario, consola)
            self.posicionCar = self.posicionCar +sizeComentario
            #print("va a L con "+c)
            self.estadoL(self.posicionCar, consola)
        else:
            self.bitacora +=" ->estadoB->EE["+c+"]\n"
            self.pos_errores.append(posActual)
            self.addError(self.columna,self.fila, c)
            print("Error Lexico: ", c)
            consola.insert('1.0', "Error Lexico: "+c+"\n")
        

    #-----------------------estado c
    def estadoC(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            

            if c.isalpha():
                self.bitacora +=" ->estadoC->#C["+c+"]\n"
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                        #print("paso por ID")
                    self.lexema = ""
            elif c.isnumeric():
                self.bitacora +=" ->estadoC->#C["+c+"]\n"
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            elif c == '-':
                self.bitacora +=" ->estadoC->#C[-]\n"
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            elif c == '#':
                self.bitacora +=" ->estadoC->#C[#]\n"
                self.lexema += c
                if(posActual+1 == fin):
                    if(self.reservadas(self.lexema)!=True):
                        self.addToken(Tipo.ID, self.lexema)
                    self.lexema = ""
            else:
                self.bitacora +=" ->estadoC->EE["+c+"]\n"
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")

        
            posActual += 1
    #-----------------------estado E
    def estadoE(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            self.bitacora +=" ->estadoE->E["+c+"]\n"
            c= self.cadena[posActual]

            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.CADENA, self.lexema)
                self.lexema = ""
            posActual += 1

    #-----------------------estado G
    def estadoG(self, posActual, fin, consola):
        c=''
        while posActual < fin:            
            c= self.cadena[posActual]
            

            if c.isnumeric():
                self.bitacora +=" ->estadoG->#G["+c+"]\n"
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.NUMERO, self.lexema)
                    self.lexema = ""
            elif c =='.':
                #mandar al estado J
                self.bitacora +=" ->estadoG->#J[.]\n"
                self.lexema += c
                posActual += 1
                self.estadoJ(posActual,fin, consola)
                break
            elif c =='%':
                self.bitacora +=" ->estadoG->#K[%]\n"
                #mandar al estado K
                self.estadoK(posActual,fin, consola)
                
            elif c.isalpha():
                self.addToken(Tipo.NUMERO, self.lexema)
                self.lexema = ""
                self.posicionCar = posActual
                break
            # estadoG -> Error Lexico o manejar los hexadecimales
            else:
                self.bitacora +=" ->estadoG->EE["+c+"]\n"
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")
            
            posActual += 1
    #-----------------------estado H
    def estadoH(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            self.bitacora +=" ->estadoH->H["+c+"]\n"

            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.COMENTARIO, self.lexema)
                self.lexema = ""
            
            posActual += 1

    #-----------------------estado I
    def estadoI(self, posActual, consola):
        c=self.cadena[posActual]
        
        if c == '"':
            self.bitacora +=" ->estadoE->#I[\"]\n"
            self.addToken(Tipo.COMILLAS, "\"")
            self.posicionCar += 1
            #for i in range(0,len(self.listaTokens)):
            #    valor = self.listaTokens[i].getValor()
            #    print(valor)
            

    #-----------------------estado J
    def estadoJ(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            

            if c.isnumeric():
                self.bitacora +=" ->estadoJ->#J["+c+"]\n"
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.NUMERO, self.lexema)
                    self.lexema = ""

            elif c.isalpha():
                self.addToken(Tipo.NUMERO, self.lexema)
                self.lexema = ""
                #self.posicionCar = posActual
                numero = self.posicionCar 
                resta= posActual
                num = numero - resta
                self.posicionCar += num
                break

            elif c =='%':
                self.bitacora +=" ->estadoJ->#K[%]\n"
                #mandar al estado K
                self.estadoK(posActual,fin, consola)

            # estadoG -> Error Lexico o manejar los hexadecimales
            else:
                self.bitacora +=" ->estadoJ->EE["+c+"]\n"
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")


            posActual += 1

    #-----------------------estado K
    def estadoK(self, posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            if c == '%':
                
                self.addToken(Tipo.PORCENTAJE , "%")
                if(posActual+1 == fin):
                    self.addToken(Tipo.NUMERO, self.lexema)
                    self.lexema = ""
            
            else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")


            posActual += 1

    #-----------------------estado L
    def estadoL(self, posActual, consola):
        if(posActual+1 < len(self.cadena)-1):
            c=self.cadena[posActual+1]
            
            if c == '*':
                self.bitacora +=" ->estadoH->L[*]\n"
                self.addToken(Tipo.ASTERISCO, "*")
                self.posicionCar += 1
                self.estadoM(self.posicionCar, consola)
            else:
                self.bitacora +=" ->estadoH->EE["+c+"]\n"
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, "Error, No se terminan los comentarios con */")
                print("Error, No se terminan los comentarios con */")
                consola.insert('1.0', "Error, No se terminan los comentarios con */")

        

    #-----------------------estado M
    def estadoM(self, posActual, consola):
        c=self.cadena[posActual]
        
        if c== '/':
            self.bitacora +=" ->estadoL->#M[/]\n"
            self.addToken(Tipo.DIAGONAL, "/")
            self.posicionCar += 1
            c=self.cadena[self.posicionCar]
            if c=="\n":
                    self.fila += 1
           # for i in range(0,len(self.listaTokens)):
           #    valor = self.listaTokens[i].getValor()
           #   print(valor)
        else:
            self.bitacora +=" ->estadoH->EE["+c+"]\n"
            self.pos_errores.append(posActual)
            self.addError(self.columna,self.fila, "Error, No se terminan los comentarios con */")
            print("Error, No se terminan los comentarios con */")
            consola.insert('1.0', "Error, No se terminan los comentarios con */")
            
        

    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i] == " " or self.cadena[i] == "{" or self.cadena[i] == "}" or self.cadena[i] == "(" or self.cadena[i] == ")" or self.cadena[i] == "," or self.cadena[i] == ";" or self.cadena[i] == ":"or self.cadena[i] == "\"" or self.cadena[i] == "'"or self.cadena[i] == "\n" or self.cadena[i] == "\t" or self.cadena[i] == "\r":# or self.entrada[i] == "$":
                if self.cadena[i]=="\n":
                    self.fila += 1
                break
            longitud+=1
        return longitud

    def getSizeComentario(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i]=="\n":
                    self.fila += 1
            if self.cadena[i] == "*" and self.cadena[i+1] == "/":
                break
            longitud+=1
        return longitud

    def getSizeCadena(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i]=="\n":
                    self.fila += 1
            if self.cadena[i] == "\"" :
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

    def rutaDestino(self):
        cadenas= self.cadena.split("\n")
        for i in range(0, len(cadenas)):
            manejar = cadenas[i]
            if manejar.lower().find("pathw")>=0:
                print(manejar.lower().find("pathw"))
                path=manejar.split(' ')
                for o in range(0, len(path)):
                    if path[o].lower().find("c")>=0:
                        if path[o].lower().find("pathw")>=0:
                            pathDef=path[o].lower().split("pathw:")
                            self.rutaDestino1=pathDef[1]
                            return pathDef[1]
                        self.rutaDestino1=path[o]
                        return path[o]
                
        

    def reservadas(self, palabra):
        if palabra.lower() =="color":
            self.addToken(Tipo.COLOR , "color")
            #print("paso por Color")
            return True
        elif palabra.lower() =="background-color":
            self.addToken(Tipo.BGCOLOR , "background-color")
            return True
        elif palabra.lower() =="background-image":
            self.addToken(Tipo.BGIMAGE , "background-image")
            return True
        elif palabra.lower() =="border":
            self.addToken(Tipo.BORDER , "border")
            return True
        elif palabra.lower() =="opacity":
            self.addToken(Tipo.OPACITY , "opacity")
            return True
        elif palabra.lower() =="background":
            self.addToken(Tipo.BG , "background")
            return True
        elif palabra.lower() =="text-align":
            self.addToken(Tipo.TEXTALIGN , "text-align")
            return True
        elif palabra.lower() =="font-family":
            self.addToken(Tipo.FONTFAMILY , "font-family")
            return True
        elif palabra.lower() =="font-style":
            self.addToken(Tipo.FONTSTYLE , "font-style")
            return True
        elif palabra.lower() =="font-wight":
            self.addToken(Tipo.FONTWEIGHT , "font-weight")
            return True
        elif palabra.lower() =="font-size":
            self.addToken(Tipo.FONTSIZE , "font-size")
            return True
        elif palabra.lower() =="font":
            self.addToken(Tipo.FONT , "font")
            return True
        elif palabra.lower() =="padding-left":
            self.addToken(Tipo.PADDINGL , "padding-left")
            return True
        elif palabra.lower() =="padding-right":
            self.addToken(Tipo.PADDINGR , "padding-right")
            return True
        elif palabra.lower() =="padding-bottom":
            self.addToken(Tipo.PADDINGB , "padding-bottom")
            return True
        elif palabra.lower() =="padding-top":
            self.addToken(Tipo.PADDINGT , "padding-top")
            return True
        elif palabra.lower() =="padding":
            self.addToken(Tipo.PADDING , "padding")
            return True
        elif palabra.lower() =="display":
            self.addToken(Tipo.DISPLAY , "display")
            return True
        elif palabra.lower() =="line-height":
            self.addToken(Tipo.LINEHEIGHT , "line-height")
            return True
        elif palabra.lower() =="width":
            self.addToken(Tipo.WIDTH , "width")
            return True
        elif palabra.lower() =="height":
            self.addToken(Tipo.HEIGHT , "height")
            return True
        elif palabra.lower() =="margin-top":
            self.addToken(Tipo.MARGINT , "margin-top")
            return True
        elif palabra.lower() =="margin-right":
            self.addToken(Tipo.MARGINR , "margin-right")
            return True
        elif palabra.lower() =="margin-bottom":
            self.addToken(Tipo.MARGINB , "margin-bottom")
            return True
        elif palabra.lower() =="margin-left":
            self.addToken(Tipo.MARGINL , "margin-left")
            return True
        elif palabra.lower() =="margin":
            self.addToken(Tipo.MARGIN , "margin")
            return True
        elif palabra.lower()=="border-style":
            self.addToken(Tipo.BORDERSTYLE , "border-style")
            return True
        elif palabra.lower() =="position":
            self.addToken(Tipo.POSITION , "position")
            return True
        elif palabra.lower() =="bottom":
            self.addToken(Tipo.BOTTOM , "bottom")
            return True
        elif palabra.lower() =="top":
            self.addToken(Tipo.TOP , "top")
            return True
        elif palabra.lower() =="right":
            self.addToken(Tipo.RIGHT , "right")
            return True
        elif palabra.lower() =="left":
            self.addToken(Tipo.LEFT , "left")
            return True
        elif palabra.lower() =="float":
            self.addToken(Tipo.FLOAT , "float")
            return True
        elif palabra.lower() =="clear":
            self.addToken(Tipo.CLEAR , "clear")
            return True
        elif palabra.lower() =="max-width":
            self.addToken(Tipo.MAXWIDTH , "max-width")
            return True
        elif palabra.lower() =="min-width":
            self.addToken(Tipo.MINWHIDTH , "min-width")
            return True
        elif palabra.lower() =="max-height":
            self.addToken(Tipo.MAXHEIGHT , "max-height")
            return True
        elif palabra.lower() =="min-height":
            self.addToken(Tipo.MINHEIGHT , "min-height")
            return True
        elif palabra.lower() =="px":
            self.addToken(Tipo.PX , "px")
            return True
        elif palabra.lower() =="em":
            self.addToken(Tipo.EM , "em")
            return True
        elif palabra.lower() =="vh":
            self.addToken(Tipo.VH , "vh")
            return True
        elif palabra.lower() =="vw":
            self.addToken(Tipo.VW , "vw")
            return True
        elif palabra.lower() =="in":
            self.addToken(Tipo.IN , "in")
            return True
        elif palabra.lower() =="cm":
            self.addToken(Tipo.CM , "cm")
            return True
        elif palabra.lower() =="mm":
            self.addToken(Tipo.MM , "mm")
            return True
        elif palabra.lower() =="pt":
            self.addToken(Tipo.PT , "pt")
            return True
        elif palabra.lower() =="pc":
            self.addToken(Tipo.PC , "pc")
            return True
        elif palabra.lower() =="rem":
            self.addToken(Tipo.REM , "rem")
            return True
        elif palabra.lower() =="url":
            self.addToken(Tipo.URL , "url")
            return True
        elif palabra.lower() =="content":
            self.addToken(Tipo.CONTENT, "content")
            return True
        else:
            return False

