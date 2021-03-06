import prestamos
import titanic
import votos
import numpy as np
import math
import copy




def calculaNumeroElementos(distribucion):
    '''Calcula el numero de elementos de cada clase'''
    numero = 0
    for elem in distribucion.values():
        numero += elem
    return numero



def aprendizajeArbolesDecision(conjuntoInicio, atributos, clases, funcionClasificacion, atributosSeleccionados=None, cotaMinima=0, cotaMayoria=1):
    '''Metodo para aprender un arbol'''
    #conjuntoActual y atributosRestantes son listas de indices
    conjuntoActual = list(range(len(conjuntoInicio)))
    atributosRestantes = list(range(len(atributos)))
    
    if atributosSeleccionados == None:
        atributosRestantes = list(range(len(atributos)))
    else:
        atributosRestantes = atributosSeleccionados
        
    nodo = aprendizajeRecursivo(conjuntoInicio, atributos,clases, cotaMinima, cotaMayoria, funcionClasificacion, conjuntoActual,atributosRestantes)
           
    return nodo
    


def aprendizajeRecursivo(conjuntoInicio, atributos,clases, cotaMinima, cotaMayoria, funcionClasificacion, conjuntoActual, atributosRestantes):
    '''Llamada recursiva para aprender un arbol, recibe adicionalmente los parametros conjuntoActual y atributosRestantes que
    indican los elementos restantes del conjunto de entrenamiento y los atributos que quedan por escoger'''
    # Crear parametro para almacenar la clase del nodo anterior y pasarsela al nodo hoja cuando no hay mas elementos, compruebaCasoBase=0
    # Si es caso base se construye un nodo hoja
    
    instanciasClaseMaxima = calculaDistribucion(conjuntoInicio, conjuntoActual,clases)
    claseMaxima = max(instanciasClaseMaxima, key=instanciasClaseMaxima.get)
    if compruebaCasoBase(clases,conjuntoInicio, conjuntoActual, atributosRestantes, cotaMinima, cotaMayoria ) == 1:
        
        if len(conjuntoActual) == 1: # Nodo hoja
            nodo1 = NodoDT(distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases),
                              atributo=None,
                              ramas=None,
                              clase=conjuntoInicio[conjuntoActual[0]][len(conjuntoInicio[conjuntoActual[0]])-1])
            
            distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases)
            atributo=None
            ramas=None
            clase=conjuntoInicio[conjuntoActual[0]][len(conjuntoInicio[conjuntoActual[0]])-1]
            
            # Como solo nos queda un elemento nos quedamos con su clase
            '''
            print ("nodo1:" + "distribucion: " + str(distr) + " -atributo: " + str(atributo ) + " -ramas: " + str(ramas) + 
                       " -clase:" + str(clase))
            '''
            return nodo1
        
        else: # Nodo hoja
            nodo2 = NodoDT(distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases),
                                   atributo=None,
                                   ramas=None,
                                   clase=claseMaxima)
            
            distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases)
            atributo=None
            ramas=None
            clase=claseMaxima
            
            # En otro caso nos quedamos con la mayoria de la clase de los elementos que queden
            '''
            print ("nodo2:" + "distribucion: " + str(distr) + " -atributo: " + str(atributo ) + " -ramas: " + str(ramas) + 
                       " -clase:" + str(clase))
            '''
            return nodo2
            
    else:
        dicRamas = {}
        
        # Si no es caso base se elige el mejor atributo atr(mejor atributo) usando la funcion clasifica(funcionClasificacion), dentro se ponen los distintos sumatorios de Entropia y los otros
        indiceMejorAtributo = obtenMejorAtributo(clases, conjuntoInicio, atributos, conjuntoActual, atributosRestantes, funcionClasificacion)
        #print("indiceMejor: " + str(indiceMejorAtributo))
        
         #Creamos el conjunto actual de cada una de las ramas
        for valor in atributos[indiceMejorAtributo][1]:
            nuevoConjuntoActual = []
            #print("valor: " + str(valor))
            
            for indice in conjuntoActual:
                datoEntrenamiento = conjuntoInicio[indice]
                if valor == datoEntrenamiento[indiceMejorAtributo]:
                    nuevoConjuntoActual.append(indice)
            
            #print ("NuevoConjActual:" + str(nuevoConjuntoActual))
            
            #Creamos los atributos restantes de cada una de las ramas
            atribRestantes = copy.deepcopy(atributosRestantes)
            atribRestantes.remove(indiceMejorAtributo)
            
            if len(nuevoConjuntoActual) > 0:
                dicRamas[valor] = aprendizajeRecursivo(conjuntoInicio, atributos,clases, cotaMinima, cotaMayoria, funcionClasificacion, nuevoConjuntoActual, atribRestantes)
                
            #print("atributosDespues:" + str(atributosRestantes) )
            #print("atributosRestantesDespues:" + str(atribRestantes) )
            
            # Se construye un nodo internmedio
            # No hacer llamadas recursivas sin ejemplos
            if len(nuevoConjuntoActual) == 0: # Nodo hoja
                claseMaxima = max(instanciasClaseMaxima, key=instanciasClaseMaxima.get)
                nodo3 = NodoDT(distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases),
                                   atributo=None,
                                   ramas=None,
                                   clase=claseMaxima)
                
                distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases)
                atributo=None
                ramas=None
                clase=claseMaxima
                
                #Si nos quedamos sin elementos creamos un nodo hoja
                '''
                print ("nodo3:" + "distribucion: " + str(distr) + " -atributo: " + str(atributo ) + " -ramas: " + str(ramas) + 
                       " -clase:" + str(clase))
                '''
                dicRamas[valor] = nodo3
        
        if len(dicRamas) > 0: # Nodo interno
            nodo4 = NodoDT(distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases),
                                   atributo=indiceMejorAtributo,
                                   ramas=dicRamas,
                                   clase=None)
            
            distr=calculaDistribucion(conjuntoInicio,conjuntoActual,clases)
            atributo=indiceMejorAtributo
            ramas=dicRamas
            clase=None
            
            # En este caso hacemos la llamada recursiva, para ir creando los nodos intermedios
            '''
            print ("nodo4:" + "distribucion: " + str(distr) + " -atributo: " + str(atributo ) + " -ramas: " + str(ramas) + 
                       " -clase:" + str(clase))
            '''
            
            return nodo4
            


