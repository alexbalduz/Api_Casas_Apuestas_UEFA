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
equipos=listaEquipos['Equipo']
print(type(equipos))

#Convertimos a lista
equipos=list(equipos)
print(type(equipos))
print(equipos)

#Normalizamos los nombres de los equipos
for año in años:
    data=pd.read_csv(f'datas/Champions/resultados{año}.csv')
    diccionario={}
    for nombre in data.Local.unique():
        lista=str(nombre).lower().split()
        if 'inter' in lista:
            diccionario[nombre]='Internazionale'
        for equipo in equipos:
            if str(equipo).lower() in lista:
                diccionario[nombre]=str(equipo)
        if 'manchester' in lista:
            if 'united' in lista:
                diccionario[nombre]='Man. United'
            elif 'city' in lista:
                diccionario[nombre]='Man. City'
        elif 'lille' in lista:
            diccionario[nombre]='LOSC'
        elif 'París' in lista:
            diccionario[nombre]='Paris'
        elif 'sporting' in lista:
            if 'portugal' in lista:
                diccionario[nombre]='Sporting CP'
        elif 'donetsk' in lista:
            diccionario[nombre]='Shakhtar Donetsk'
        elif 'real' in lista:
            if 'madrid' in lista:
                diccionario[nombre]='Real Madrid'
        elif 'young' in lista:
            diccionario[nombre]='Young Boys'

    for nombre in diccionario:
        data["Local"] = data["Local"].replace(nombre,diccionario[nombre])
        data["Visitante"] = data["Visitante"].replace(nombre,diccionario[nombre])
    data.to_csv(f'Datos/resultados{año}.csv',index=False)

#Normalizamos los nombres de los equipos
def NormalizacionNombres(palabra:str):
    palabra=palabra.lower()
    palabra=palabra.replace("á","a")
    palabra=palabra.replace("é","e")
    palabra=palabra.replace("í","i")
    palabra=palabra.replace("ó","o")
    palabra=palabra.replace("ö","o")
    palabra=palabra.replace("ú","u")
    palabra=palabra.replace("ü","u")
    palabra=palabra.replace("ç","c")
    return palabra