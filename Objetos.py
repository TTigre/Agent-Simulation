import Ambiente
import heapq
import random

direcciones=[[1,0],[0,1],[-1,0],[0,-1]]
cuadricula=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
class ObjetoSimulacion():
    pass

class ElementoActivo(ObjetoSimulacion):
    def Actuar(self, ambiente:Ambiente):
        pass

class PosicionConDistancia():
    def __init__(self, X, Y, distancia, anterior=None):
        self.X=X
        self.Y=Y
        self.distancia=distancia
        self.anterior=anterior
    
    def __lt__(self, next):
        return self.distancia<next.distancia

class Robot(ElementoActivo):
    def __init__(self, posicionX, posicionY):
        self.posicionX=posicionX
        self.posicionY=posicionY
        self.ninno=None
        self.tipo="Robot"

    def EncontrarMasCercano(self, ambiente:Ambiente, tipo:str):
        visitado={}
        posicionInicial=PosicionConDistancia(self.posicionX, self.posicionY, 0)
        visitado[str(self.posicionX)+"#"+str(self.posicionY)]=True
        heap=[posicionInicial]
        encontrado=False
        while(len(heap)>0):
            actual=heapq.heappop(heap)
            for dir in direcciones:
                nuevoX=actual.X+dir[0]
                nuevoY=actual.Y+dir[1]
                if nuevoX>=0 and nuevoY>=0 and nuevoX<ambiente.tamannox and nuevoY<ambiente.tamannoy and (not str(nuevoX)+"#"+str(nuevoY) in visitado.keys()):
                    nuevaPosicion=PosicionConDistancia(nuevoX, nuevoY, actual.distancia+1,actual)
                    
                    if str(nuevoX)+"#"+str(nuevoY) in ambiente.tablero.keys():
                        elemento=ambiente.tablero[str(nuevoX)+"#"+str(nuevoY)]
                        if elemento.tipo=="Obstaculo":
                            continue
                        if elemento.tipo=="Corral" and elemento.lleno:
                            continue
                        if elemento.tipo==tipo:
                            return nuevaPosicion

                    visitado[str(nuevoX)+"#"+str(nuevoY)]=True
                    heapq.heappush(heap,nuevaPosicion)
                    heapq.heapify(heap)
        return None

    def EncontrarProximoPaso(self, tamannopaso, posicionfinal:PosicionConDistancia):
        posiciones=[]
        posicionactual=posicionfinal
        while(posicionactual.anterior!=None):
            posiciones.append(posicionactual)
            posicionactual=posicionactual.anterior

        posiciones.reverse()
        if len(posiciones)>=tamannopaso:
            return posiciones[tamannopaso-1]
        elif len(posiciones)>0:
            return posiciones[len(posiciones)-1]
        else:
            return PosicionConDistancia(self.posicionX, self.posicionY, 0)

    def BuscaElementoYMuevete(self, ambiente:Ambiente, tipo:str):
        lugar=self.EncontrarMasCercano(ambiente, tipo)
        if lugar==None:
            return False
        tamannopaso=1
        if self.ninno!=None:
            tamannopaso=2
        posicionProxima=self.EncontrarProximoPaso(tamannopaso,lugar)
        if posicionProxima.X==self.posicionX and posicionProxima.Y==self.posicionY:
            return False
        self.posicionX=posicionProxima.X
        self.posicionY=posicionProxima.Y
        return True

    def AnalizaElemento(self, ambiente:Ambiente):
        elemento=None
        if str(self.posicionX)+"#"+str(self.posicionY) in ambiente.tablero.keys():
                elemento=ambiente.tablero[str(self.posicionX)+"#"+str(self.posicionY)]
        return elemento
    
    def CargaNinno(self, ambiente:Ambiente):
        elemento=self.AnalizaElemento(ambiente)
        if elemento!=None and elemento.tipo=="Ninno" and self.ninno==None:
            self.ninno=elemento
            if self.ninno in ambiente.ninnos:
                ambiente.ninnos.remove(self.ninno)
            return True
        return False

    def Limpiar(self, ambiente:Ambiente):
        elemento=self.AnalizaElemento(ambiente)
        if elemento!=None and elemento.tipo=="Suciedad":
            ambiente.suciedad.remove(elemento)
            ambiente.suciedadcant-=1
            ambiente.tablero.pop(str(self.posicionX)+"#"+str(self.posicionY))
            return True
        return False

    def DepositarEnCorral(self, ambiente:Ambiente):
        elemento=self.AnalizaElemento(ambiente)
        if elemento!=None and elemento.tipo=="Corral" and self.ninno!=None:
            elemento.lleno=True
            self.ninno=None
            return True
        return False


class Suciedad(ObjetoSimulacion):
    def __init__(self):
        self.tipo="Suciedad"