def compruebaCasoBase(clases,conjuntoInicio, conjuntoActual, atributosRestantes, cotaMinima=0, cotaMayoria=1):
    '''Metodo para comprobar cuando estamos en un caso base dentro de la recursion'''
    casoBase = 0
    if len(conjuntoActual) > 0:
        primero = conjuntoInicio[conjuntoActual[0]][len(conjuntoInicio[conjuntoActual[0]])-1]
    
    # CASOS BASE:
    #  - Cuando todos los datos son de la misma clase
    for elem in conjuntoActual:
        
        datoEntrenamiento = conjuntoInicio[elem]
        valorClase = datoEntrenamiento[len(datoEntrenamiento) - 1]
        if valorClase == primero:
            casoBase = 1
            
        else:
            casoBase = 0
            break
    
    #  - Todos los elementos son muy pocos comparados con los que habia al principio
    elemsMin = len(conjuntoActual) / len(conjuntoInicio)
    if elemsMin < cotaMinima:
        casoBase = 1
    
    #  - Cuando la mayoria sean todos de la misma clase
    dicClase = calculaDistribucion(conjuntoInicio, conjuntoActual,clases)
    
    if len(conjuntoActual) > 0:  
        elemsMax = max(dicClase.values()) / len(conjuntoActual)
        if elemsMax > cotaMayoria:
            casoBase = 1
    #print (elemsMax)
        
    
    #CASOS EN LOS QUE SE HAN DE CREAR HOJAS:
    #   Si se queda el conjunto con un ejemplo se devuelve una hoja con la clase mayoritaria
    #   Si el conjunto está vacío se devuelve una hoja con la clase mayoritaria del nodo anterior
    if len(conjuntoActual) <= 1: 
        casoBase = 1
        
    # Si se queda sin atributos
    if len(atributosRestantes) == 0:
        casoBase = 1
    
    return casoBase



def calculaDistribucion(conjuntoInicio, conjuntoActual, clases):
    '''Calcula la distribucion de las clases y las almacena en un diccionario'''
    dicClases = {}
    for e in clases:
        dicClases[e] = 0
    
    for elem1 in conjuntoActual:
        
        datoEntrenamiento = conjuntoInicio[elem1]
        
        valorClase = datoEntrenamiento[len(datoEntrenamiento) - 1]
        dicClases[ valorClase ] += 1
    
    return dicClases



