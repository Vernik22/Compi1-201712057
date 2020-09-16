from TokenHtml import Error
from TokenHtml import Token
from TokenHtml import Tipo
from tkinter import *
from ReporteHtml import reporteHtml
from CorreccionErrores import Correccion
import os

class ScannerHtml:
    listaTokens = list()
    listaErrores= list()
    pos_errores= ""
    posicionCar= 0
    fila= 1
    columna= 1
    lexema= ""
    rutaDestino1=""

    def __init__(self):
        self.listaErrores = list()
        self.listaTokens = list()
        self.pos_errores= list()
        lexema = ""
        posicionCar = 0
        fila= 1
        columna=1
        self.rutaDestino1=""

    def getFilas(self):
        return self.fila

    def borrarTokenYErrores(self):
        self.rutaDestino1=rutaDestino()
        if os.path.isfile(self.rutaDestino1+"Tokens.html"):
            os.remove(self.rutaDestino1+"Tokens.html")

        if os.path.isfile(self.rutaDestino1+"reporteErrores.html"):
            os.remove(self.rutaDestino1+"reporteErrores.html")

    #-------------------------------Estado A
    def estadoA(self,entrada,consola):
        self.cadena= entrada +"$"
        self.caracterActual= ""
        self.borrarTokenYErrores()
        while self.posicionCar < len(self.cadena):
            self.caracterActual = self.cadena[self.posicionCar]

            if self.caracterActual =="<":
                if self.cadena[self.posicionCar+1]=='!':
                    self.estadoE(self.posicionCar, consola)
                else:
                    self.addToken(Tipo.MENORQ,"<") 
            elif self.caracterActual ==">":
                self.addToken(Tipo.MAYORQ, ">")
                self.posicionCar +=1
                sizeCadena = self.getSizeCadena(self.posicionCar)
                self.estadoD(self.posicionCar, self.posicionCar+ sizeCadena, consola)
                self.posicionCar = self.posicionCar + sizeCadena 
                self.estadoF(self.posicionCar,consola)
            elif self.caracterActual == "/":
                self.addToken(Tipo.DIAGONAL, "/")
            elif self.caracterActual == "\"":
                self.addToken(Tipo.COMILLADOBLE, "\"")
                self.posicionCar +=1
                sizeCadena = self.getSizeCadena(self.posicionCar)
                self.estadoD(self.posicionCar, self.posicionCar+ sizeCadena, consola)
                self.posicionCar = self.posicionCar + sizeCadena
                self.estadoF(self.posicionCar,consola)
            elif self.caracterActual == "=":
                self.addToken(Tipo.ASIGNACION, "=")
            elif self.caracterActual == "-":
                self.addToken(Tipo.GUION, "-")
            elif self.caracterActual== "!":
                self.addToken(Tipo.ADMIRACION, "!")


            #estado A a estado B (Reservadas e IDs)
            elif self.caracterActual.isalpha():
                sizeLexema = self.getSizeLexema(self.posicionCar)
                self.estadoB(self.posicionCar,self.posicionCar+sizeLexema, consola)
                #self.reservadas(posicionCar, posicionCar+sizeLexema)
                self.posicionCar = self.posicionCar + sizeLexema -1

            
            
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
                        correccion.eliminarC(self.rutaDestino1,entrada,"html",self.pos_errores)
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
            correccion = Correccion()
            reporte.reporteEnHtml(self.listaErrores,self.rutaDestino1)
            reporte.vistaTokens(self.listaTokens,self.rutaDestino1)
            correccion.eliminarC(self.rutaDestino1,entrada,"html",self.pos_errores)
            return "La entrada que ingresaste fue: Exiten Errores Lexicos" 
        else:
            reporte.vistaTokens(self.listaTokens,self.rutaDestino1)
            return "La entrada que ingresaste fue:" + self.cadena + "\n Analisis Exitoso"

    #-------------------------------Estado B
    def estadoB(self, posActual, fin, consola):
        c= ''
        while posActual<fin:
            c=self.cadena[posActual]
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
            else:
                self.pos_errores.append(posActual)
                self.addError(self.columna,self.fila, c)
                print("Error Lexico: ", c)
                consola.insert('1.0', "Error Lexico: "+c+"\n")

            posActual +=1 

    #----------------------------Estado D
    def estadoD(self, posActual, fin ,consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.CADENA, self.lexema)
                self.lexema = ""
            
            posActual += 1

    #--------------------------Estado E

    def estadoE(self, posActual, consola):
        c=self.cadena[posActual+1]              
        if c == '!':
            self.addToken(Tipo.MENORQ, "<")
            self.addToken(Tipo.ADMIRACION, "!")
            self.posicionCar = posActual+2
            self.estadoG(self.posicionCar,consola)
        elif c.isalpha():
            sizeLexema = self.getSizeLexema(self.posicionCar)
            self.estadoB(self.posicionCar,self.posicionCar+sizeLexema, consola)
            #self.reservadas(posicionCar, posicionCar+sizeLexema)
            self.posicionCar = self.posicionCar + sizeLexema
        elif c=='/':
            self.addToken(Tipo.DIAGONAL, "/")
            self.posicionCar+=1
        else:
            self.pos_errores.append(posActual)
            self.addError(self.columna,self.fila, c)
            print("Error Lexico: ", c)
            consola.insert('1.0', "Error Lexico: "+c+"\n")
        

    #-------------------------Estado F
    def estadoF(self,posActual, consola):
        c= self.cadena[posActual]
        if c == '"':
            self.addToken(Tipo.COMILLADOBLE, "\"")
            self.posicionCar += 1
            #for i in range(0,len(self.listaTokens)):
            #    valor = self.listaTokens[i].getValor()
            #    print(valor)
        elif c=='<':
            self.addToken(Tipo.MENORQ, "<")
            self.posicionCar += 1
        
    #--------------------------Estado G
    def estadoG(self,posActual, consola):
        c= self.cadena[posActual]
        if c== '-':
            c= self.cadena[posActual+1]
            if c=='-':
                self.addToken(Tipo.GUION, "-")
                self.addToken(Tipo.GUION, "-")
                self.posicionCar = posActual+2
                sizeComentario= self.getSizeComentario(self.posicionCar)
                self.estadoI(self.posicionCar, self.posicionCar+sizeComentario, consola)
                self.posicionCar = self.posicionCar +sizeComentario
                #print("va a L con "+c)
                self.estadoJ(self.posicionCar, consola)

    #-----------------------Estado I
    def estadoI(self,posActual, fin, consola):
        c=''
        while posActual < fin:
            c= self.cadena[posActual]
            
            self.lexema +=c
            if(posActual+1 == fin):

                self.addToken(Tipo.COMENTARIO, self.lexema)
                self.lexema = ""
            
            posActual += 1
    
    #---------------------Estado J
    def estadoJ(self,posActual,consola):
        c= self.cadena[posActual]
        if c== '-':
            c= self.cadena[posActual+1]
            if c=='-':
                self.addToken(Tipo.GUION, "-")
                self.addToken(Tipo.GUION, "-")
                self.posicionCar = posActual+2
                c= self.cadena[self.posicionCar]
                if c=='>':
                    self.addToken(Tipo.MAYORQ, ">")
                    self.posicionCar +=1



    def getSizeComentario(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i]=="\n":
                self.fila += 1
            if self.cadena[i] == "-" and self.cadena[i+1] == "-" and self.cadena[i+2] == ">":
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
            elif self.cadena[i] == "<" and self.cadena[i+1] == "/":
                break
            longitud+=1
        return longitud

    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.cadena)-1):
            if self.cadena[i] == " "   or self.cadena[i] == "\"" or self.cadena[i] == "'" or self.cadena[i] == "=" or self.cadena[i] == "[" or self.cadena[i] == "]"   or self.cadena[i] == "<" or self.cadena[i] == ">" or self.cadena[i] == "!"  or self.cadena[i] == "\n" or self.cadena[i] == "\t" or self.cadena[i] == "\r":# or self.entrada[i] == "$":
                if self.cadena[i]=="\n":
                    self.fila += 1
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

    def reservadas(self,palabra):
        if palabra.lower() =="html":
            self.addToken(Tipo.HTML , "html")
            #print("paso por Color")
            return True
        elif palabra.lower() =="head":
            self.addToken(Tipo.HEAD , "head")
            return True
        elif palabra.lower() =="title":
            self.addToken(Tipo.TITLE , "title")
            return True
        elif palabra.lower() =="body":
            self.addToken(Tipo.BODY , "body")
            return True
        elif palabra.lower() =="h1":
            self.addToken(Tipo.H1 , "h1")
            return True
        elif palabra.lower() =="h2":
            self.addToken(Tipo.H2 , "h2")
            return True
        elif palabra.lower() =="h3":
            self.addToken(Tipo.H3 , "h3")
            return True
        elif palabra.lower() =="h4":
            self.addToken(Tipo.H4 , "h4")
            return True
        elif palabra.lower() =="h5":
            self.addToken(Tipo.H5 , "h5")
            return True
        elif palabra.lower() =="h6":
            self.addToken(Tipo.H6 , "h6")
            return True
        elif palabra.lower() =="p":
            self.addToken(Tipo.P , "p")
            return True
        elif palabra.lower() =="img":
            self.addToken(Tipo.IMG , "img")
            return True
        elif palabra.lower() =="src":
            self.addToken(Tipo.SRC , "src")
            return True
        elif palabra.lower() =="a":
            self.addToken(Tipo.A , "a")
            return True
        elif palabra.lower() =="href":
            self.addToken(Tipo.HREF , "href")
            return True
        elif palabra.lower() =="ul":
            self.addToken(Tipo.UL , "ul")
            return True
        elif palabra.lower() =="li":
            self.addToken(Tipo.LI , "li")
            return True
        elif palabra.lower() =="style":
            self.addToken(Tipo.STYLE , "style")
            return True
        elif palabra.lower() =="th":
            self.addToken(Tipo.TH , "th")
            return True
        elif palabra.lower() =="tr":
            self.addToken(Tipo.TR , "tr")
            return True
        elif palabra.lower() =="td":
            self.addToken(Tipo.TD , "td")
            return True
        elif palabra.lower() =="caption":
            self.addToken(Tipo.CAPTION , "caption")
            return True
        elif palabra.lower() =="col":
            self.addToken(Tipo.COL , "col")
            return True
        elif palabra.lower() =="thead":
            self.addToken(Tipo.THEAD , "thead")
            return True
        elif palabra.lower() =="tbody":
            self.addToken(Tipo.TBODY , "tbody")
            return True
        elif palabra.lower() =="tfoot":
            self.addToken(Tipo.TFOOT , "tfoot")
            return True
        elif palabra.lower() =="table":
            self.addToken(Tipo.TABLE , "table")
            return True
        elif palabra.lower() =="br":
            self.addToken(Tipo.BR , "br")
            return True
        elif palabra.lower() =="div":
            self.addToken(Tipo.DIV , "div")
            return True
        elif palabra.lower() =="strong":
            self.addToken(Tipo.STRONG , "strong")
            return True
        elif palabra.lower() =="ol":
            self.addToken(Tipo.OL , "ol")
            return True
        elif palabra.lower() =="span":
            self.addToken(Tipo.SPAN , "span")
            return True