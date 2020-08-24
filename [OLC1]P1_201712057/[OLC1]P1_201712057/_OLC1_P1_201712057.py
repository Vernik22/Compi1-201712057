
import tkinter

ventana = tkinter.Tk()
ventana.geometry("1000x600")

etiqueta = tkinter.Label(ventana, text= "Compi 1", bg = "red") # tambien puedo ponerle color al texto con otro parametro
#etiqueta.pack() el texto simpre esta arriba y centrado
etiqueta.pack(side=tkinter.BOTTOM) #aqui puedo mover el texto a cualquier parte de la ventana

#se tiene que definir la funcion antes de ponerla en el boton 
def saludo():
    print("hola")

#funcion con parametros 
def pers(nombre):
    print ("hola "+ nombre)
#boton
boton1 =tkinter.Button(ventana, text = "Aceptar", padx=60 , pady = 50 , command= saludo)
boton1.pack()

boton2 =tkinter.Button(ventana, text = "Personalizado", padx=60 , pady = 50 , command= lambda: pers("Vernik"))
boton2.pack()

#caja de texto
cajaTexto= tkinter.Entry(ventana)
cajaTexto.pack()

def tx():
    entrada= cajaTexto.get()
    print(entrada)

boton3 =tkinter.Button(ventana, text = "Texto Caja", padx=60 , pady = 50 , command=tx)
boton3.pack()


#es mejor el metodo grid para colocar lascosas en la ventana
ventana.mainloop()