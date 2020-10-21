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

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = 'us_accidents_small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Buscar Accidentes por Fecha")
    print("4- Buscar Accidentes antes de una Fecha")
    print("5- Buscar Accidentes en un Rango de Fechas")
    print("6- Buscar el Estado con más Accidentes en un Rango de Fechas")
    print("7- Conocer Accidentes en Rango de Horas")
    print("8- Conocer Accidentes cercanos a una Locación")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfile)
        print('Accidentes cargados: ' + str(controller.AccidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha: ")
        Date = input("Fecha (YYYY-MM-DD): ")
        dic = controller.getAccidentsByDate(cont, Date)
        total= dic[1]+dic[2] + dic[3]+ dic[4]
        if dic[1]==0 and dic[2]==0 and dic[3]==0 and dic[4]==0:
            print("\nNo se encontraron accidentes en esa fecha")
        else:
            print("\nEn la fecha seleccionada hubo un total de " + str(total)+ " accidentes ")
            print("Se encontraron: ")
            print("■ " + str(dic[1])+ " Accidentes de Severidad 1")
            print("■ " + str(dic[2])+ " Accidentes de Severidad 2")
            print("■ " + str(dic[3])+ " Accidentes de Severidad 3")
            print("■ " + str(dic[4])+ " Accidentes de Severidad 4")
    
    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes antes de una fecha: ")
        Date = input("Fecha (YYYY-MM-DD): ")
        tup = controller.getAccidentsBeforeDate(cont, Date)
        total=tup[1]
        if total==0:
            print("\nNo se encontraron accidentes antes de esa fecha")
        else:
            fecha= tup[0].strftime('%Y-%m-%d')
            print("\nAntes de la fecha seleccionada hubo un total de " + str(total)+ " accidentes.")
            print("\nLa fecha que más accidentes tuvo antes del {}, fue el {} del {} del {}.".format(Date,fecha[8:10],fecha[5:7],fecha[0:4]))
    
    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes en un rango de fechas: ")
        inicialdate = input("Fecha inicial (YYYY-MM-DD): ")
        finaldate = input("Fecha final (YYYY-MM-DD): ")
        dic = controller.getAccidentsbyrange(cont, inicialdate, finaldate)
        if dic[0][1]==0 and dic[0][2]==0 and dic[0][3]==0 and dic[0][4]==0:
            print("\nNo se encontraron accidentes en esa fecha")
        else:
            print("\nEn la fecha seleccionada hubo un total de " + str(dic[1])+ " accidentes ")
            print("La categoría con mayor número de accidentes es Severidad " + str(dic[2])+ " con un total de "+ str(dic[3])+ " accidentes.")
            print("Se encontraron: ")
            print("■ " + str(dic[0][1])+ " Accidentes de Severidad 1")
            print("■ " + str(dic[0][2])+ " Accidentes de Severidad 2")
            print("■ " + str(dic[0][3])+ " Accidentes de Severidad 3")
            print("■ " + str(dic[0][4])+ " Accidentes de Severidad 4")
    elif int(inputs[0]) == 6:
        print("\nBuscando estado más accidentado en un rango de fechas: ")
        initialDate = input("Fecha inicial (YYYY-MM-DD): ")
        finalDate = input("Fecha final (YYYY-MM-DD): ")
        info = controller.getAccidentsByState(cont,initialDate,finalDate)
        print("Entre {} y {}, el estado en el que mas accidentes hubo fue {}, con un total de {} accidentes.".format(initialDate,finalDate,info[0], info[1]))
        print("La fecha en la que más accidentes hubo fue {}.".format(info[2]))
    
    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes en un rango de horas: ")
        print("Recuerde que las horas están en formato 00:00 a 23:59")
        inic = input("Ingrese el rango inferior de horas que desea buscar en formato HH:MM : ")
        final = input("Ingrese el rango superior de horas que desea buscar en formato HH:MM : ")
        info = controller.getAccidentsByTime(cont, inic, final)
        print("\nPara el rango horario seleccionado existen:\n■ {} Accidentes de Severidad 1\n■ {} Accidentes de Severidad 2\n■ {} Accidentes de Severidad 3\n■ {} Accidentes de Severidad 4".format(info[0],info[1],info[2],info[3]))
   
    elif int(inputs[0]) == 8:
        print("\nBuscando accidentes en el radio de una locación")
        latitud=float(input("Digite la latitud del punto inicial: "))
        longitud=float(input("Digite la longitud del punto inicial: "))
        radio=float(input("Digite el radio de búsqueda en km: "))
        res=controller.getAccidentsBylocation(cont,latitud,longitud,radio)
        print(res)
        print("\nEn el radio de {} km medidos desde {} de latitud y {} de longitud hubo {} accidentes:".format(radio,latitud,longitud,res[1]))
        print("Se encontraron: ")
        print("■ {} Accidentes el Domingo\n■ {} Accidentes el Lunes\n■ {} Accidentes el Martes\n■ {} Accidentes el Miércoles\n■ {} Accidentes Jueves\n■ {} Accidentes Viernes\n■  {} Accidentes el Sábado ".format(res[0][0],res[0][1],res[0][2],res[0][3],res[0][4],res[0][5],res[0][6]))
    else:
        sys.exit(0)
sys.exit(0)