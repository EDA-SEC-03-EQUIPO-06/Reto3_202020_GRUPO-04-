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
    print("4- Buscar Accidentes en un rango determinado")
    print("6- Buscar estado con mas accidentes en un rango de fechas")
    print("7- Buscar accidentes por rango de horas")
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
        print("\nBuscando accidentes en un rango de fecha: ")
        inicialdate = input("Fecha inicial (YYYY-MM-DD): ")
        finaldate = input("Fecha fianl (YYYY-MM-DD): ")
        dic = controller.getAccidentsbyrange(cont, inicialdate, finaldate)
        if dic[0][1]==0 and dic[0][2]==0 and dic[0][3]==0 and dic[0][4]==0:
            print("\nNo se encontraron accidentes en esa fecha")
        else:
            print("\nEn la fecha seleccionada hubo un total de " + str(dic[1])+ " accidentes ")
            print("La categoria con mayor numero de accidentes es " + str(dic[2])+ " con un total de "+ str(dic[3]))
            print("Hubo " + str(dic[0][1])+ " accidentes de severidad 1")
            print("Hubo " + str(dic[0][2])+ " accidentes de severidad 2")
            print("Hubo " + str(dic[0][3])+ " accidentes de severidad 3")
            print("Hubo " + str(dic[0][4])+ " accidentes de severidad 4")
            
    elif int(inputs[0]) == 6:
        initialDate = input("Fecha inicial (YYYY-MM-DD): ")
        finalDate = input("Fecha final (YYYY-MM-DD): ")
        info = controller.getAccidentsByRange(cont,initialDate,finalDate)
        print("Entre {} y {}, el estado en el que mas hubo accidentes fue {}, con un total de {} accidentes. La fecha en la que mas accidentes hubo fue {}".format(initialDate,finalDate,info[0], info[1], info[2]))
    
    elif int(inputs[0]) == 7:
        inic = input("Ingrese el rango inferior de horas que desea buscar en formato HH:MM: ")
        final = input("Ingrese el rango superior de horas que desea buscar en formato HH:MM: ")
        info = controller.getAccidentsByTime(cont, inic, final)
        print("\nPara el rango horario seleccionado existen:\n■ {} Accidentes de Severidad 1\n■ {} Accidentes de Severidad 2\n■ {} Accidentes de Severidad 3\n■ {} Accidentes de Severidad 4".format(info[0],info[1],info[2],info[3]))
        

    else:
        sys.exit(0)
sys.exit(0)