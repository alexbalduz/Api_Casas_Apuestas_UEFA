#El objetivo de este archivo es normalizar los nombres de los equipos para que coincidan con los de la base de datos de equipos

#Al normalizar todos los nombres, generamos un diccionario con clave el nombre del equipo y valor los goles.
#De esta forma, tendremos un diccionario con los goles de cada equipo.
#Además, limpiamos los nombres respecto cualquier tipo de error como lo son las tildes por ejemplo.


import pandas as pd
import sys
sys.path.append('../')

#Definimos todos los años como una lista(20 últimos años)
años = ["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
    ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]

#Leemos el csv de equipos
listaEquipos = pd.read_csv('docs/equipo.csv')
print(listaEquipos.head())

#Vemos con qué tipo de datos trabajamos
infoEquipos = listaEquipos['Equipo']
print(type(infoEquipos))

#Convertimos a lista
equipos = list(infoEquipos)
#Comprobacion
print(type(equipos))
print(equipos)

#Normalizamos los nombres de los equipos
for año in años:
    df_equipos = pd.read_csv(f'datas/Champions/resultados_{año}.csv')
    #La clave sera el equipo y el valor los goles
    diccionario={}
    for nombre in df_equipos.Local.unique():
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
        df_equipos["Local"] = df_equipos["Local"].replace(nombre,diccionario[nombre])
        df_equipos["Visitante"] = df_equipos["Visitante"].replace(nombre,diccionario[nombre])
    #Convertimos a csv para trabajar sobre los nuevos datos
    df_equipos.to_csv(f'datas/resultados{año}.csv',index=False)

#Normalizamos los nombres de los equipos para eliminar cualquier tipo de impureza
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