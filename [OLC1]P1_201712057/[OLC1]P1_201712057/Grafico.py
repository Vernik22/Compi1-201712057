from tkinter import * #ventana
from tkinter import Menu    #menu
from tkinter import filedialog      # filechooser
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box

class Grafico:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("1000x600")
        self.ventana.title(" [OLC1] Proyecto 1" )
        #self.ventana.configure(bg = '#73AB85')
        self.ventana.configure(bg = '#F5A903')

        self.menu = Menu(self.ventana)

        self.archivo_item = Menu(self.ventana)
        self.archivo_item.add_command(label="Abrir Archivo", command=self.abrir)
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
        self.txtConsola = Entry(self.ventana,width=10)

        self.txtEntrada = scrolledtext.ScrolledText(self.ventana, width=115,height=25)
        self.txtEntrada.place(x=12, y=20)
        
        self.ventana.mainloop()

    def abrir(self) :
        print("hello")

 
    
