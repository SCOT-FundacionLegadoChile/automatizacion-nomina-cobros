# Automatizacion Nomina Cobros

## Resumen
Cada mes el banco genera un archivo ‘cobro universo’. Con la información que este entrega (socios con PAC, entre otros) se debe generar y enviar al banco un archivo de cobro indicando el socio y el monto a cobrar (entre otros). En este momento la generación del archivo de cobro que se envía al banco se realiza de manera manual. La tarea es automatizar la generación de este archivo en base al archivo de origen ‘cobro universo’.

##Especificaciones
###Etapas
1. Script simple tipo ejecutable que tome el archivo universo y genere archivo de cobros
2. Generación de estadísticas y análisis simple de datos de cobro

## Preguntas
¿Porqué ‘Cobro Octubre’ tiene 134 ingresos y ‘COBRO1006’ tiene 133?
¿Porqué ‘Cobro Noviembre’ tiene 133 ingresos y ‘COBRO1103’ tiene 131?
¿Cómo se definía la fecha de facturación y vencimiento?

## Otros
Revisar links para obtener valor UF actualizado automáticamente:
http://mindicador.cl/
https://stackoverflow.com/questions/6386308/http-requests-and-json-parsing-in-python
http://docs.python-guide.org/en/latest/scenarios/json/
