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
    print("4- Buscar Accidentes antes de una fecha")
    print("5- Buscar Accidentes en un rango de fechas")
    print("6- Conocer Estado con más Accidentes")
    print("7- Conocer Accidentes por rango de horas")
    print("8- Conocer la zona geográfica más accidentada")
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
            print("Hubo " + str(dic[1])+ " accidentes de severidad 1")
            print("Hubo " + str(dic[2])+ " accidentes de severidad 2")
            print("Hubo " + str(dic[3])+ " accidentes de severidad 3")
            print("Hubo " + str(dic[4])+ " accidentes de severidad 4")
    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes antes de una fecha: ")
        Date = input("Fecha (YYYY-MM-DD): ")
        tup = controller.getAccidentsBeforeDate(cont, Date)
        fecha= tup[0].strftime('%Y-%b-%d')
        total=tup[1]
        print("\nAntes de la fecha seleccionada hubo un total de " + str(total)+ " accidentes.")
        print("\nLa fecha que más accidentes tuvo antes del " + Date + " fue el "+ fecha+".")
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        h1=input("Digite la hora inicial en formato HH:MM:SS: ")
        h2=input("Digite la hora final en formato HH:MM:SS: ")
        dic=controller.getAccidentsByHourRange(cont,h1,h2)
        total= dic[1]+dic[2] + dic[3]+ dic[4]
        if len(dic)==None:
            print("No se encontraron accidentes en el rango de horas")
        else:
            print("\nEn el rango de horas seleccionado hubo un total de " + str(total)+ " accidentes ")
            print("Hubo " + str(dic[1])+ " accidentes de severidad 1")
            print("Hubo " + str(dic[2])+ " accidentes de severidad 2")
            print("Hubo " + str(dic[3])+ " accidentes de severidad 3")
            print("Hubo " + str(dic[4])+ " accidentes de severidad 4")
        if controller.AccidentsSize(cont)>0:
            porcentaje=(total*100)/(controller.AccidentsSize(cont))
            print("""El porcentaje de accidentes sucedidos en el rango de horas elegido\ncomparado con las cantidad total de accidentes es: {0} %""".format(str(round(porcentaje,2))))
    elif int(inputs[0]) == 8:
        latitud=float(input("Digite la latitud del punto inicial: "))
        longitud=float(input("Digite la longitud del punto inicial: "))
        radio=float(input("Digite el radio de búsqueda en km: "))
        res=controller.getAccidentsBylocation(cont,latitud,longitud,radio)
        print(res)
    else:
        sys.exit(0)
sys.exit(0)
