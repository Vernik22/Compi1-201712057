from tkinter import *  #ventana
from tkinter import Menu    #menu
from tkinter import filedialog      # filechooser
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from tkinter import ttk             #combobox
from AnalisisLexicoCss import ScannerCss
from AnalisisLexicoJs import ScannerJs
from AnalisisLexicoHtml import ScannerHtml
from AnalisisLexicoRmt import ScannerRmt
from AnalisisSintacticoRmt import SintacticoRmt
from ReporteArbol import Rparbol
import webbrowser
import os
from EnumerarLineas import TextLineNumbers
from PIL import Image, ImageTk

class Grafico:
    bitacora=""
    filas=1
    rutaDestino=""
    grafoCadena=""
    grafoComentario=""
    grafoNumero=""
    def __init__(self):
        repBitacora=""
        rutaDestino=""
        grafoCadena=""
        grafoComentario=""
        grafoNumero=""
        self.ventana = Tk()
        self.ventana.geometry("1000x600")
        self.ventana.title(" [OLC1] Proyecto 1" )
        #self.ventana.configure(bg = '#73AB85')
        self.ventana.configure(bg = '#F5A903')

        self.menu = Menu(self.ventana)

        self.archivo_item = Menu(self.ventana)
        self.archivo_item.add_command(label="Nuevo", command=self.abrir)
        self.archivo_item.add_separator()
        self.archivo_item.add_command(label="Abrir", command=self.abrir)
        self.archivo_item.add_separator()
        self.archivo_item.add_command(label="Guardar", command=self.abrir)
        self.archivo_item.add_separator()
        self.archivo_item.add_command(label="Guardar Como", command=self.abrir)
        self.archivo_item.add_separator()
        self.archivo_item.add_command(label="Ejecutar Analisis", command = self.analisar)
        self.archivo_item.add_separator()
        self.archivo_item.add_command(label="Salir", command=self.ventana.destroy)

        self.errores_item = Menu(self.ventana)
        self.errores_item.add_command(label="Errores", command = self.abrirErrores)
        self.errores_item.add_separator()
        self.errores_item.add_command(label="Tokens", command= self.abrirTokens)

        self.reportes_item = Menu(self.ventana)
        self.reportes_item.add_command(label="Bitacora", command= self.repBitacora)
        self.reportes_item.add_separator()
        self.reportes_item.add_command(label="Arbol", command=self.repoArbol)
        self.reportes_item.add_separator()


        self.menu.add_cascade(label='Archivo' , menu=self.archivo_item)
        self.menu.add_cascade(label="Errores",menu=self.errores_item)
        self.menu.add_cascade(label="Reportes", menu=self.reportes_item)

        self.ventana.config(menu=self.menu)

        self.txtEntrada = Entry(self.ventana,width=10)
        self.labelEntrada = Label(self.ventana, text='Entrada',bg='#F5A903')
        self.txtConsola = Entry(self.ventana,width=10)
        self.labelConsola = Label(self.ventana,text='Consola',bg='#F5A903')
        self.txtFilas = Entry(self.ventana, width=5 )
        #self.numberLines = TextLineNumbers(self.ventana, width=25,height=18, bg='#313335')
        #self.numberLines.attach(self.txtEntrada)
        #self.numberLines.pack(side=LEFT, fill=Y, padx=(5, 0))

        self.txtEntrada = scrolledtext.ScrolledText(self.ventana, width=112,height=18)
        self.txtEntrada.place(x=42, y=30)
        self.labelEntrada.place(x=20, y=1)

        #self.txtFilas = scrolledtext.ScrolledText(self.ventana,width=20, heigh= 18) 
        self.txtFilas.place(x=12, y= 30, width= 25 , height=293)
        self.txtConsola = scrolledtext.ScrolledText(self.ventana, width=70,height=10)
        self.txtConsola.place(x=12, y=390)
        self.labelConsola.place(x=12, y=370 )

        self.analiButton = Button(self.ventana, text= 'Analizar', padx= 25, pady=12, bg= 'grey',fg='white', command = self.analisar)
        self.analiButton.place(x=455, y=335)

        self.combo = ttk.Combobox(self.ventana,state="readonly",values= ["Elegir Lenguaje","Css","Js", "Html", "Rtm"] )
        self.combo.current(0)
        self.combo.place(x=455 ,y=3)

        

        #self.txtEntrada.bind("<Key>", self.onPressDelay)
        #self.txtEntrada.bind("<Button-1>", self.numberLines.redraw)
        #self.scrollbar.bind("<Button-1>", self.onScrollPress)
        #self.txtEntrada.bind("<MouseWheel>", self.onPressDelay)

        self.ventana.mainloop()

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def redraw(self):
        self.numberLines.redraw()

    def abrir(self) :
        self.txtEntrada.delete('1.0',END)           #Limpia el area de texto
        self.archivo = filedialog.askopenfilename(filetypes=[("Archivos Aceptados",".css .js .html .rmt"),("CSS","*.css"),("JavaScript","*.js"),("HTML",".html"),("Aritmetico JS",".rmt")]) #archivo es la Path
        if self.archivo != '':
            self.arch_open = open(self.archivo, 'r')    #se abre el archivo
            self.texto= self.arch_open.read()      #texto ya contiene todas las lineas de texto
            self.txtEntrada.insert(END,self.texto)
            self.arch_open.close()
        
        #self.arch_open.seek(0)      #pone el puntero de nuevo en el inicio
        #print(self.texto)

    def analisar(self):
        valor= self.combo.get()
        self.txtConsola.delete('1.0',END)
        entrada = self.txtEntrada.get('1.0', END)
        if valor.lower() =="css":
            scaner = ScannerCss()
            retorno = scaner.estadoA(entrada, self.txtConsola)
            self.bitacora = scaner.reporteBitacora()
            self.filas= scaner.getFilas()
            self.llenarFilas()
            self.rutaDestino=scaner.rutaDestino()
            self.pathD(self.rutaDestino)
            self.txtConsola.insert(END,retorno)
            messagebox.showinfo('Proyecto-1', 'Analisis Finalizado')
        elif valor.lower() =="js":
            scaner = ScannerJs()
            retorno = scaner.estadoA(entrada, self.txtConsola)
            fila= scaner.getFilas()
            self.rutaDestino=scaner.rutaDestino()
            self.grafoCadena= scaner.getPrimerCadena()
            self.grafoComentario= scaner.getPrimerComentario()
            self.grafoNumero= scaner.getPrimerNumero()
            self.pathD(self.rutaDestino)
            self.txtConsola.insert(END,retorno)
            messagebox.showinfo('Proyecto-1', 'Analisis Finalizado')
        elif valor.lower() =="html":
            scaner = ScannerHtml()
            retorno = scaner.estadoA(entrada, self.txtConsola)
            fila= scaner.getFilas()
            self.rutaDestino=scaner.rutaDestino()
            self.pathD(self.rutaDestino)
            self.txtConsola.insert(END,retorno)
            messagebox.showinfo('Proyecto-1', 'Analisis Finalizado')
        elif valor.lower()=="rtm":
            scaner = ScannerRmt()
            retorno = scaner.estadoA(entrada, self.txtConsola)
            self.txtConsola.insert(END,retorno)
            listaTokens= scaner.getListaToken()
            sintactic = SintacticoRmt(listaTokens)
            sintactic.E()
            errores = sintactic.getErrores()
            if len(errores)== 0:
                self.txtConsola.insert(END,"\nSintactico Correcto")
            else:
                self.txtConsola.insert(END,"\nSintactico Incorrecto")
            messagebox.showinfo('Proyecto-1', 'Analisis Finalizado')

    def repBitacora(self):
        self.txtConsola.insert(END,"\n ************************-REPORTE BITACORA-*********************\n")
        self.txtConsola.insert(END,self.bitacora)

    def abrirTokens(self):
        if os.path.isfile(self.rutaDestino+"/Tokens.html"):
            nombreArchivo = self.rutaDestino+"/Tokens.html"
            webbrowser.open_new_tab(nombreArchivo)
       
    def abrirErrores(self):
        if os.path.isfile(self.rutaDestino+"/reporteErrores.html"):
            nombreArchivo = self.rutaDestino+"/reporteErrores.html"
            webbrowser.open_new_tab(nombreArchivo)

    def pathD(self,ruta):
        print(str(ruta))
        if not os.path.isdir(str(ruta)):
            os.makedirs(str(ruta))

    def llenarFilas(self):
        for i in range(0,self.filas):
            self.txtFilas.insert("0",str(i+1)+"\n")

    def repoArbol(self):
        if os.path.isdir(self.rutaDestino):
            arbol= Rparbol()
            #arbol.graficar()
            cadenaGrafo= self.grafoCadena+ " "+self.grafoComentario+" "+self.grafoNumero
            arbol.comando(self.rutaDestino,cadenaGrafo,"reporteArbol")
            #arbol.comando(self.rutaDestino,self.grafoComentario,"primerComentario")
            #arbol.comando(self.rutaDestino,self.grafoNumero,"primerNumero")
            self.abrirImagen("reporteArbol")
            #self.abrirImagen("primerComentario")
            #self.abrirImagen("primerNumero")
        
    def abrirImagen(self, img):
        if os.path.isfile(self.rutaDestino+"/"+img+".png"):
            ruta=(self.rutaDestino+"/"+img+".png")
            im= Image.open(ruta)
            im.show()

            #im = PhotoImage(file=ruta)
            #widget = self.labelImg(self.ventana, image=im).pack()

            #im = im.resize((400, 260), Image.ANTIALIAS)
            #im = ImageTk.PhotoImage(im)
            #self.labelImg.config(image=im)
            
            o_size=im.size
            f_size=(450,230)
            factor = min(float(f_size[1])/o_size[1], float(f_size[0])/o_size[0])
            width = int(o_size[0] * factor)
            height = int(o_size[1] * factor)
            rImg= im.resize((width, height), Image.ANTIALIAS)
            rImg = ImageTk.PhotoImage(rImg)
            lblImage=Label(self.ventana,image=rImg).place(x=610,y=370)
            self.ventana.mainloop()

            

                            