from Ambiente import *
from Objetos import *

def Promedio(elementos:list):
    total=0.0
    contador=0
    for elemento in elementos:
        total+=elemento
        contador+=1
    
    return total/contador

class ParametrosAmbiente():
    def __init__(self, tamannox, tamannoy, obstaculos, suciedad, ninnos, turnoscambio, tiporobot="Reactivo"):
        self.tamannox=tamannox
        self.tamannoy=tamannoy
        self.obstaculos=obstaculos
        self.suciedad=suciedad
        self.ninnos=ninnos
        self.turnoscambio=turnoscambio
        self.tiporobot=tiporobot

class Resultado():
    def __init__(self):
        self.limpiado=0
        self.despedido=0
        self.nada=0
        self.suciedadmedia=0.0

    def __init__(self, limpiado, despedido, nada, suciedadmedia):
        self.limpiado=limpiado
        self.despedido=despedido
        self.nada=nada
        self.suciedadmedia=suciedadmedia

    def cadena(self):
        return "Limpiados="+str(self.limpiado)+", Despedido="+str(self.despedido)+", Suciedad Media="+str(self.suciedadmedia)

if __name__ == "__main__":
    escenarios1=[
        ParametrosAmbiente(20, 20,0.1,0.1,10,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.3,0.1,10,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.5,0.1,10,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.1,0.1,20,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.3,0.1,20,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.1,0.2,20,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.1,0.3,10,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.1,0.1,40,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.2,0.0,40,10,"Reactivo"),
        ParametrosAmbiente(20, 20,0.1,0.1,80,10,"Reactivo")

    ]
    escenarios2=[
        ParametrosAmbiente(20, 20,0.1,0.1,10,10,"Semi"),
        ParametrosAmbiente(20, 20,0.3,0.1,10,10,"Semi"),
        ParametrosAmbiente(20, 20,0.5,0.1,10,10,"Semi"),
        ParametrosAmbiente(20, 20,0.1,0.1,20,10,"Semi"),
        ParametrosAmbiente(20, 20,0.3,0.1,20,10,"Semi"),
        ParametrosAmbiente(20, 20,0.1,0.2,20,10,"Semi"),
        ParametrosAmbiente(20, 20,0.1,0.3,10,10,"Semi"),
        ParametrosAmbiente(20, 20,0.1,0.1,40,10,"Semi"),
        ParametrosAmbiente(20, 20,0.2,0.0,40,10,"Semi"),
        ParametrosAmbiente(20, 20,0.1,0.1,80,10,"Semi"),
    ]
    resultados1=[]
    resultados2=[]
    for e in range(len(escenarios1)):
        esc1=escenarios1[e]
        esc2=escenarios2[e]
        tablero1=Ambiente.Ambiente(esc1.tamannox, esc1.tamannoy, esc1.obstaculos, esc1.suciedad, esc1.ninnos, esc1.turnoscambio,esc1.tiporobot)
        tablero2=Ambiente.Ambiente(esc2.tamannox, esc2.tamannoy, esc2.obstaculos, esc2.suciedad, esc2.ninnos, esc2.turnoscambio,esc2.tiporobot)
        suciedad1=[]
        suciedad2=[]
        correcto1=0
        despedido1=0
        termino1=0
        correcto2=0
        despedido2=0
        termino2=0
    #Escenario1
        for i in range(30):
            final1=tablero1.Simular()
            suciedad1.append(tablero1.PorcientoCasillasSucias())
            if final1 == None:
                termino1+=1
            elif final1:
                correcto1+=1
            else:
                despedido1+=1
            final2=tablero2.Simular()
            suciedad2.append(tablero2.PorcientoCasillasSucias())
            if final2 == None:
                termino2+=1
            elif final2:
                correcto2+=1
            else:
                despedido2+=1

        promedio1=Promedio(suciedad1)
        promedio2=Promedio(suciedad2)

        final1=Resultado(correcto1,despedido1,termino1, promedio1)
        final2=Resultado(correcto2,despedido2,termino2, promedio2)
        resultados1.append(final1)
        resultados2.append(final2)

    cadenas1=[]
    for x in resultados1:
        cadenas1.append(x.cadena())

    cadenas2=[]
    for x in resultados2:
        cadenas2.append(x.cadena())

    print("El primer robot se desempeñó:")
    print(cadenas1)
    print("El segundo robot se desempeñó:")
    print(cadenas2)