import random 
from itertools import combinations 
import math 
import matplotlib.pyplot as plt

class Individuo():
    def __init__(self, X,Y,bino,dec):
        self.X = X
        self.Y = Y
        self.bino = bino
        self.dec = dec

    def __repr__(self):
        rep = 'Individuo(' + str(self.X) +' | '+ str(self.Y) + ' | ' + str(self.bino) +' | ' + str(self.dec) +')'
        return rep

class AlgoritmoGenetico():  

    def __init__(self, Xmin,Xmax, intervalo, rango, puntos, poblacionMaxima, poblacionInicial, generaciones,noBits, Pmi,Pmg):
        self.Xmin = Xmin
        self.intervalo = intervalo
        self.Xmax = Xmax
        self.rango = rango
        self.puntos = puntos
        self.poblacionInicial = poblacionInicial
        self.poblacionMaxima = poblacionMaxima
        self.generaciones = generaciones
        self.noBits = noBits
        self.individuos = []
        self.probabilidadDeCruce = .50
        self.Pmi = Pmi
        self.Pmg = Pmg
        

    def generarPoblacionInicial(self):
        individuos = []
        for i in range(0,self.poblacionInicial):
            binary = 0
            decimal = random.uniform(0,self.rango)
            binary = bin(int(decimal))
            binary = binary.removeprefix("0b")
            if(len(binary) < self.noBits):
                binary = binary.zfill(self.noBits)
            x = self.Xmin + (decimal * self.intervalo)
            self.individuos.append(Individuo(x,-1,binary,decimal))
        individuos = self.individuos 
        return individuos

    def posiblesParejas(self):
        parejas = []
        temp = combinations(self.individuos,2)
        for i in list(temp):
            parejas.append(i)
        return parejas


    def cruza(self,listParejas):
        listNewgen = []
        for i in range(len(listParejas)):
            probabilidadCruza = random.uniform(0.1,1.0)            
            if(probabilidadCruza <= self.probabilidadDeCruce):
                var = listParejas[i]
                for x in range(len(var)):
                    gen1 = var[0].bino
                    gen2 = var[1].bino
                # print('Gen1:',gen1)
                # print('Gen2:',gen2)
                div1 = gen1[:len(gen1)//2]
                div2 = gen2[len(gen2)//2:] 
                div3 = gen2[:len(gen2)//2]
                div4 = gen1[len(gen1)//2:]
                temp = div1 + div2
                temp2 = div3 + div4
                listNewgen.append(temp)
                listNewgen.append(temp2)

        # print('lista de nuevos G:', listNewgen)
        
        return listNewgen


    def mutacion(self, ListCruza):
        listNewInd = []
        listGenMutado= []
        bitAnalizador=[]
        i=0
        for i in range(len(ListCruza)):
            var = ListCruza[i]
            # print("Individuo seleccionado: ",ListCruza[i])
            pmir=random.random()
            # print("Su probabilidad es: ",pmir)
            if pmir <= self.Pmi:
                listNewInd.append(ListCruza[i])
            else:
                listGenMutado.append(ListCruza[i])
        for i in range(len(listNewInd)):
            bitAnalizador.append(listNewInd[i])
            var =bitAnalizador[i]
            var = list(var)
            for x in range(len(var)):
                # print("El bit a evaluar es: ",var[x])
                Pmgr = random.random()
                # print("Su probabilidad es :",Pmgr)
                if Pmgr <= self.Pmg:
                    if var[x] == "0":
                        var[x] = "1"
                    else:
                        var[x]==0
                        if var[x] == "1":
                            var[x]= "0"
                        else:
                            var[x]=="1"
                aux = "".join(var)
            listGenMutado.append(aux)
    
        return listGenMutado

    def ConvertirAObjetos(self,mutados):
        for i in range(0,len(mutados)):
            mutadoBinario = mutados[i]
            posicion = 0
            decimal = 0
            binario = mutadoBinario[::-1]            
            for digito in binario:
                # Elevar 2 a la posición actual
                multiplicador = 2**posicion
                decimal += float(digito) * multiplicador
                posicion += 1            
            x = self.Xmin + (decimal * self.intervalo)
            self.individuos.append(Individuo(x,-1,mutados[i],decimal))


    
    def calcularX(self):
        for elemento in self.individuos:
           elemento.X = self.Xmin + (elemento.dec *self.intervalo)
           
    def fx(self):
        dataAux =  []
        for i in range(len(self.individuos)):
            x = self.individuos[i].X
            op = float("{:.4f}".format(math.sin(math.radians(x))))
            op2 = float("{:.4f}".format(math.sqrt(2*(pow(x,2))-x-2)))
            if(op2 > 0): 
                resultado = float("{:.4f}".format(op * op2))
                self.individuos[i].Y = resultado
                dataAux.append(self.individuos[i])    
        self.individuos.clear()
        self.individuos = dataAux
        
    def limpiar(self):
        auxIndividuos = []
        # i = 0
        for i in range(len(self.individuos)):
            if(self.individuos[i].X <= self.Xmax):
                auxIndividuos.append(self.individuos[i])
        self.individuos.clear()
        self.individuos = auxIndividuos            
        # for elemento in self.individuos:
        #     if(elemento.X > self.Xmax):
        #         self.individuos.pop(i)
            # i += 1

    def poda(self):
        uniqueData = []
        self.individuos = sorted(self.individuos, key = lambda x: x.Y, reverse=True)
        if(len(self.individuos) > self.poblacionMaxima):
            while(len(self.individuos) > self.poblacionMaxima):
                self.individuos.pop()
        for individuo in self.individuos:
            if not any(I.bino == individuo.bino for I in uniqueData):
                uniqueData.append(individuo)
        self.individuos.clear()
        print(self.individuos)
        self.individuos = uniqueData



if __name__ == "__main__":
    print("Generaciones: ")
    generaciones = int(input()) 
    print("Población maxima")
    poblacionMaxima = int(input())
    poblacionInicial = random.randint(2,poblacionMaxima)
    print("Rango Maximo")
    xMaximo = float(input())
    print("Rango Minimo")
    xMinimo = float(input())
    print("Intervalo")
    intervalo = float(input())
    rango = xMaximo-xMinimo 
    puntos = (rango/intervalo)+1 
    bit= bin(int(puntos))
    bit=bit.removeprefix("0b")
    noBits= len(bit)
    print(noBits)
    print("Ingrese la probabilidad de mutación del inidividuo")
    Pmi= float(input())
    print("Ingrese la probabilidad de mutacion de gen")
    Pmg= float(input())

    ag = AlgoritmoGenetico(xMinimo, xMaximo, intervalo, rango, puntos, poblacionMaxima, poblacionInicial, generaciones, noBits, Pmi,Pmg)
    ag.generarPoblacionInicial()
    MejoresIndividuos = []
    MediaIndividuos = []
    PeoresIndividuos = []
    for i in range(0,generaciones):
        parejas = ag.posiblesParejas()
        hijos = ag.cruza(parejas)
        mutados = ag.mutacion(hijos)
        # print(ag.individuos) 
        # print("CONVERSION A OBJETVOS")
        ag.ConvertirAObjetos(mutados)
        # ag.individuos.extend(mutados)
        # print("______DESPUES______-")
        # print(ag.individuos)
        
        ag.calcularX()
        ag.fx()
        print("_______________________________ya_________________")
        print(ag.individuos)
        print("_______________________________ya2_________________")
        ag.limpiar()
        ag.poda()
        MejoresAptitudes = [individuo.Y for individuo in ag.individuos]
        MejoresIndividuos.append(max(MejoresAptitudes))
        aptitudes = [individuo.Y for individuo in ag.individuos]
        promedio = sum(aptitudes)/len(aptitudes)
        MediaIndividuos.append(promedio)
        peoresAptitudes = [individuo.Y for individuo in ag.individuos]
        PeoresIndividuos.append(min(peoresAptitudes))
        print(i)
        print("_____MEJORES_____\n" , MejoresIndividuos)
        print("______PROMEDIO_____\n", MediaIndividuos)
        print("_____PEOR_____\n", PeoresIndividuos)
        
        try:
            rmtree("assets")
        except:
            pass 
        os.makedirs("assets\Video", exist_ok=True)

        plt.plot(MejoresIndividuos, label="Mejor individuo", color="red", linestyle="-",)
        plt.plot(MediaIndividuos, label="Promedio", color="blue", linestyle="-",)
        plt.plot(PeoresIndividuos, label="Peor individuo", color="green", linestyle="-")
        plt.legend()
        os.makedirs("assets\Grafica", exist_ok=True)
        plt.savefig("assets\Grafica\GraficaHistorial.png")
        plt.close()
