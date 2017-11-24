#######################################################################################################################
#
# Codigo de Automatizacion de la Nomina de Cobros de socios FLC
#
#   El codigo toma el ARCHIVO UINVERSO descargado desde el banco y debe generar la
#   NOMINA DE COBROS para subir luego al banco con el detalle de los cobros por PAC
#   a los socios de FLC inscritos.
#
# - Estructura ARCHIVO UNIVERSO
#
#     0   (3)      3     (3)      6     (3)       9     10    (22)        32          33   (8)       41     (8)       49
#     | cod. banco | cod. empresa | cod. convenio | 'D' | id. de servicio | 'espacio' | AAAAMMDD gen | AAAAMMDD serv. | 'espacio' |
#
#     ...:::...:......................:........::::::::.
#     001015051D0000000000000029788537 2017103120161109
#
# - Estructura NOMINA DE COBROS
#
#     0     (3)    3     (3)      6      (3)      9     10     (22)       32          33     (10)      43    (11)    54     (8)       62     (8)       70 (10)
#     | cod. banco | cod. empresa | cod. convenio | 'D' | id. de servicio | 'espacio' | info adicional | monto cargo | AAAAMMDD fact. | AAAAMMDD venc. | .'s |
#
#
#     ...:::...:......................:..........:::::::::::........::::::::..........
#     001015051D029788537              L.GALLARDO000002929002017110120171106..........
#
#
#######################################################################################################################

from xlrd import open_workbook
import urllib
import json
import requests

## INGRESAR DIRECCION DEL DOCUMENTO
# Universo = input("Ingrese la ubicacion del archivo Universo")
# Salida1  = input("Ingrese la ubicacion de destino archivo nomina cobro")
# Mes      = input("Ingrese la fecha de la forma: Mes A~no (Septiembre 2017)")
# Fecha1   = input("Ingrese fecha subida del documento de la forma A~noMesDia")
# Fecha2   = input("Ingrese fecha de cobro del banco de la forma A~noMesDia")
# Salida2  = "Nomina "+Mes

# 1. Extraer nombres y montos de cobro de 'Registro Donaciones.xls'
#

mes = 'Octubre 2017'
wb = open_workbook('Registro Donaciones.xls')

sheet = wb.sheet_by_name('PACs')
nrows = sheet.nrows
ncols = sheet.ncols
start_row = 0

# Encontrar mes correspondiente en hoja de calculo
for row in range (1,nrows):
    value = sheet.cell(row, 0).value
    if value == mes:
        start_row = row
        break;

if start_row == 0:
    print 'Error: no se encontro mes ingresado en registro de donaciones'
    exit()

# Extraer nombres y montos de cobro
items = []
rows   = []
nombres = []
montos_uf = []
montos_clp = []

for row in range (start_row, nrows):
    value = sheet.cell(row, 0).value
    if (value != 1) and (value != mes):
        end = row
        break

    name = sheet.cell(row, 2).value
    monto_uf = sheet.cell(row, 4).value
    monto_clp = sheet.cell(row, 5).value

    nombres.append(name[0:10])
    montos_uf.append(str(int(monto_uf)))
    montos_clp.append(str(int(monto_clp)))

# Docuentacion para extraer ultima uf en tiempo real
# http://api.sbif.cl/documentacion/UF.html
# HTTP GET http://api.sbif.cl/api-sbifv3/recursos_api/uf/2017/11?apikey=f2bff81776be1aa02fb4f9b6d112e5c3adb3a714&formato=json
#
# url = 'http://api.sbif.cl/api-sbifv3/recursos_api/uf/2017/11?apikey=f2bff81776be1aa02fb4f9b6d112e5c3adb3a714&formato=json'
# r = requests.get(url)
# response = json.loads(r.text)
# print response['UFs'][0]['Valor']

# 2. Leer archivo universo y escribir archivo de cobros
#
file_object = open('cobros pasados/Cobro octubre.txt', 'r')

# TODO: como se definen las fechas de facturacion y vencimiento??
fecha_facturacion = '20171102'
fecha_vencimiento = '20171106'
dots   = '..........'

archivo_final = []

i = 0
for line in file_object:
    if line[9] == 'D':
        aux1 = line[0:10] # cod. banco + cod. empresa + cod. convenio + 'D'
        aux2 = line[23:32].ljust(23) # id. servicio
        monto_cobro = str(montos_clp[i] + '00').zfill(11)
        nombre_socio = nombres[i].ljust(10)

        linea_cobro = aux1 + aux2 + nombre_socio + monto_cobro + fecha_facturacion + fecha_vencimiento + dots
        # print str(i+1) + ', ' + linea_cobro
        archivo_final.append(linea_cobro)

        i += 1
    elif line[9] == 'T':
        if int(line[33:39]) != i:
            print 'Error: numero de socios procesados vs indicados en universo, no coinciden'
    else:
        print 'Error: archivo universo corrupto'


#Crear archivo y guardar datos.

file = open('COBROx','w')
for i in range(0,len(archivo_final)):
    file.write(archivo_final[i]+"\n")
file.close()