class Obstaculo(ObjetoSimulacion):
    def __init__(self):
        self.tipo="Obstaculo"

    def Mover(self, ambiente:Ambiente,direccion, posicionX, posicionY):
        nuevaX=posicionX+direccion[0]
        nuevaY=posicionY+direccion[1]
        elemento=None
        if str(nuevaX)+"#"+str(nuevaY) in ambiente.tablero.keys():
            elemento=ambiente.tablero[str(nuevaX)+"#"+str(nuevaY)]
        
        if nuevaX<0 or nuevaY<0 or nuevaX>=ambiente.tamannox or nuevaY>=ambiente.tamannoy or (elemento!=None and elemento.tipo!="Obstaculo"):
            return False
        elif elemento!=None and elemento.tipo=="Obstaculo":
            resultado=elemento.Mover(ambiente,direccion,nuevaX,nuevaY)
            if not resultado:
                return False
        
        ambiente.tablero.pop(str(posicionX)+"#"+str(posicionY))
        ambiente.tablero[str(nuevaX)+"#"+str(nuevaY)]=self
        return True

        
        

class CasillaCorral(ObjetoSimulacion):
    def __init__(self, posicionX, posicionY):
        self.posicionX=posicionX
        self.posicionY=posicionY
        self.lleno=False
        self.tipo="Corral"

class Ninno(ElementoActivo):
    def __init__(self, posicionX, posicionY, movimientoAleatorio=0.3):
        self.posicionX=posicionX
        self.posicionY=posicionY
        self.ensucio=False
        self.tipo="Ninno"
        self.movimientoAleatorio=movimientoAleatorio

    def Actuar(self, ambiente:Ambiente):
        self.Mover(ambiente)
        self.Ensucia(ambiente)

    def ObtenerNinnosCuadricula(self, ambiente:Ambiente):
        ninnosSucios=[]
        if self.ensucio:
            return []

        for cambio in cuadricula:
            nuevaX=self.posicionX+cambio[0]
            nuevaY=self.posicionY+cambio[1]

            if nuevaX<0 or nuevaY<0 or nuevaX>=ambiente.tamannox or nuevaY>=ambiente.tamannoy:
                continue

            if str(nuevaX)+"#"+str(nuevaY) in ambiente.tablero.keys():
                elemento=ambiente.tablero[str(nuevaX)+"#"+str(nuevaY)]
                if elemento.tipo=="Ninno":
                    if not elemento.ensucio:
                        elemento.ensucio=True
                        ninnosSucios.append(elemento)
        ninnosSucios.append(self)
        return ninnosSucios

    def Mover(self, ambiente:Ambiente):
        direccionesposibles=[]
        for pos in direcciones:
            nuevaX=self.posicionX+pos[0]
            nuevaY=self.posicionY+pos[1]
            if nuevaX<0 or nuevaY<0 or nuevaX>=ambiente.tamannox or nuevaY>=ambiente.tamannoy:
                continue
            if str(nuevaX)+"#"+str(nuevaY) in ambiente.tablero.keys():
                elemento=ambiente.tablero[str(nuevaX)+"#"+str(nuevaY)]
                if elemento.tipo!="Obstaculo":
                    continue
                    # if not elemento.Mover(ambiente, pos, nuevaX, nuevaY):
                    #     continue
            elif str(nuevaX)+"#"+str(nuevaY) in ambiente.tablero.keys() or (ambiente.robot.posicionX==nuevaX and ambiente.robot.posicionY==nuevaY):
                continue
            direccionesposibles.append(pos)
        
        if random.random()<self.movimientoAleatorio and len(direccionesposibles)>0:
            elegido=random.randint(0, len(direccionesposibles)-1)
            direccion=direccionesposibles[elegido]
            nuevaX=self.posicionX+direccion[0]
            nuevaY=self.posicionY+direccion[1]
            elemento=None
            if str(nuevaX)+"#"+str(nuevaY) in ambiente.tablero.keys():
                elemento=ambiente.tablero[str(nuevaX)+"#"+str(nuevaY)]
                if elemento.tipo=="Obstaculo":
                    if not elemento.Mover(ambiente, direccion, nuevaX, nuevaY):
                        return
            ambiente.tablero.pop(str(self.posicionX)+"#"+str(self.posicionY))
            self.posicionX=nuevaX
            self.posicionY=nuevaY
            ambiente.tablero[str(self.posicionX)+"#"+str(self.posicionY)]=self

        return



    def Ensucia(self, ambiente:Ambiente):
        if self.ensucio:
            return
        ninnosSucios=self.ObtenerNinnosCuadricula(ambiente)
        cuadriculaslibres=[]
        for cambio in cuadricula:
            nuevaX=self.posicionX+cambio[0]
            nuevaY=self.posicionY+cambio[1]
            if nuevaX<0 or nuevaY<0 or nuevaX>=ambiente.tamannox or nuevaY>=ambiente.tamannoy:
                continue
            if not str(nuevaX)+"#"+str(nuevaY) in ambiente.tablero.keys():
                cuadriculaslibres.append(cambio)

        cantidARemover=min(len(cuadriculaslibres),int(3**(len(ninnosSucios)-1)))
        cantidARemover=random.randint(0,cantidARemover)
        if len(cuadriculaslibres)==0:
            return
        for i in range(cantidARemover):
            elegido=random.randint(0,len(cuadriculaslibres)-1)
            cambio=cuadriculaslibres[elegido]
            cuadriculaslibres.remove(cambio)
            nuevaX=self.posicionX+cambio[0]
            nuevaY=self.posicionY+cambio[1]
            sucio=Suciedad()
            ambiente.suciedad.append(sucio)
            ambiente.tablero[str(nuevaX)+"#"+str(nuevaY)]=sucio

        return


