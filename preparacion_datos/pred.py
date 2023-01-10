import pandas as pd
from normalizacion import NormalizacionNombres

class Prediccion():

    def __init__(self):
        #Leemos el csv de equipos
        self.listaEquipos = pd.read_csv ('docs/equipo.csv')
        print(self.listaEquipos.head())

        #Vemos con qué tipo de datos trabajamos
        self.equipos = self.listaEquipos['Equipo']
        print(type(self.equipos))

        #Convertimos a lista
        self.equipos=list(self.equipos)

        #Definimos todos los años como un array
        self.años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11","2009-10","2008-09"
        ,"2007-08","2006-07","2005-06","2004-05","2003-04","2002-03","2001-02","2000-01"]

    def contarGolesChampions(self):
        self.Champions={}
        #Leemos los datos de la Champions
        for año in self.años:
            self.Champions[f'{año}'] = pd.read_csv(f'datas/Champions/resultados_{año}.csv')

        #Diccionarios para guardar los goles de cada equipo
        self.golesLocal = {}
        self.golesVisitante = {}

        #Inicializamos los diccionarios
        for equipo in self.equipos:
            self.golesLocal[equipo] = 0
            self.golesVisitante[equipo] = 0

        for año in self.años:
            for i in range(len(self.Champions[año])):
                if str(self.Champions[año].iloc[i]['Local']) in self.equipos:
                    self.golesLocal[self.Champions[año].iloc[i]['Local']] += int(self.Champions[año].iloc[i]['GolesLocal'])
                if self.Champions[año].iloc[i]['Visitante'] in self.equipos:
                    self.golesVisitante[self.Champions[año].iloc[i]['Visitante']] += int(self.Champions[año].iloc[i]['GolesVisitante'])
            print(f'año {año} terminado')

        #print(self.golesLocal)

    def golesLigasNacionales(self):
        self.golesLigaLocal = {}
        self.golesLigaVisitante = {}
        #Recorremos todos los equipos
        for equipo in self.equipos:
            self.golesLigaLocal[equipo] = 0
            self.golesLigaVisitante[equipo] = 0
            self.pais = str(self.listaEquipos['Pais'][self.listaEquipos['Equipo'] == equipo].iloc[0])
            if self.pais.lower() == 'paises bajos':
                self.pais = 'Holanda'
            self.pais = NormalizacionNombres(self.pais)
            self.datos = pd.read_csv(f'datas/LigasNacionales/{self.pais}2021-22.csv')
            if self.pais != 'moldavia':
                for i in range(len(self.datos)):
                    if str(self.datos.iloc[i]['Local']) == str(equipo):
                        print(equipo)
                        self.golesLigaLocal[equipo] += int(self.datos.iloc[i]['GolesLocal'])
                    if str(self.datos.iloc[i]['Visitante']) == str(equipo):
                        self.golesLigaVisitante[equipo] += int(self.datos.iloc[i]['GolesVisitante'])
            else:
                self.golesLigaLocal[equipo] += int(self.datos.iloc[0]['goles A favor'])/2
                self.golesLigaVisitante[equipo] += int(self.datos.iloc[0]['goles A favor'])/2


        #print(golesLigaVisitante)
        #print(golesLigaLocal)
    def convertirGolesChampions(self):
        df1= pd.DataFrame([[key, self.golesLocal[key]] for key in self.golesLocal.keys()], columns = ['EquipoEnLocal', 'golesLocal'])
        df1.to_csv('golesLocal.csv', index=False)
        df2 = pd.DataFrame([[key, self.golesVisitante[key]] for key in self.golesVisitante.keys()], columns = ['EquipoEnVisitante', 'golesVisitante'])
        df2.to_csv('golesVistante.csv', index=False)
        df3 = pd.concat([df1, df2], axis=1)
        df3.to_csv('golesChampions.csv', index=False)
        print(df3)


    def convertirGolesLiga(self):
        df3 = pd.DataFrame([[key, self.golesLigaVisitante[key]] for key in self.golesLigaVisitante.keys()], columns=['Equipo', 'goles'])
        df3.to_csv('golesLigaVisitante.csv', index=False)
        df4 = pd.DataFrame([[key, self.golesLigaLocal[key]] for key in self.golesLigaLocal.keys()], columns=['Equipo', 'goles'])
        df4.to_csv('golesLigaLocal.csv', index=False)
        print(df3)
        print(df4)




if __name__ == '__main__':
    pred = Prediccion()
    pred.Champions()
    pred.convertirGolesChampions()