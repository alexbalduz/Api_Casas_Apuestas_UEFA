import pandas as pd
from normalizacion import NormalizacionNombres

#La intencion de este archivo es crear un modelo de predicción de goles con los datos ya normalizados
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

        #Recoremos todos los años
        for año in self.años:
            #Recoremos todos los partidos de la temporada
            for i in range(len(self.Champions[año])):
                #Se mete en la temporada de la champions, en la fila del fichero,
                # escogiendo solo la información de la columna Visitante. Si este equipo está en nuestra información
                # de equipos:
                if str(self.Champions[año].iloc[i]['Local']) in self.equipos:
                    #Se le suma a la temporada de la champions, en la fila del fichero, los goles del equipo local
                    self.golesLocal[self.Champions[año].iloc[i]['Local']] += int(self.Champions[año].iloc[i]['GolesLocal'])
                #Se realiza lo mismo pero con el equipo visitante
                if self.Champions[año].iloc[i]['Visitante'] in self.equipos:
                    self.golesVisitante[self.Champions[año].iloc[i]['Visitante']] += int(self.Champions[año].iloc[i]['GolesVisitante'])
            print(f'año {año} terminado')

    #Sacamos los ficheros con los goles contabilizados.
    def convertirGolesChampions(self):
        #Utilizamos los datos anteriores para obtener los csv con los goles como Local y como Visitante
        df_golesLocal = pd.DataFrame([[key, self.golesLocal[key]] for key in self.golesLocal.keys()], columns = ['EquipoLocal', 'golesLocal'])
        df_golesLocal.to_csv(f'preparacion_datos/golesLocal.csv', index=False)
        df_golesVisitante = pd.DataFrame([[key, self.golesVisitante[key]] for key in self.golesVisitante.keys()], columns = ['EquipoVisitante', 'golesVisitante'])
        df_golesVisitante.to_csv(f'preparacion_datos/golesVistante.csv', index=False)
        #Unimos los dos csv anteriores en uno solo para obtener el conjunto de goles de cada equipo en la champions
        df_total = pd.concat([df_golesLocal, df_golesVisitante], axis=1)
        df_total.to_csv(f'preparacion_datos/golesChampions.csv', index=False)


if __name__ == '__main__':
    prediccion = Prediccion()
    prediccion.contarGolesChampions()
    prediccion.convertirGolesChampions()