class RobotReactivo(Robot):
    def __init__(self, posicionX, posicionY):
        self.posicionX=posicionX
        self.posicionY=posicionY
        self.ninno=None
        self.tipo="Robot"

    def Actuar(self, ambiente:Ambiente):
        elemento=None
        if str(self.posicionX)+"#"+str(self.posicionY) in ambiente.tablero.keys():
            elemento=ambiente.tablero[str(self.posicionX)+"#"+str(self.posicionY)]
        
        if self.ninno != None:
            if self.DepositarEnCorral(ambiente):
                return

            if not self.BuscaElementoYMuevete(ambiente,"Corral"):
                if self.Limpiar(ambiente):
                    return
                else:
                    self.BuscaElementoYMuevete(ambiente,"Suciedad")
                    return
        elif len(ambiente.ninnos)>0:
            if self.BuscaElementoYMuevete(ambiente,"Ninno"):
                self.CargaNinno(ambiente)
            elif self.Limpiar(ambiente):
                    return
            else:
                self.BuscaElementoYMuevete(ambiente,"Suciedad")
        
        else:
            if self.Limpiar(ambiente):
                return
            self.BuscaElementoYMuevete(ambiente,"Suciedad")
                   

    # def AccionaCasillaActualDespuesMoverse(self, ambiente:Ambiente):
    #     if str(self.posicionX)+"#"+str(self.posicionY) in ambiente.tablero.keys():
    #         elemento=ambiente.tablero[str(self.posicionX)+"#"+str(self.posicionY)]
            
    #         elif elemento.tipo == "Ninno":
    #             if self.ninno != None:
    #                 return
    #             self.ninno=elemento
    #             ambiente.tablero.pop(str(self.posicionX)+"#"+str(self.posicionY))
    #             ambiente.ninnos.remove(self.ninno)
            
    #         elif elemento.tipo == "Corral":
    #             if self.ninno == None:
    #                 return
    #             elemento.lleno=True
    #             self.ninno=None

class RobotSemiReactivo(Robot):
    def __init__(self, posicionX, posicionY, probabilidadBuscarNinno=0.7):
        self.posicionX=posicionX
        self.posicionY=posicionY
        self.ninno=None
        self.probabilidadBuscarNinno=probabilidadBuscarNinno
        self.buscandoNinno=None
        self.tipo="Robot"

    def Actuar(self, ambiente:Ambiente):
        elemento=None
        if str(self.posicionX)+"#"+str(self.posicionY) in ambiente.tablero.keys():
            elemento=ambiente.tablero[str(self.posicionX)+"#"+str(self.posicionY)]
        
        if self.ninno == None:
            if self.buscandoNinno==None:
                if len(ambiente.ninnos)==0:
                    self.buscandoNinno=False
                elif random.random()<self.probabilidadBuscarNinno:
                    self.buscandoNinno=True
                else:
                    self.buscandoNinno=False

            if self.buscandoNinno:
                if self.BuscaElementoYMuevete(ambiente,"Ninno"):
                    self.CargaNinno(ambiente)
                elif self.Limpiar(ambiente):
                    return
                else:
                    self.BuscaElementoYMuevete(ambiente,"Suciedad")
            else:
                if self.Limpiar(ambiente):
                    self.buscandoNinno=None
                elif not self.BuscaElementoYMuevete(ambiente,"Suciedad"):
                    if self.BuscaElementoYMuevete(ambiente,"Ninno"):
                        self.CargaNinno(ambiente)

        else:
            if self.DepositarEnCorral(ambiente):
                return

            if not self.BuscaElementoYMuevete(ambiente,"Corral"):
                if self.Limpiar(ambiente):
                    return
                else:
                    self.BuscaElementoYMuevete(ambiente,"Suciedad")
                    return