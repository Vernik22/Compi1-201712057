import os

class Correccion:
    cadenaFinal=""
    pos_car=list()

    def __init__(self):
        self.cadena = ""
        self.pos_car= list()

    def eliminarC(self,ruta,cadena, extension,posiciones):
        recorrido = cadena
        posicionCar=0
        if len(posiciones)!= 0:

            while posicionCar < len(recorrido):

                for i in range(0, len(posiciones)-1):
                    if posiciones[i]==posicionCar:                
                        break
                else:
                    self.cadenaFinal+=recorrido[posicionCar]
            
            

                posicionCar+=1
        else:
            self.cadenaFinal=cadena
        self.crearArchivoFinal(ruta,extension)


    def crearArchivoFinal(self,ruta,extension):
        self.pathD(ruta)
        f = open(ruta+"/archivoCorregido."+extension,"w+")
         
        f.write(self.cadenaFinal)
        f.close()

    def pathD(self,ruta):
        print(str(ruta))
        if not os.path.isdir(str(ruta)):
            os.makedirs(str(ruta))

