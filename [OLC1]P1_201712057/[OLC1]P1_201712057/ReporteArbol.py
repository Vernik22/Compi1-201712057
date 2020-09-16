import subprocess



class Rparbol:
    variable=""
    def __init__(self):
        self.variable=""

    def comando(self,ruta,grafo,nombre):
        self.graficar(ruta,grafo,nombre)
        subprocess.call(['cd',ruta, '&&'  'dot', '-Tpng',  nombre+'.txt', '-o', nombre+'.png'],shell=True)
        
    def graficar(self,ruta,grafo,nombre):
        f = open(ruta+"/"+nombre+".txt","w+")
        mensaje= """ digraph G{"""
        mensaje+=str(grafo) 

        mensaje+="""}"""    
        f.write(mensaje)
        f.close()

       

    
        

       