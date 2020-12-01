from Objetos import *
import random
direcciones=[[1,0],[0,1],[-1,0],[0,-1]]
class Ambiente():
    def __init__(self, tamannox, tamannoy, obstaculos, suciedad, ninnos, turnoscambio, tiporobot="Reactivo"):
        self.tamannox=tamannox
        self.tamannoy=tamannoy
        self.obstaculos=int((tamannox*tamannoy-2*ninnos)*obstaculos)
        self.suciedadcant=int((tamannox*tamannoy-2*ninnos-self.obstaculos)*suciedad)
        self.cantNinnos=ninnos
        self.tablero={}
        self.robot=None
        self.corrales=[]
        self.ninnos=[]
        self.suciedad=[]
        self.turnoscambio=turnoscambio
        self.turnosFaltantes=turnoscambio
        self.GenerarTablero(tiporobot)
        self.turnoactual=0

    def Simular(self):
        for i in range(self.turnoscambio*100):
            resultado=self.ProximoTurno()
            if resultado!=None:
                return resultado
        return None

    def ProximoTurno(self):
        # self.ImprimirTablero(self.turnoactual)
        self.turnosFaltantes-=1
        self.robot.Actuar(self)
        for ninno in self.ninnos:
            ninno.ensucio=False
        for ninno in self.ninnos:
            ninno.Actuar(self)

        if self.ChequearDespedido():
            # print("El robot ha sido despedido")
            return False

        if self.ChequearFinLimpio():
            # print("El robot ha limpiado todo y guardado a los niños")
            return True

        if self.turnosFaltantes==0:
            self.Variar()
            self.turnosFaltantes=self.turnoscambio

        self.turnoactual+=1

        return None

    def ImprimirTablero(self, turno):
        print("Tablero en el turno "+str(turno))
        for i in range(self.tamannox):
            linea=""
            for e in range(self.tamannoy):
                if self.robot.posicionX == i and self.robot.posicionY == e:
                    linea+="R "
                elif not str(i)+"#"+str(e) in self.tablero.keys():
                    linea+="  "
                else:
                    linea+=self.tablero[str(i)+"#"+str(e)].tipo[0]+" "
            print(linea)

    def CasillasValidasCorrales(self):
        disponibles={}
        if len(self.corrales)==0:
            return self.CasillasVacias()
        else:
            for corral in self.corrales:
                for direccion in direcciones:
                    nuevaX=corral.posicionX+direccion[0]
                    nuevaY=corral.posicionY+direccion[1]
                    if nuevaX>=0 and nuevaY>=0 and nuevaX<self.tamannox and nuevaY<self.tamannoy and (not str(nuevaX)+"#"+str(nuevaY) in self.tablero.keys()):
                        disponibles[str(nuevaX)+"#"+str(nuevaY)]=[nuevaX, nuevaY]
        resultado=[]
        for a in disponibles.values():
            resultado.append(a)
        return resultado

    def CasillasVacias(self):
        vacias=[]
        for i in range(self.tamannox):
            for e in range(self.tamannoy):
                if not str(i)+"#"+str(e) in self.tablero.keys():
                    vacias.append([i,e])
        return vacias


    def GenerarCorrales(self, yaempezo=False):
        for i in range(self.cantNinnos):
            disponibles=self.CasillasValidasCorrales()
            elegido=random.randint(0,len(disponibles)-1)
            X=disponibles[elegido][0]
            Y=disponibles[elegido][1]
            corral=CasillaCorral(X,Y)
            self.corrales.append(corral)
            self.tablero[str(X)+"#"+str(Y)]=corral
        
        if yaempezo:
            self.LlenarCorrales()

    def LlenarCorrales(self):
        cantidad=self.cantNinnos-len(self.ninnos)
        if self.robot.ninno != None:
            cantidad-=1
        corralesvacios=self.corrales.copy()
        for i in range(cantidad):
            elegido=random.randint(0,len(corralesvacios)-1)
            corral=corralesvacios[elegido]
            corral.lleno=True
            corralesvacios.remove(corral)
        
        for corral in corralesvacios:
            corral.lleno=False


    def GenerarObstaculos(self):
        for i in range(self.obstaculos):
            vacias=self.CasillasVacias()
            elegido=random.randint(0,len(vacias)-1)
            X=vacias[elegido][0]
            Y=vacias[elegido][1]
            obstaculo=Obstaculo()
            self.tablero[str(X)+"#"+str(Y)]=obstaculo

    def GenerarNinnos(self, yaempezo=False):
        contador=self.cantNinnos
        if yaempezo:
            contador=len(self.ninnos)
            # if self.robot.ninno!=None:
            #     contador+=1
            self.ninnos=[]
        for i in range(contador):
            vacias=self.CasillasVacias()
            elegido=random.randint(0,len(vacias)-1)
            X=vacias[elegido][0]
            Y=vacias[elegido][1]
            ninno=Ninno(X,Y)
            self.ninnos.append(ninno)
            self.tablero[str(X)+"#"+str(Y)]=ninno

    def GenerarSuciedad(self):
        for i in range(self.suciedadcant):
            vacias=self.CasillasVacias()
            elegido=random.randint(0,len(vacias)-1)
            X=vacias[elegido][0]
            Y=vacias[elegido][1]
            suciedad=Suciedad()
            self.suciedad.append(suciedad)
            self.tablero[str(X)+"#"+str(Y)]=suciedad

    def GenerarRobot(self, tipo:str ="Reactivo"):
        vacias=self.CasillasVacias()
        elegido=random.randint(0,len(vacias)-1)
        X=vacias[elegido][0]
        Y=vacias[elegido][1]
        if self.robot==None:
            if tipo == "Reactivo":
                self.robot=RobotReactivo(X,Y)
            elif tipo == "Semi":
                self.robot=RobotSemiReactivo(X,Y)
        else:
            self.robot.posicionX=X
            self.robot.posicionY=Y


    def GenerarTablero(self, tiporobot:str="Reactivo"):
        self.GenerarCorrales()
        self.GenerarNinnos()
        self.GenerarObstaculos()
        self.GenerarSuciedad()
        self.GenerarRobot(tiporobot)

    def Variar(self):
        self.tablero={}
        self.corrales=[]
        self.suciedad=[]
        self.GenerarCorrales(True)
        self.GenerarNinnos(True)
        self.GenerarObstaculos()
        self.GenerarSuciedad()
        vacias=self.CasillasVacias()
        elegido=random.randint(0,len(vacias)-1)
        X=vacias[elegido][0]
        Y=vacias[elegido][1]
        self.robot.posicionX=X
        self.robot.posicionY=Y

    def PorcientoCasillasSucias(self):
        casillasdisponibles=self.tamannox*self.tamannoy-self.cantNinnos-len(self.ninnos)-self.obstaculos
        return len(self.suciedad)*1.0/casillasdisponibles

    def ChequearDespedido(self):
        casillasdisponibles=self.tamannox*self.tamannoy-self.cantNinnos-len(self.ninnos)-self.obstaculos
        return len(self.suciedad)*1.0/casillasdisponibles>0.4

    def ChequearFinLimpio(self):
        return len(self.ninnos)==0 and self.robot.ninno==None and len(self.suciedad)==0
            