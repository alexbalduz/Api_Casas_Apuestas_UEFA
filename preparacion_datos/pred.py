import pandas as pd
from normalizacion import NormalizacionNombres

#Definimos todos los años como un array
años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
    ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]
Champions={}

#Leemos el csv de equipos
listaEquipos = pd.read_csv ('docs/equipo.csv')
print(listaEquipos.head())

#Vemos con qué tipo de datos trabajamos
equipos = listaEquipos['Equipo']
print(type(equipos))
equipos=list(equipos)

#Leemos los datos de la Champions
for año in años:
    Champions[f'{año}'] = pd.read_csv(f'datas/Champions/resultados_{año}.csv')

#Diccionarios para guardar los goles de cada equipo
golesLocal = {}
golesVisitante = {}

#Inicializamos los diccionarios
for equipo in equipos:
    golesLocal[equipo] = 0
    golesVisitante[equipo] = 0

#Recorremos los datos de la Champions
for año in años:
    for i in range(len(Champions[año])):
        if str(Champions[año].iloc[i]['Local']) in equipos:
            #Contamos los goles locales, para ello casteamos
            golesLocal[Champions[año].iloc[i]['Local']] += int(Champions[año].iloc[i]['GolesLocal'])
        if Champions[año].iloc[i]['Visitante'] in equipos:
            #Contamos los goles locales, para ello casteamos
            golesVisitante[Champions[año].iloc[i]['Visitante']] += int(Champions[año].iloc[i]['GolesVisitante'])
    print(f'año {año} terminado')

print(golesLocal)
print(golesVisitante)