class NodoDT(object):
    def __init__(self,atributo=-1,distr=None,ramas=None,clase=None):
        self.distr=distr # Diccionario con el numero de ejemplos de cada clase
        self.atributo=atributo # Indice del atributo, solo para  nodos internos
        self.ramas=ramas # Diccionario con tantas claves como valores tenga el atributo (valor del atributo: nodo inferior)
        self.clase=clase # Solo para nodos hojas
        


def obtenMejorAtributo(clases, conjuntoInicio, atributos, conjuntoActual, atributosRestantes, funcionClasificacion):
    '''Funcion que nos devuelve el mejor atributo para seleccionar'''
    dic = calculaAtributoValores(clases,conjuntoInicio, atributos, conjuntoActual, atributosRestantes)
    
    # Calcular la impureza del nodo padre y restarla al sumatorio de ni/n * impureza de cada valor del atributo
    # Se hacen los sumatorios con los valores de cada atributo y quedarnos con el menor para "error"
    #Impureza del padre
    
    #print("CONJUNTOINICIO: " + str(conjuntoInicio))
    #print("ATRIBUTOSRESTANTES: " + str(atributosRestantes))
    if funcionClasificacion == "error":
        #impurezaPadre = 1 - pd/S
        
        distribucionClases = calculaDistribucion(conjuntoInicio, conjuntoActual, clases)
        pdPadre = sorted(distribucionClases.values())[len(distribucionClases) - 1]
        
        impurezaPadre = 1 - (pdPadre/len(conjuntoActual))
        
        tam = len(conjuntoActual)
        indiceAtributoMejor = 0
        valorErrorMinimo = 1.0
        for elem in atributosRestantes:
            error = 0.00
            #print(str(elem)) 
            for elem1 in dic[elem]:
                #print(str(elem1))
                    
                if dic[elem][elem1][0] > 0:
                    pd = dic[elem][elem1][1]
                    si = dic[elem][elem1][0]
                        
                    error += (si/tam)*(1 - (pd/si))
                      
            #print("atributo nuevo:"+str(error))
            
            impurezaTotalAtributo = impurezaPadre - error
            if impurezaTotalAtributo < valorErrorMinimo:
                valorErrorMinimo = impurezaTotalAtributo
                indiceAtributoMejor = elem
                
        return indiceAtributoMejor
    
    # Mide lo organizados que están los datos dentro del conjunto
    elif funcionClasificacion == "gini":
        distribucionClases = calculaDistribucion(conjuntoInicio, conjuntoActual, clases)
        tam = len(conjuntoActual)
        #print ("distribucion:"+str(distribucionClases))
        pj = 0
       
        for clase in distribucionClases:
            pj += distribucionClases[clase]**2
            #print ("clase: " + str(distribucionClases[clase]))
       
        impurezaPadre = 1 - (pj/tam**2)
        #print ("impurezaPadre: " + str(impurezaPadre))
       
        indiceAtributoMasOrganizado = 0
        valorOrganizacionMinimo = 1.0
        for elem in atributosRestantes:
            impurezasHijos = 0.0
            
            for valor in atributos[elem][1]:
                conjuntoHijo = []
                
                for persona in conjuntoActual:
                    if valor in conjuntoInicio[persona]:
                        conjuntoHijo.append( persona )
                #print ("conjuntoHijo:"+str(conjuntoHijo))
                distribucionHijo = calculaDistribucion(conjuntoInicio, conjuntoHijo, clases)
                #print(distribucionHijo)
                
                impurezaHijo = 0
                
                for clase in distribucionHijo:
                    valorClase = distribucionHijo[clase]
                    
                    if valorClase > 0:
                        pi = valorClase**2
                        si = len(clase)
                        impurezaHijo += (si/tam)*(1-(pi/tam**2))
               
                #print ("impurezaHijo: " + str(impurezaHijo))
                impurezasHijos += impurezaHijo
                
            impurezaTotalAtributo = impurezaPadre - impurezasHijos
            
            if impurezaTotalAtributo < valorOrganizacionMinimo:
                #print("errorMinimo"+str(impurezaTotalAtributo))
                valorOrganizacionMinimo = impurezaTotalAtributo
                indiceAtributoMasOrganizado = elem
       
        #print("indiceAtributoMasOrganizado: " + str(indiceAtributoMasOrganizado))
        return indiceAtributoMasOrganizado
    
    elif funcionClasificacion == "entropia":
        # Padre {'conceder': 6, 'no conceder': 2, 'estudiar': 7} --> - 6/15*log2(6/15) - 2/15*log2(2/15) - 7/15*log2(7/15)
        distribucionClases = calculaDistribucion(conjuntoInicio, conjuntoActual, clases)
        #print ("distribucion:" + str(distribucionClases))
        tam = len(conjuntoActual)
        
        impurezaPadre = 0
       
        for clase in distribucionClases:
            valorClase = distribucionClases[clase]
            if valorClase > 0:
                impurezaPadre -= ( (valorClase/len(conjuntoActual)) * (math.log(valorClase,2))/(tam) )
            #print ("clase: " + str(distribucionClases[clase]))
       
        #print ("impurezaPadre: " + str(impurezaPadre))
       
        indiceAtributoMejor = 0
        valorErrorMinimo = 1.0
        #print("atributosRestantes: "+str(atributosRestantes))
        for elem in atributosRestantes:
            #print("........................")
            #print ("indiceAtributo:" + str(elem))
            impurezasHijos = 0.0
            
            for valor in atributos[elem][1]:
                conjuntoHijo = []
                
                for persona in conjuntoActual:
                    if valor in conjuntoInicio[persona]:
                        conjuntoHijo.append( persona )
                #print ("conjuntoHijo:"+str(conjuntoHijo))
                distribucionHijo = calculaDistribucion(conjuntoInicio, conjuntoHijo, clases)
                #print(distribucionHijo)
                
                impurezaHijo = 0
                
                for clase in distribucionHijo:
                    valorClase = distribucionHijo[clase]
                    
                    if valorClase > 0:
                        impurezaHijo -= ( (valorClase/len(conjuntoHijo)) * (math.log(valorClase,2))/( len(conjuntoHijo) ) )
               
                #print ("impurezaHijo: " + str(impurezaHijo))
                impurezasHijos += impurezaHijo
                
            impurezaTotalAtributo = impurezaPadre - impurezasHijos
            
            if impurezaTotalAtributo < valorErrorMinimo:
                #print("errorMinimo"+str(impurezaTotalAtributo))
                valorErrorMinimo = impurezaTotalAtributo
                indiceAtributoMejor = elem
            
        return indiceAtributoMejor
    


