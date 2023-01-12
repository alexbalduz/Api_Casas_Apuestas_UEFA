from main.map import ApuestaSchema
from main.repositories.repositorioapuesta import ApuestaRepositorio
from main.repositories.repositoriocuota import CuotaRepositorio
from abc import ABC
from preparacion_datos.pred import Prediccion
from scipy.stats import poisson
import pandas as pd

apuesta_schema = ApuestaSchema()
apuesta_repositorio = ApuestaRepositorio()
cuota_repositorio = CuotaRepositorio()

class ApuestaService:
    #Constructor
    def __init__(self, df_total, df_golesLocal, df_golesVisitante):
        self.df_total = df_total
        self.df_golesLocal = df_golesLocal
        self.df_golesVisitante = df_golesVisitante

    def agregar_apuesta(self, apuesta, local, visitante):
        cuota = cuota_repositorio.find_by_partido(apuesta)
        probabilidad = self.set_cuota(cuota, local, visitante)
        apuesta.ganancia = round(apuesta.monto * probabilidad, 2)
        return apuesta_repositorio.create(apuesta)

    def set_cuota(self, cuota, local, visitante):
        if local:
            cuota_local = CuotaLocal()
            probabilidad = cuota_local.calcular_cuota(cuota)
            return probabilidad
        if visitante:
            cuota_visitante = CuotaVisitante()
            probabilidad = cuota_visitante.calcular_cuota(cuota)
            return probabilidad
        cuota_empate = CuotaEmpate()
        probabilidad = cuota_empate.calcular_cuota(cuota)
        return probabilidad

    def obtener_apuesta_por_id(self, id):
        return apuesta_repositorio.find_one(id)

    def obtener_apuestas_ganadas(self):
        return apuesta_repositorio.find_wins()

    def obtener_apuestas(self):
        return apuesta_repositorio.find_all()

class CuotaStrategy(ABC):
    def calcular_cuota(self, local, visitante, cuota):
        """Calcular probabilidad"""
        #Vemos si el equipo está considerado en el modelo
        if local in self.df_golesLocal.index and visitante in self.df_golesLocal.index:
            #Utilizamos at para saber el número exacto de goles que tiene el equipo local que se pasa por parámetro
            cuotaLocal = self.df_golesLocal.at[local, 'GolesLocal'] * self.df_golesLocal.at[visitante, 'GolesVisitante']
            #at para saber el número exacto de goles que tiene el equipo visitante que se pasa por parámetro
            cuotaVisitante = self.df_golesLocal.at[visitante, 'GolesVisitante'] * self.df_golesLocal.at[local, 'GolesLocal']
            #Definimos las probabilidades e inicializamos
            probabilidad_empate, probabilidad_local, probabilidad_visitante = 0, 0, 0
            #Numero de goles del equipo local
            for i in range(0, 11):
                #Numero de goles del equipo visitante
                for j in range(0, 11):
                    #Supongamos que no se marcan mas de 10 goles en un partido
                    #Utilizamos la distribucion de Poisson para calcular la probabilidad de que ocurran i goles para el equipo local y j goles para el equipo visitante
                    #utilizamos como mu las respectivas cuotas
                    #Usamos Poisson porque mide la probabilidad de que un evento ocurra bajo un parametro, el tiempo
                    #En este caso medimos las probabilidades de variables discretas
                    probabilidad_poisson = poisson.pmf(i, cuotaLocal) * poisson.pmf(j, cuotaVisitante)
                    #Si la probabilidad es la misma entonces están empatados
                    if i == j:
                        probabilidad_empate += probabilidad_poisson
                    #Si la probabilidad de la primera es mayor que la segunda entonces el equipo local gana
                    elif i > j:
                        probabilidad_local += probabilidad_poisson
                    #Si la probabilidad de la segunda es mayor que la primera entonces el equipo visitante gana
                    else:
                        probabilidad_visitante += probabilidad_poisson

            #Calculamos los puntos ganados por cada equipo(Local y Visitante)
            #Tenemos en cuenta que siempre se puntua cuando ganas(3 ptos) y cuando empatas(1 pto)
            puntosGanadosLocal = 3*probabilidad_local + probabilidad_empate
            puntosGanadosVisitante = 3*probabilidad_visitante + probabilidad_empate
            #Calculamos las probabilidades de que gane cada equip(Local o Visitante), rendondeamos a 2 decimales
            probabilidad_local = round(puntosGanadosLocal/(puntosGanadosLocal + puntosGanadosVisitante), 2)
            probabilidad_visitante = round(puntosGanadosVisitante/(puntosGanadosLocal + puntosGanadosVisitante), 2)
            #La probabilidad de empate sera la diferencia entre 1 y la suma de las probabilidades de ganar tambien redondeando
            #Esto es asi puesto que si a un suceso seguro le quitas las dos probabilidades de ganar independientes, el resultado es la probabilidad de empate(los dos ganar ptos)
            probabilidad_empate = round(1 - probabilidad_local - probabilidad_visitante, 2)
            return (puntosGanadosLocal, puntosGanadosVisitante)
        else:
            return (0, 0)

class CuotaLocal(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_local
        return probabilidad

class CuotaVisitante(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_visitante
        return probabilidad 

class CuotaEmpate(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_empate
        return probabilidad