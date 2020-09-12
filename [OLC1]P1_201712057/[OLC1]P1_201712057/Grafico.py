from tkinter import * #ventana
from tkinter import Menu    #menu
from tkinter import filedialog      # filechooser
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from AnalisisLexicoCss import ScannerCss
from AnalisisLexicoJs import ScannerJs

class Grafico:

    def __init__(self):
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
        self.archivo_item.add_command(label="Ejecutar Analisis", command=self.abrir)
        self.archivo_item.add_separator()
        self.archivo_item.add_command(label="Salir", command=self.ventana.destroy)

        self.errores_item = Menu(self.ventana)
        self.errores_item.add_command(label="Errores")
        self.errores_item.add_separator()
        self.errores_item.add_command(label="Tokens")

        self.reportes_item = Menu(self.ventana)
        self.reportes_item.add_command(label="Bitacora")
        self.reportes_item.add_separator()
        self.reportes_item.add_command(label="Arbol")
        self.reportes_item.add_separator()


        self.menu.add_cascade(label='Archivo' , menu=self.archivo_item)
        self.menu.add_cascade(label="Errores",menu=self.errores_item)
        self.menu.add_cascade(label="Reportes", menu=self.reportes_item)

        self.ventana.config(menu=self.menu)

        self.txtEntrada = Entry(self.ventana,width=10)
        self.labelEntrada = Label(self.ventana, text='Entrada',bg='#F5A903')
        self.txtConsola = Entry(self.ventana,width=10)
        self.labelConsola = Label(self.ventana,text='Consola',bg='#F5A903')

        self.txtEntrada = scrolledtext.ScrolledText(self.ventana, width=115,height=18)
        self.txtEntrada.place(x=12, y=20)
        self.labelEntrada.place(x=12, y=1)
        
        self.txtConsola = scrolledtext.ScrolledText(self.ventana, width=115,height=10)
        self.txtConsola.place(x=12, y=390)
        self.labelConsola.place(x=12, y=370 )

        self.analiButton = Button(self.ventana, text= 'Analizar', padx= 25, pady=12, bg= 'grey',fg='white', command = self.analisar)
        self.analiButton.place(x=455, y=335)

        self.ventana.mainloop()

    
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
        self.txtConsola.delete('1.0',END)
        entrada = self.txtEntrada.get('1.0', END)
        #scaner = ScannerCss()
        scaner = ScannerJs()
        retorno = scaner.estadoA(entrada, self.txtConsola)
        #self.txtConsola.delete('1.0',END)   
        self.txtConsola.insert(END,retorno)
        messagebox.showinfo('Proyecto-1', 'Analisis Finalizado')

    
        
    
    
