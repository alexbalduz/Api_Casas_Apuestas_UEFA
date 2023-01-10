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
        if local in self.df_golesLocal.index and visitante in self.df_golesLocal.index:
            cuota_local = self.df_golesLocal.at[local, 'GolesLocal'] * self.df_golesLocal.at[visitante, 'GolesVisitante']
            cuota_visitante = self.df_golesLocal.at[visitante, 'GolesVisitante'] * self.df_golesLocal.at[local, 'GolesLocal']
            probabilidad_empate, probabilidad_local, probabilidad_visitante = 0, 0, 0
            for x in range(0, 11): # Numero de goles del equipo local
                for y in range(0, 11): #Numero de goles del equipo visitante
                    p = poisson.pmf(x, cuota_local) * poisson.pmf(y, cuota_visitante)
                    if x == y:
                        probabilidad_empate += p
                    elif x>y:
                        probabilidad_local += p
                    else:
                        probabilidad_visitante += p

            puntos_local = 3*probabilidad_local + probabilidad_empate
            puntos_visitante = 3*probabilidad_visitante + probabilidad_empate
            probabilidad_local = round(puntos_local/(puntos_local + puntos_visitante), 2)
            probabilidad_visitante = round(puntos_visitante/(puntos_local + puntos_visitante), 2)
            probabilidad_empate = round(1 - probabilidad_local - probabilidad_visitante, 2)
            return (puntos_local, puntos_visitante)

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