def calculaAtributoValores(clases,conjuntoInicio, atributos, conjuntoActual, atributosRestantes):
    '''Metodo auxiliar para calcular de cada atributo cuantas veces aparece y cuantas de
    estas veces pertenece a la clase dominante'''
    diccionarioAtributosValores = {}
    contadorPosicion = 0
  
    dicClases = calculaDistribucion(conjuntoInicio, conjuntoActual,clases)
  
    claseMaxima = max(dicClases, key=dicClases.get)
  
    for atr in atributosRestantes:
        listaValoresAtributo = atributos[atr][1]
        dic = {}
      
        for atrVal in listaValoresAtributo:
            dic[atrVal] = [0,0]
      
        diccionarioAtributosValores[atributosRestantes[contadorPosicion]] = dic
        contadorPosicion += 1
        
    for entrada in conjuntoActual:
        contadorPosicion = 0
        datoEntrenamiento = conjuntoInicio[entrada]
        clase = datoEntrenamiento[len(datoEntrenamiento) - 1]
        
        todosIndices = list(range(len(atributos)))
        a = np.array(todosIndices)
        b = atributosRestantes
        
        res= list(a[b])
        
        c = np.array(datoEntrenamiento)
        d = res
        #print("-------")
        #print( str(list(c[d])))
        indicesAObtener = list(c[d])
        
        for elem in indicesAObtener:
        
            dic = diccionarioAtributosValores[atributosRestantes[contadorPosicion]]
            #print("diccionario: " + str(dic))
            #print("elem: " + str(elem))
            
            dic.get(elem, None)
            dic[elem][0] += 1
            
            if clase == claseMaxima:
                dic[elem][1] += 1
                
            contadorPosicion += 1
        
    #print(str(diccionarioAtributosValores))           
    return diccionarioAtributosValores



class Clasificador:
    def __init__(self,clasificacion,clases,atributos,atributosSeleccionados = None):
        self.clasificacion=clasificacion
        self.clases=clases
        self.atributos=atributos
        self.nodoRaiz=None
        self.atributosSeleccionados = atributosSeleccionados
        
    def entrena(self,entrenamiento,cotaMinima=0, cotaMayoria=1,validacion=None):
        self.nodoRaiz = aprendizajeArbolesDecision(entrenamiento, self.atributos, self.clases, "gini", self.atributosSeleccionados, cotaMinima, cotaMayoria)
    
    def clasifica(self, ejemplo):
        indiceAtributo = self.nodoRaiz.atributo
        res = obtenSubnodo(self.nodoRaiz,ejemplo[indiceAtributo],ejemplo)
        return res
        
    def evalua(self,prueba):
        aciertos = 0
        numTotal = len(prueba)
        
        for p in prueba:
            clasificacionArbol = self.clasifica(p)
            if clasificacionArbol == p[len(p) - 1]:
                aciertos = aciertos + 1
        
        rendimiento = aciertos/numTotal
        print("El rendimiento es: " + str(rendimiento))
        return rendimiento
                
    def imprime(self):
        arbol = imprimeRec(self.nodoRaiz,0,self.atributos)
        print(str(arbol))



