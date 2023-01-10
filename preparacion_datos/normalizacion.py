import pandas as pd
import sys
sys.path.append('../')

#Definimos todos los años como un array
años = ["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
    ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]

#Leemos el csv de equipos
listaEquipos = pd.read_csv('docs/equipo.csv')
print(listaEquipos.head())

#Vemos con qué tipo de datos trabajamos
equipos = listaEquipos['Equipo']
print(type(equipos))

#Convertimos a lista
equipos = list(equipos)
print(type(equipos))
print(equipos)

#Normalizamos los nombres de los equipos
for año in años:
    df = pd.read_csv(f'datas/Champions/resultados_{año}.csv')
    #La clave sera el equipo y el valor los goles
    diccionario={}
    for nombre in df.Local.unique():
        list = str(nombre).lower().split()
        if 'inter' in list:
            diccionario[nombre] = 'Internazionale'
        for equipo in equipos:
            if str(equipo).lower() in list:
                diccionario[nombre] = str(equipo)
        if 'manchester' in list:
            if 'united' in list:
                diccionario[nombre] = 'Man. United'
            elif 'city' in list:
                diccionario[nombre] = 'Man. City'
        elif 'lille' in list:
            diccionario[nombre] = 'LOSC'
        elif 'París' in list:
            diccionario[nombre] ='Paris'
        elif 'sporting' in list:
            if 'portugal' in list:
                diccionario[nombre] = 'Sporting CP'
        elif 'donetsk' in list:
            diccionario[nombre] = 'Shakhtar Donetsk'
        elif 'real' in list:
            if 'madrid' in list:
                diccionario[nombre] = 'Real Madrid'
        elif 'young' in list:
            diccionario[nombre] = 'Young Boys'

    for nombre in diccionario:
        df["Local"] = df["Local"].replace(nombre,diccionario[nombre])
        df["Visitante"] = df["Visitante"].replace(nombre,diccionario[nombre])
    df.to_csv(f'datas/resultados{año}.csv',index=False)

#Normalizamos los nombres de los equipos
def NormalizacionNombres(nombre:str):
    nombre = nombre.lower()
    nombre = nombre.replace("á","a")
    nombre = nombre.replace("é","e")
    nombre = nombre.replace("í","i")
    nombre = nombre.replace("ó","o")
    nombre = nombre.replace("ö","o")
    nombre = nombre.replace("ú","u")
    nombre = nombre.replace("ü","u")
    nombre = nombre.replace("ç","c")
    return nombre