"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 .
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Sorting import selectionsort as ins
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------


# Funciones para agregar informacion al catalogo
def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {'Accidents': None,
                'dateIndex': None,
                'timeIndex': None,
                }

    analyzer['Accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['timeIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo


def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['Accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    updateTimeIndex(analyzer['timeIndex'],accident)
    return analyzer
    
""" Inicio de Carga del arbol de Horas """

def updateTimeIndex(map, accident):
    
    ocurredtime = accident['Start_Time']
    ocurredtime = getTime(ocurredtime)
    entry = om.get(map, ocurredtime)
    if entry is None:
        datentry= newDataEntryTime(accident)
        om.put(map, ocurredtime, datentry)
    else:
        datentry = me.getValue(entry)
    addTimeIndex(datentry, accident)
    return map
    
def addTimeIndex(datentry, accident):
    
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    SeverityIndex = datentry['SeverityIndex']
    offentry = m.get(SeverityIndex, accident['Severity'])
    if (offentry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverity'], accident)
        m.put(SeverityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstseverity'], accident)
    
    return datentry
    
    

def getTime(ocurredtime):
    """Esta funcion aproxima el .datetime a una hora aproximada a la media hora anterior mas cercana 
    Hace el cambio de "YYYY-MM-DD HH:MM:SS" a "HH:MM"
    Si la hora es 10:25 lo aproxima a 10:00, si es 10:35 lo aproxima a 10:30"""
    
    a = datetime.datetime.strptime(ocurredtime, '%Y-%m-%d %H:%M:%S').time()
    time = datetime.time.isoformat(a)
    time = time[0:5]
    minutes = int(time[3:5])
    if minutes >= 30:
        minutes = "30"
    else:
        minutes = "00"
    time = time[0:3]
    time += minutes
    time = datetime.datetime.strptime(time,'%H:%M').time()
    return time

def newDataEntryTime(accident):
    entry = {'SeverityIndex': None, 'lstaccidents': None}
    entry['SeverityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry
    
"""Termina la carga del arbol de horas"""
##################################################
"""Inicio de la carga del arbol por fechas"""
def updateDateIndex(map, accident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de severidad y estados de accidentes.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza eel indice de severidad y estados de accidentes.
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    SeverityIndex = datentry['SeverityIndex']
    StateIndex = datentry['StateIndex']
    offentry = m.get(SeverityIndex, accident['Severity'])
    offentry1 = m.get(StateIndex, accident['State'])
    if (offentry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverity'], accident)
        m.put(SeverityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstseverity'], accident)
    if offentry1 is None:
        entry1 = newStateEntry(accident['State'])
        lt.addLast(entry1['lststate'], accident)
        m.put(StateIndex,accident['State'],entry1)
    else:
        entry1 = me.getValue(offentry1)
        lt.addLast(entry1['lststate'], accident)
    return datentry

def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'SeverityIndex': None,'StateIndex': None , 'lstaccidents': None}
    entry['SeverityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverity)
    entry['StateIndex'] = m.newMap(numelements=100,    #Mapa cuyas llaves son cada estado.
                                   maptype= 'PROBING',
                                   comparefunction= compareStates)
    
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newSeverityEntry(Severitygrp, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    entry = {'Severity': None, 'lstseverity': None}
    entry['Severity'] = Severitygrp
    entry['lstseverity'] = lt.newList('SINGLELINKED', compareSeverity)
    return entry
    
def newStateEntry(state):
    """
    Crea una entrada en el indice por cada estado.
    """
    entry = {"State": None, "lststate": None} #State es la llave, lststate son los accidentes en ese estado
    entry["State"] = state
    entry["lststate"] = lt.newList('SINGLELINKED', compareStates)
    return entry
    
"""Termina carga de arbol por fechas"""

# ==============================
# Funciones de consulta
# ==============================
def AccidentsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['Accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])

def listSize(lst):
    return lt.size(lst)

def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])


def getAccidentsByDate(analyzer, Date):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.get(analyzer['dateIndex'], Date)
    return lst

def getAccidentsBySeverity(analyzer, Date, Severity):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    Date = om.get(analyzer['dateIndex'], Date)
    try:
        if Date['key'] is not None:
            Severitymap = me.getValue(Date)['SeverityIndex']
            numseverity = m.get(Severitymap, str(Severity))
            if numseverity is not None:
                return m.size(me.getValue(numseverity)['lstseverity'])
            return 0
    except:
        return 0
        
"""Inicio de Requerimento 4"""
        
def getAccidentsByRange(analyzer,initialDate,finalDate):
    """
    Retorna una 'estructura' con los crimenes dentro de un rango
    """
    
    lst = om.keys(analyzer["dateIndex"], initialDate, finalDate)
    lstiterator = it.newIterator(lst)
    most_accidents_date = lt.getElement(lst,1)
    
    states_count = lt.newList("ARRAY_LIST", compareCount) 
    checklist = lt.newList("ARRAY_LIST", compareNames) 
    
    while it.hasNext(lstiterator):
        date = it.next(lstiterator)
        mapdate = om.get(analyzer["dateIndex"],date)
        map = me.getValue(mapdate)
        accidents = map["lstaccidents"]
        if lt.size(accidents) > lt.size((me.getValue(om.get(analyzer["dateIndex"],most_accidents_date)))["lstaccidents"]):
            most_accidents_date = date
        statemap = map["StateIndex"]
        count_states(statemap,states_count,checklist)
        
    ins.selectionSort(states_count,greater_function)
    
    return (lt.getElement(states_count,1), most_accidents_date)

def greater_function(element1,element2):
    if element1["Count"] > element2["Count"]:
        return True
    else:
        return False
        
def count_states(statemap, list, checklist):
        states = m.keySet(statemap)
        ite = it.newIterator(states)
        while it.hasNext(ite):
            state = it.next(ite)
            pos = lt.isPresent(checklist,state)
            if pos == 0:
                newStateNumber = newStateCount(state)
                lt.addLast(list,newStateNumber)
                lt.addLast(checklist,state)
            stateNumber = lt.getElement(list, pos)
            stateNumber["Count"] += lt.size((me.getValue(m.get(statemap, state)))["lststate"])
            
def newStateCount(state):
    return {"State": state, "Count": 0}
    

"""Fin del requerimento 4"""

#Requerimento 5
def getAccidentsByTime(analyzer, initialTime, finalTime):
    
    initialTime = getTime(initialTime)
    finalTime = getTime(finalTime)
    
    lst = om.values(analyzer["timeIndex"], initialTime,finalTime)
    lstiterator = it.newIterator(lst)
    sev_1 = 0
    sev_2 = 0
    sev_3 = 0
    sev_4 = 0
    while it.hasNext(lstiterator):
        map = it.next(lstiterator)
        accidents = map["SeverityIndex"]
        if m.get(accidents,"1") is not None:
            sev_1 += lt.size(me.getValue(m.get(accidents,"1"))["lstseverity"])
        if m.get(accidents,"2") is not None:
            sev_2 += lt.size(me.getValue(m.get(accidents,"2"))["lstseverity"])
        if m.get(accidents,"3") is not None:
            sev_3 += lt.size(me.getValue(m.get(accidents,"3"))["lstseverity"])
        if m.get(accidents,"4") is not None:
            sev_4 += lt.size(me.getValue(m.get(accidents,"4"))["lstseverity"])
    return [sev_1,sev_2,sev_3,sev_4] 
        

# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareSeverity(severity1, severity2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    severity1 = int(severity1)
    severity=int(me.getKey(severity2))
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1
        
def compareStates(state1,state2):
    state = me.getKey(state2)
    if state1 == state:
        return 0
    elif state1 > state:
        return 1
    else:
        return -1

def compareCount(element1, element2):
    if element1["Count"] == element2["Count"]:
        return 0
    elif element1["Count"] > element2["Count"]:
        return 1
    else:
        return -1
        
def compareNames(element1,element2):
    if element1 == element2: 
        return 0
    elif element1 == element2:
        return 1
    else:
        return -1