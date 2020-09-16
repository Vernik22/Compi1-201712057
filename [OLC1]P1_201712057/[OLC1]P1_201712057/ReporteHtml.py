import os

class reporteHtml:
    columna= 0
    fila = 0
    listaErrores= list()
    directorio= ""

    def __init__(self):
        self.columna=0
        self.fila=0
        self.listaErrores= list()
        directorio= ""

    def pathD(self,ruta):
        print(str(ruta))
        if not os.path.isdir(str(ruta)):
            os.makedirs(str(ruta))
            
    def reporteEnHtml(self, lista,ruta):
        self.pathD(ruta)
        self.listaErrores = lista 
        f = open(ruta+"/reporteErrores.html","w+")

        mensaje = """<html>

<head>
        <title>Reporte de Errores</title>
</head>

<body>
        <h1>Reporte de Errores</h1>
        <table border="3" class="egt">
                <tr>
                        <th scope="col">No</th>
                        <th scope="col">Fila</th>
                        <th scope="col">Columna</th>
                        <th scope="col">Descripcion</th>
                </tr>"""
        for i in range(0,len(self.listaErrores)):                                      
            mensaje+="""<tr>
            <td>"""+str(i)+"""</td>
            <td>"""+str(self.listaErrores[i].getFila())+"""</td>
            <td>"""+str(self.listaErrores[i].getColumna())+"""</td>
            <td>"""+str(self.listaErrores[i].getValor())+"""</td>
            </tr>"""
               
        mensaje += """
        </table>
</body>

</html>"""

        f.write(mensaje)
        f.close()


    def vistaTokens(self, lista,ruta):
        self.pathD(ruta)
        f = open(ruta+"/Tokens.html","w+")

        mensaje = """<html>

<head>
        <title>Reporte de Tokens</title>
</head>

<body>
        <h1>Reporte de Tokens</h1>
        <table border="3" class="egt">
                <tr>
                        <th scope="col">No</th>
                        <th scope="col">Tipo</th>
                        <th scope="col">Valor</th>                      
                </tr>"""
        for i in range(0,len(lista)):                                      
            mensaje+="""<tr>
            <td>"""+str(i)+"""</td>
            <td>"""+str(lista[i].getTipo())+"""</td>
            
            <td>"""+str(lista[i].getValor())+"""</td>
            </tr>"""
               
        mensaje += """
        </table>
</body>

</html>"""

        f.write(mensaje)
        f.close()


