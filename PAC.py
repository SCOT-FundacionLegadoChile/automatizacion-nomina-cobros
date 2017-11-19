#######################################################################################################################
#
# Codigo de Automatizacion de la Nomina de Cobros de socios FLC
#
#   El codigo toma el ARCHIVO UINVERSO descargado desde el banco y debe generar la
#   NOMINA DE COBROS para subir luego al banco con el detalle de los cobros por PAC
#   a los socios de FLC inscritos.
#
# Estructura ARCHIVO UNIVERSO
#
#   0   (3)      3     (3)      6     (3)       9     10    (22)        32          33   (8)       41     (8)       49
#   | cod. banco | cod. empresa | cod. convenio | 'D' | id. de servicio | 'espacio' | AAAAMMDD gen | AAAAMMDD serv. | 'espacio' |
#
#   ...:::...:......................:........::::::::.
#   001015051D0000000000000029788537 2017103120161109
#
# Estructura NOMINA DE COBROS
#
#   0     (3)    3     (3)      6      (3)      9     10     (22)       32          33     (10)      43    (11)    54     (8)       62     (8)       70 (10)
#   | cod. banco | cod. empresa | cod. convenio | 'D' | id. de servicio | 'espacio' | info adicional | monto cargo | AAAAMMDD fact. | AAAAMMDD venc. | .'s |
#
#
#   ...:::...:......................:..........:::::::::::........::::::::..........
#   001015051D029788537              L.GALLARDO000002929002017110120171106..........
#
#
#######################################################################################################################

# noinspection PyUnresolvedReferences
import numpy as np
from xlrd import open_workbook

# 1. Extraer nombres y montos de cobro de 'Registro Donaciones.xls'
#

mes = "Septiembre 2017"
wb = open_workbook('Registro Donaciones.xls')

items = []
rows   = []
nombres = []
montos_uf = []
montos_clp = []

sheet = wb.sheet_by_name('PACs')
nrows = sheet.nrows
ncols = sheet.ncols
start_row = 0

# Encontrar mes correspondiente hoja de calculo
for row in range (1,nrows):
    value = sheet.cell(row, 0).value
    if value == mes:
        start_row = row

# Extraer nombres y montos de cobro
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

    #print(sheet.cell(0,0).value)
    #print(start)
    #print(end)
    #print(Nombre)
    print(montos_clp)


# 2. Leer archivo universo y escribir archivo de cobros
#
file_object = open("Cobro noviembre.txt", "r")

spaces = "              " # 14 espacios
dots   = ".........."
contador = 0

archivo_final = []

for line in file_object:
    aux1 = line[0:10]
    aux2 = line[23:32]
    monto_cobro = (str(montos_clp[contador] + "00")).zfill(11)
    archivo_final.append(aux1 + aux2 + spaces + nombres[contador] + monto_cobro + dots)
    contador += 1

a = "0020"
F = str(Monto[1]+a)
#a[-3:-1]=b
print(F.zfill(13))