def imprimeRec(nodo,contador,atributos):
    '''Metodo auxiliar para imprimir el arbol'''
    arbol = ''
    ramas = nodo.ramas
    arbol = arbol + "nodo" + str(contador) + ":" + "\n"
    contadorCopia = contador + 1
    
    if ramas != None:
        #print(atributos[nodo.atributo][0])
        arbol = arbol + "           atributo: " + atributos[nodo.atributo][0] +"\n"
        arbol = arbol + "           distribucion: " + imprimeDistribucion(nodo.distr) +"\n"
        subArbol = ''
        
        for rama in ramas:
            nodoSub = ramas[rama]
            arbol = arbol + subArbol +  "           rama: "+ str(rama) + ",nodo" +str(contadorCopia) + "\n"
            arbol = arbol + subArbol + imprimeRec (nodoSub,contadorCopia,atributos)
            
            
    else:
        arbol = arbol + "           clase: "+  str(nodo.clase) + "\n"
    
    return arbol



def imprimeDistribucion(distr):
    '''Metodo auxiliar para imprimir la distribucion de clases'''
    cadena = "{"
    for d in distr:
        cadena = cadena + str(d) + ":" + str(distr[d])+","
    cadena = cadena + "}"
    cadena = cadena.replace(",}", "}")
        
    return cadena



def obtenSubnodo(nodo,rama,ejemplo):
    '''Funcion auxliar para imprimir los subnodos'''
    ramas = nodo.ramas
    clase = ''
    
    indiceAtributo = nodo.atributo
    valorAtributo = ejemplo[indiceAtributo]
    if nodo.ramas != None:
            nuevoNodo = ramas[valorAtributo]
            
            indiceNuevoAtributo = nuevoNodo.atributo
            if indiceNuevoAtributo != None:
                
                valorNuevoAtributo = ejemplo[indiceNuevoAtributo]
                clase = obtenSubnodo(nuevoNodo,valorNuevoAtributo,ejemplo)
                
            else:
                clase = clase +  nuevoNodo.clase
    else:
        clase = clase +  nodo.clase
        
    return clase
    



#Titanic
print("-------------------")
#indicesAtributosTitanicSeleccionados =  [1,6,8]
#atributosSeleccionados = [titanic.atributos[i] for i in indicesAtributosTitanicSeleccionados]

clasificador1 = Clasificador("",titanic.clases,titanic.atributos,[1,3,9])
clasificador1.entrena(titanic.entrenamiento,cotaMinima=0, cotaMayoria=1)
clasificador1.imprime()
res = clasificador1.clasifica(["1","1st","Cardeza, Mrs James Warburton Martinez (Charlotte Wardle Drake)","adulto","Cherbourg","Germantown, Philadelphia, PA","B-51/3/5","17755 L512 6s","3","female"])
print("El valor de clasificacion para el ejemplo es: " + str(res))
clasificador1.evalua(titanic.prueba)


'''
#Votos
print("-------------------")
clasificador2 = Clasificador("",votos.clases,votos.atributos)
clasificador2.entrena(votos.entrenamiento,cotaMinima=0, cotaMayoria=1)
clasificador2.imprime()
res = clasificador2.clasifica(['n','s','s','s','s','s','n','n','n','s','s','n','s','s','n','n',])
print("El valor de clasificacion para el ejemplo es: " + str(res))
clasificador2.evalua(votos.prueba)
'''

'''
#Prestamos
print("-------------------")
clasificador3 = Clasificador("",prestamos.clases,prestamos.atributos)
clasificador3.entrena(prestamos.entrenamiento,cotaMinima=0, cotaMayoria=1)
clasificador3.imprime()
res = clasificador3.clasifica(['jubilado','ninguno','ninguna','uno','soltero','altos'])
print("El valor de clasificacion para el ejemplo es: " + str(res))
clasificador3.evalua(prestamos.prueba)'''